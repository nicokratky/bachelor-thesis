import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

matplotlib.use("pgf")

sns.set()

CPU_UTILIZATION_DATA = "../data/cpu-utilization-vertical-controller-1node-20min.csv"
MEMORY_UTILIZATION_DATA = "../data/memory-utilization-vertical-controller-1node-20min.csv"

CONTROLLER_START = 1702729489000

OUTPUT_FILENAME = "../utilization-vertical-controller-1node-20min.pgf"

SCRAPE_INTERVAL = 5

# CPU Utilization

columns = ["Time", "cpu_utilization"]
df = pd.read_csv(CPU_UTILIZATION_DATA, usecols=columns)

x = pd.Series([val.timestamp() for val in pd.to_datetime(df["Time"])]).tolist()
first_timestamp = x[0] * 1000000000
x = [i * SCRAPE_INTERVAL for i in range(len(x))]
y = df["cpu_utilization"].tolist()

controller_start_x = (CONTROLLER_START - first_timestamp) / \
    1000 / SCRAPE_INTERVAL

fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(5.6, 4))

axs[0].set_ylim((-0.1, 1.1))

axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('CPU Utilization (%)')

axs[0].plot(x, y)

# Memory Utilization

columns = ["Time", "memory_utilization"]
df = pd.read_csv(MEMORY_UTILIZATION_DATA, usecols=columns)

x = pd.Series([val.timestamp() for val in pd.to_datetime(df["Time"])]).tolist()
x = [i * SCRAPE_INTERVAL for i in range(len(x))]
y = df["memory_utilization"].tolist()

y = [min(val, 1) for val in y]  # ignore values > 100%

axs[1].set_ylim((-0.1, 1.1))

axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Memory Utilization (%)')

axs[1].axvspan(118, 412, color='red', alpha=0.3,
               label="k8ssandra reconsiliation")

axs[1].plot(x, y)

axs[1].axhline(y=0.7, color="tab:green", ls="--",
               label="target memory utilization")

for ax in axs:
    ax.axvline(x=controller_start_x, color="orange", ls="--",
               label="start of elasticity strategy controller")
    ax.legend(fontsize=8)

fig.tight_layout()

# plt.show()
plt.savefig(OUTPUT_FILENAME)
