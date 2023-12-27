import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

matplotlib.use("pgf")

CPU_LIMITS_DATA = "../data/diagonal-elasticity-limits-cpu.csv"
MEMORY_LIMITS_DATA = "../data/diagonal-elasticity-limits-memory.csv"

OUTPUT_FILENAME = "../diagonal-elasticity-limits.pgf"

sns.set()

SCRAPE_INTERVAL = 5

scaling_event_timestamps = [
    1703334464,
    1703335069,
    1703335670,
    1703336272,
    1703336872]

# CPU Limits

columns = ["Time", "cpu_limits"]
df = pd.read_csv(CPU_LIMITS_DATA, usecols=columns)

x = pd.Series([int(val.timestamp() * 1000000)
              for val in pd.to_datetime(df["Time"])]).tolist()
first_timestamp = x[0]
x = [i * SCRAPE_INTERVAL for i in range(len(x))]
y = df["cpu_limits"].tolist()
y = [val * 1000 for val in y]  # *1000 to convert to milliCPU

scaling_event_x = [(timestamp - first_timestamp)
                   for timestamp in scaling_event_timestamps]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.6, 4))

for index, value in enumerate(scaling_event_x):
    ax1.axvline(
        x=value,
        color="orange",
        ls=":",
        label="scaling event" if index == 0 else "")
    ax2.axvline(x=value, color="orange", ls=":")

ax1.set_xlabel('Time (s)')
ax1.set_ylabel('CPU Limits (milliCPU)')
ax1.set_ylim((1700, 2100))
ax1.plot(x, y)

# Memory Limits

columns = ["Time", "memory_limits"]
df = pd.read_csv(MEMORY_LIMITS_DATA, usecols=columns)

x = pd.Series([val.timestamp() for val in pd.to_datetime(df["Time"])]).tolist()
x = [i * SCRAPE_INTERVAL for i in range(len(x))]
y = df["memory_limits"].tolist()
y = [val / 1000000 for val in y]

ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Memory Limits (MiB)')
ax2.set_ylim((3000, 7000))
ax2.plot(x, y)

plt.figlegend(fontsize=8)

fig.tight_layout()

# plt.show()
plt.savefig(OUTPUT_FILENAME)
