import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

matplotlib.use("pgf")

sns.set_theme()

CPU_LIMITS_DATA = "../data/cpu-limits-vertical-controller-1node-30min.csv"
MEMORY_LIMITS_DATA = "../data/memory-limits-vertical-controller-1node-30min.csv"

OUTPUT_FILENAME = "../simple-limits-vertical-controller-1node-30min.pgf"

SCRAPE_INTERVAL = 5

# CPU Utilization

columns = ["Time", "cpu_limits"]
df = pd.read_csv(CPU_LIMITS_DATA, usecols=columns)

x = pd.Series([val.timestamp() for val in pd.to_datetime(df["Time"])]).tolist()
x = [i * SCRAPE_INTERVAL for i in range(len(x))]
y = df["cpu_limits"].tolist()
y = [val * 1000 for val in y]  # *1000 to convert to milliCPU

fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(5, 3.5))

axs[0].set_ylim((700, 1200))

axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("CPU Limits (milliCPU)")

axs[0].plot(x, y)

# Memory Utilization

columns = ["Time", "memory_limits"]
df = pd.read_csv(MEMORY_LIMITS_DATA, usecols=columns)

x = pd.Series([val.timestamp() for val in pd.to_datetime(df["Time"])]).tolist()
x = [i * SCRAPE_INTERVAL for i in range(len(x))]
y = df["memory_limits"].tolist()
y = [val / 1000000 for val in y]

axs[1].set_ylim((3000, 7500))

axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Memory Limits (MiB)")

axs[1].plot(x, y)

fig.tight_layout()

# plt.show()
plt.savefig(OUTPUT_FILENAME)
