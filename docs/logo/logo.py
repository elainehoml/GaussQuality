import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

dist1 = np.random.normal(5, 20, 100)
dist2 = np.random.normal(50, 30, 100)
x = np.linspace(-50, 120)
dist1_pdf = norm.pdf(x, 5, 20)
dist2_pdf = norm.pdf(x, 50, 30)

plt.style.use('seaborn')
plt.figure(figsize=(3,3))
# plt.hist(dist1, bins=15, density=True, color="#5e60ce", alpha=0.5)
# plt.hist(dist2, bins=15, density=True, color="#4ea8de", alpha=0.5)
plt.fill_between(x, np.zeros(len(x)), dist1_pdf, color="#5e60ce", alpha=0.5)
plt.fill_between(x, np.zeros(len(x)), dist2_pdf, color="#4ea8de", alpha=0.5)
plt.plot(x, dist1_pdf, color="#5e60ce")
plt.plot(x, dist2_pdf, color="#4ea8de")
plt.xticks([])
plt.yticks([])
plt.xlim([-80,150])
plt.ylim([-0.01,0.03])
plt.show()