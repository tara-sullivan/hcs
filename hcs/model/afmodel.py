import numpy as np
import pandas as pd
import numba as nb

# Useful tools
import pdb
from quantecon.util import timing

init_spec = [
    ('ab_0', nb.float64[:, :]),
    ('h_0', nb.float64[:]),
    ('delta', nb.float64),
    ('v', nb.float64[:]),
    ('w', nb.float64[:]),
]


class ModelParams:
    '''
    Initialize model parameters
    '''
    def __init__(self,
                 ab_0,        # initial abilities
                 h_0=None,    # initial human capital
                 delta=0.96,  # discount rate
                 v=None,      # human capital update amount
                 w=None,      # default sector-specific wages
                 ):
        self.ab_0 = ab_0
        self.delta = delta
        # self.history_i = None

        # number of fields; used for initialized array
        n_j, _ = ab_0.shape
        if v is None:
            self.v = np.ones(n_j, dtype=np.float64)
        else:
            self.v = v
        if w is None:
            self.w = np.ones(n_j, dtype=np.float64)
        else:
            self.w = w  # (note: this was wages)
        if h_0 is None:
            self.h_0 = np.ones(n_j, dtype=np.float64)
        else:
            self.h_0 = h_0


history_spec = init_spec + [
    ('ab_t', nb.float64[:, :]),
    ('field_state', nb.float64[:]),
    ('chosen_field', nb.int8),
    ('c_history', nb.optional(nb.int16[:])),
    ('c_outcome', nb.optional(nb.int16[:])),
    ('n_switch', nb.int8),
    ('specialize_idx', nb.int8),
]


# Weird numba note! Numba jitclass does not work with numpy random seeding.
# When I want to seed my simulations, I need to comment out this decorator.
# I also need to comment out the numba decorator if I want to use some of my
# testing flags when simulating agent history (i.e. if I want agents to fail
# their first N courses, or if I want to force them to choose a particular
# course first). There may be a better way to do this, but numba jitclass is 
# super buggy. But if I need to run 10,000 simulations, it speeds up my code 
# x10, so it's staying. Would recommend sticking to numba function decorators
# in the future.
@nb.experimental.jitclass(history_spec)
class AgentHistory(ModelParams):
    '''
    Simulates agent's course history and specialization decision, given 
    their prior beliefs about their abilities, ab_0.
    '''
    # Work around: https://github.com/numba/numba/issues/1694
    __init__ModelParams = ModelParams.__init__

    def __init__(self, ab_0, delta=0.96, v=None, w=None, h_0=None):
        self.__init__ModelParams(ab_0, delta=delta, v=v, w=w, h_0=h_0)
        self.c_history = None
        self.c_outcome = None

    def get_index(self, ab_t):
        '''
        Evaluate the index function (i.e. expected lifetime payoff) given the
        current state ab_t. Note that ab_t is a J x 2 matrix
        '''
        # simplify terms
        delta, v = self.delta, self.v
        dd = np.ceil(delta / (1 - delta))
        # Payoff associated with studying an additional period
        study_payoff = (
            dd * delta**(dd - (np.sum(ab_t, axis=1)))) / (np.sum(ab_t, axis=1))
        I_t = (self.w * ab_t[:, 0] * v) / (1 - delta) * study_payoff
        # Find if in graduation region
        I_t = np.where(np.sum(ab_t, axis=1) < dd,
                       I_t,
                       np.multiply(ab_t[:, 0], v) / (1 - delta))
        # Rounding to get occasional equals
        # Numba bug: https://github.com/numba/numba/issues/4439
        out = np.empty_like(I_t)
        I_t = np.round(I_t, 8, out)

        return I_t

    def find_history_i(self, true_theta, fail_first=0, choose_first=-1):
        '''
        Find course history of agent i

            * choose_first: choose course j first
            * fail_first: fail first n number of courses

        Note: choose_first and fail_first do not work with numba (there is
        probably a way to fix that).
        '''
        # simplify terms
        delta, ab_0 = self.delta, self.ab_0
        dd = np.ceil(delta / (1 - delta))

        # make a copy of initial human capital levels
        ab_t = np.copy(ab_0)
        # find initial index
        I_t = self.get_index(ab_t)

        # calculate total courses
        total_courses = np.ceil(delta / (1 - delta)) - np.sum(ab_0, axis=1)

        # # Initialize course history
        c_t = np.empty(0, dtype=np.int16)
        c_outcome = np.empty(0, dtype=np.int16)
        n_switch = 0
        specialize_idx = 0

        # Find full course history
        keep_studying = 1
        while keep_studying == 1:
            # If no first course is specified, pick a random one
            if choose_first == -1:
                # Find the largest indices (there may be more than one)
                max_j = np.reshape(np.argwhere(I_t == np.max(I_t)), (-1,))
                # Randomly choose largest index
                choose_j = np.random.choice(max_j)
            # Otherwise specify which course comes first
            else:
                choose_j = choose_first
                choose_first = -1

            # Determine whether you are specialized
            if specialize_idx == 0:
                # Make dictionary of course counts
                # Note: https://github.com/numba/numba/pull/2959
                # course_counts = dict(zip(
                #     * np.unique(c_t, return_counts=True)))
                # Also: https://github.com/numba/numba/issues/5135
                # unique = np.unique(c_t)
                # pdb.set_trace()
                # unique_counts = np.array([len(c_t[np.where(c_t == x)]) for x in unique])
                # course_counts = dict(zip(unique, unique_counts))
                # pdb.set_trace()
                # course_counts = {x: len(c_t[np.where(c_t == x)]) for x in unique}
                # if choose_j not in course_counts:
                #     course_counts[choose_j] = 0
                course_counts = len(c_t[np.where(c_t == choose_j)])
                # calculate index as if you failed remaining courses
                fail_index = (
                    (1 / (1 - delta)) * delta ** (
                        total_courses[choose_j] - course_counts)
                    * (self.w[choose_j] * self.v[choose_j]
                        * ab_t[choose_j, 0])
                )
                # add failure index to index
                I_specialize = I_t.copy()
                I_specialize[choose_j] = fail_index
                max_specialize = np.argwhere(I_specialize == np.max(I_specialize))
                if max_specialize[0, 0] == choose_j:
                    specialize_idx = len(c_t) - 1

            # Graduate if in graduation region
            if np.sum(ab_t[choose_j, :]) >= dd:
                self.chosen_field = choose_j
                self.field_state = ab_t[choose_j, :]
                keep_studying = 0
            else:
                # study
                if fail_first == 0:
                    outcome_j = np.random.binomial(1, true_theta[choose_j])
                else:
                    outcome_j = 0
                    fail_first = max(fail_first - 1, 0)
                # update skills
                ab_t[choose_j, :] = ab_t[choose_j, :] + \
                    np.array([outcome_j, 1 - outcome_j])
                # record results
                if len(c_t) > 0:
                    if c_t[-1] != choose_j:
                        n_switch = n_switch + 1
                c_t = np.append(c_t, np.int16(choose_j))
                c_outcome = np.append(c_outcome, np.int16(outcome_j))
                # update index
                I_t = self.get_index(ab_t)

        self.c_outcome = c_outcome
        self.c_history = c_t
        self.ab_t = ab_t
        self.n_switch = n_switch
        self.specialize_idx = specialize_idx


if __name__ == '__main__':

    np.random.seed(10)
    N = 10
    # Initial human capital levels
    ab_0 = np.array([[1, 1], [1, 1]], dtype=np.float64)
    wages = np.array([1, 1.25], dtype=np.float64)

    # Number of fields
    N_j = np.size(ab_0, axis=0)

    true_ability = np.random.beta(ab_0[:, 0], ab_0[:, 1], size=(N, N_j))

    # call instance of AFModel
    # timing.tic()
    afm = AgentHistory(ab_0, w=wages)

    afm.find_history_i(true_ability[0])
    # timing.toc()

    n_switch = np.empty(N)
    specialize_idx = np.empty(N)
    chosen_field = np.empty(N)
    field_state = np.empty((N, 2))
    course_history_list = []

    timing.tic()
    # Simulate course history for N agents
    for i in range(N):
        # afm.find_history_i(true_ability[i], fail_first=1)
        afm.find_history_i(true_ability[i])

        n_switch[i] = afm.n_switch
        specialize_idx[i] = afm.specialize_idx
        chosen_field[i] = afm.chosen_field
        field_state[i] = afm.field_state
        course_history_list.append(
            pd.DataFrame(list(zip(afm.c_history, afm.c_outcome)),
                         columns=['subject', 'outcome']))

    timing.toc()
    course_history = pd.concat(course_history_list,
                               keys=range(N),
                               names=['student', 't'])

    def print_i(idx):
        # Create a nice dataframe that summarizes the above output
        print('True ability: ' + str(true_ability[idx]))
        print('Course History: ')
        print(course_history.loc[idx])
        print(np.unique(course_history.loc[idx, 'subject'],
                        return_counts=True))
        print('Final state: ' + str(field_state[idx]))
        print('Number switches: ' + str(n_switch[idx]))
        print('Specialize index: ' + str(specialize_idx[idx]))

    # Print agent i's history
    print_i(0)
