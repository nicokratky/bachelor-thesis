from scipy.interpolate import make_interp_spline
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sys

matplotlib.use("pgf")

sns.set()

OUTPUT_FILENAME = "../application-no-scaling.pgf"

# Dataset
x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
y = np.array([20, 20, 22, 27, 29, 26, 31, 26, 20])

x_y_spline = make_interp_spline(x, y)

x = np.linspace(x.min(), x.max(), 500)
y = x_y_spline(x)

y_supply = 25

fig, axs = plt.subplots(figsize=(5.6, 4.5))

axs.set_xlabel("Time")
axs.set_ylabel("Resources")

clock = [
    "00:00",
    "03:00",
    "06:00",
    "09:00",
    "12:00",
    "15:00",
    "18:00",
    "21:00",
    "24:00"]

axs.set_xticks([i for i in range(len(clock))])

axs.set_xticklabels(clock)
axs.set_yticklabels([])

axs.plot(x, y, label="resource demand")

axs.axhline(y=y_supply, linewidth=2, color="orange", label="resource supply")

axs.fill_between(
    x,
    y,
    y_supply,
    where=(
        y < y_supply),
    color="tab:green",
    alpha=0.3,
    label="overprovisioning")
axs.fill_between(
    x,
    y,
    y_supply,
    where=(
        y > y_supply),
    color="tab:red",
    alpha=0.3,
    label="underprovisioning")

axs.legend(loc="upper left")

# plt.show()
plt.savefig(OUTPUT_FILENAME)
