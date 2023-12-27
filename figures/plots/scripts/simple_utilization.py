import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

matplotlib.use("pgf")

sns.set()

CPU_UTILIZATION_DATA = "../data/cpu-utilization-vertical-controller-1node-30min.csv"
MEMORY_UTILIZATION_DATA = "../data/memory-utilization-vertical-controller-1node-30min.csv"

OUTPUT_FILENAME = "../simple-utilization-vertical-controller-1node-30min.pgf"

SCRAPE_INTERVAL = 5

# CPU Utilization

columns = ["Time", "cpu_utilization"]
df = pd.read_csv(CPU_UTILIZATION_DATA, usecols=columns)

x = pd.Series([val.timestamp() for val in pd.to_datetime(df["Time"])]).tolist()
x = [i * SCRAPE_INTERVAL for i in range(len(x))]
y = df["cpu_utilization"].tolist()

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

axs[1].plot(x, y)

fig.tight_layout()

# plt.show()
plt.savefig(OUTPUT_FILENAME)
