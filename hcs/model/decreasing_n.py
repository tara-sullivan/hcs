import numpy as np
from scipy.stats import beta

import matplotlib.pyplot as plt

delta = 0.96
dd = delta / (1 - delta)

v = .1

a_f, b_f = 3*1, 2*1
a_m, b_m = a_f*2, b_f*2

# Mean and sample size
mu_m = beta.moment(1,a_m,b_m)
mu_f = beta.moment(1,a_f,b_f)
n_m, n_f = a_m + b_m, a_f + b_f
mu = mu_m

# def exit_condition_m(h, m):
h_j0 = 1
h_j = 1.7
m_j = 10



(v * n_range * mu + h_j - h_j0) / (h_j * (m_j + n_range))



# Plot figure
fig, ax = plt.subplots()

n_range = np.arange(1, 20)

exit_if = (delta / (1 - delta))

ax.plot(n_range, np.ones_like(n_range) * exit_if, '--')

# format axes
ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')

# label axes
ax.set_xlabel('')
ax.set_ylabel(r'$\frac{\delta}{1 - \delta}$')



plt.show()