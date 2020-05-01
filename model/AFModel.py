import numpy as np
import pandas as pd


class AgentHistory:
    '''
    Simulates agent's course history, given prior ab_0
    '''
    def __init__(self,
                 ab_0,        # initial human capital levels
                 delta=0.96,  # discount rate
                 v=1,         # human capital update amount
                 wages=None,  # default sector-specific wages
                 ):
        self.delta, self.v = delta, v
        self.ab_0 = ab_0
        if wages is None:
            self.w = np.ones(np.size(ab_0, 0))
        elif np.size(ab_0, 0) == np.size(wages, 0):
            self.w = wages
        else:
            print('ERROR: wage size mis-match.')

    def get_index(self, ab_t):
        "Evaluate the index function given the current state ab_t"
        # simplify terms
        delta, v = self.delta, self.v
        dd = np.ceil(delta / (1 - delta))
        # Payoff associated with studying an additional period
        study_payoff = (
            dd * delta**(dd - (np.sum(ab_t, axis=1)))) / (np.sum(ab_t, axis=1))
        I_t = (self.w * ab_t[:, 0] * v) / (1 - delta) * study_payoff
        # Find if in graduation region
        G_idx = np.argwhere(np.sum(ab_t, axis=1) >= dd)
        # Augment index if graduating
        I_t[G_idx] = ((ab_t[:, 0] * v) / (1 - delta))[G_idx]

        return I_t

    def history_i(self, true_theta, fail_first=0):
        "Determine the education decision of agent i"
        # simplify terms
        delta, ab_0 = self.delta, self.ab_0
        dd = np.ceil(delta / (1 - delta))

        # make a copy of initial human capital levels
        ab_t = np.copy(ab_0)
        # find initial index
        I_t = self.get_index(ab_t)

        # Initialize course history
        c_t = np.array([], dtype=str)
        c_outcome = np.array([], dtype=int)

        # Find full course history
        keep_studying = 1
        while keep_studying == 1:
            # Find the largest indices (there may be more than one)
            max_j = np.reshape(np.argwhere(I_t == np.max(I_t)), (-1,))
            # Randomly choose largest index
            choose_j = np.random.choice(max_j)

            if np.sum(ab_t[choose_j, :]) >= dd:
                chosen_field = choose_j
                field_state = ab_t[choose_j, :]
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
                c_t = np.append(c_t, 'j' + str(choose_j))
                c_outcome = np.append(c_outcome, outcome_j)
                # update index
                I_t = self.get_index(ab_t)

        return self.return_history_i(c_t, ab_t, chosen_field,
                                     field_state, c_outcome)

    class return_history_i:
        def __init__(self, c_t, ab_t, chosen_field, field_state, c_outcome):
            self.c_t = c_t
            self.ab_t = ab_t
            self.chosen_field = chosen_field
            self.field_state = field_state
            self.c_outcome = c_outcome


# Playing around with this class!
np.random.seed(10)
N = 4
# Initial human capital levels
ab_0 = np.array([[3, 2], [4, 3]])

# Number of fields
N_j = np.size(ab_0, axis=0)

# call instance of AFModel
afm = AgentHistory(ab_0, wages=np.array([2, 1]))

# true abilities for all people
true_ability = np.random.beta(ab_0[:, 0], ab_0[:, 1], size=(N, N_j))

chosen_field = np.empty(N, dtype=int)
field_state = np.empty((N, 2))
course_history_list = []

for i in range(N):
    history = afm.history_i(true_ability[i], fail_first=0)

    chosen_field[i] = history.chosen_field
    field_state[i] = history.field_state
    course_history_list.append(pd.DataFrame(list(zip(history.c_t,
                                                     history.c_outcome)),
                                            columns=['subject', 'outcome']))

course_history = pd.concat(course_history_list,
                           keys=range(N),
                           names=['student', 't'])


def print_i(idx):
    print('True ability: ' + str(true_ability[idx]))
    print('Course History: ')
    print(course_history.loc[idx])
    print(np.unique(course_history.loc[idx, 'subject'], return_counts=True))
    print('Final state: ' + str(field_state[idx]))


print_i(1)
