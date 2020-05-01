import numpy as np
import pandas as pd

from AFModel import AgentHistory


def gen_agent_history(ab_0, true_ability, v=1):
    '''
    Creates a course history for a single agent.
    Uses initial state ab_0 to generate agent history using AFModel
    '''
    # Call agent history class
    afm = AgentHistory(ab_0, v=v)
    # Generate course history for agent
    history = afm.history_i(true_ability,fail_first=0)

    # print relevant variables
    print('True ability: ' + str(true_ability))
    history_pd = pd.DataFrame(list(zip(history.c_t, history.c_outcome)),
                              columns=['subject', 'outcome'])
    # Coiunt number of courses in chosen field
    print('Course History: ')
    print(history_pd)
    c_count = np.unique(history_pd['subject'], return_counts=True)
    print('Chosen field: ' + str(c_count[0][0]) +
          ' [' + str(c_count[1][0]) + ' courses]')
    print('Final state: ' + str(history.field_state))


# Initial human capital levels
ab_0_f = np.array([[4, 4], [2, 4]])
ab_0_m = ab_0_f * 1.5

# Number of fields
N_j = np.size(ab_0_f, axis=0)

# True ability
# true_ability = np.random.beta(ab_0_f[:, 0] + ab_0_m[:, 0],
#                               ab_0_f[:, 1] + ab_0_m[:, 1], size=N_j)
true_ability = [0.4, 0.8]

v_f = 1
v_m = v_f / 2

gen_agent_history(ab_0_f, true_ability, v_f)
gen_agent_history(ab_0_m, true_ability, v_m)
