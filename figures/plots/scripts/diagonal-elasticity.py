import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

matplotlib.use("pgf")

AVG_WRITE_LOAD_DATA = "../data/diagonal-elasticity-avgWriteLoadPerNode.csv"
NODE_COUNT_DATA = "../data/diagonal-elasticity-nodeCount.csv"
AVG_CPU_UTILIZATION_DATA = "../data/diagonal-elasticity-avgCpuUtilization.csv"
AVG_MEMORY_UTILIZATION_DATA = "../data/diagonal-elasticity-avgMemoryUtilization.csv"

TARGET_CPU_UTILIZATION = 0.6
TARGET_MEMORY_UTILIZATION = 0.7

OUTPUT_FILENAME = "../diagonal-elasticity.pgf"

sns.set_theme()

SCRAPE_INTERVAL = 5

scaling_event_timestamps = [1703334464, 1703335069, 1703335670, 1703336272, 1703336872]

columns_writeLoad = ["Time", "avgWriteLoadPerNode"]
df_writeLoad = pd.read_csv(AVG_WRITE_LOAD_DATA, usecols=columns_writeLoad)
x_writeLoad = pd.Series(
    [int(val.timestamp() * 1000000) for val in pd.to_datetime(df_writeLoad["Time"])]
).tolist()
first_timestamp = x_writeLoad[0]
x_writeLoad = [i * SCRAPE_INTERVAL for i in range(len(x_writeLoad))]
y_writeLoad = df_writeLoad["avgWriteLoadPerNode"].tolist()

scaling_event_x = [
    (timestamp - first_timestamp) for timestamp in scaling_event_timestamps
]

columns_nodeCount = ["Time", "nodeCount"]
df_nodeCount = pd.read_csv(NODE_COUNT_DATA, usecols=columns_nodeCount)
x_nodeCount = pd.Series(
    [val.timestamp() for val in pd.to_datetime(df_nodeCount["Time"])]
).tolist()
x_nodeCount = [i * SCRAPE_INTERVAL for i in range(len(x_nodeCount))]
y_nodeCount = df_nodeCount["nodeCount"].tolist()

columns_avgCpuUtilization = ["Time", "avgCpuUtilization"]
df_avgCpuUtilization = pd.read_csv(
    AVG_CPU_UTILIZATION_DATA, usecols=columns_avgCpuUtilization
)
x_avgCpuUtilization = pd.Series(
    [val.timestamp() for val in pd.to_datetime(df_avgCpuUtilization["Time"])]
).tolist()
x_avgCpuUtilization = [i * SCRAPE_INTERVAL for i in range(len(x_avgCpuUtilization))]
y_avgCpuUtilization = df_avgCpuUtilization["avgCpuUtilization"].tolist()

columns_avgMemoryUtilization = ["Time", "avgMemoryUtilization"]
df_avgMemoryUtilization = pd.read_csv(
    AVG_MEMORY_UTILIZATION_DATA, usecols=columns_avgMemoryUtilization
)
x_avgMemoryUtilization = pd.Series(
    [val.timestamp() for val in pd.to_datetime(df_avgMemoryUtilization["Time"])]
).tolist()
x_avgMemoryUtilization = [
    i * SCRAPE_INTERVAL for i in range(len(x_avgMemoryUtilization))
]
y_avgMemoryUtilization = df_avgMemoryUtilization["avgMemoryUtilization"].tolist()

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(5.6, 5))

for index, x in enumerate(scaling_event_x):
    ax1.axvline(
        x=x, color="orange", ls=":", label="scaling event" if index == 0 else ""
    )
    ax2.axvline(x=x, color="orange", ls=":")
    ax3.axvline(x=x, color="orange", ls=":")
    ax4.axvline(x=x, color="orange", ls=":")

ax1.set_title("a)")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Average Write Load Per Node")
ax1.plot(x_writeLoad, y_writeLoad)

ax2.set_title("b)")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("\\# nodes")
ax2.set_ylim((0.5, 3.5))
ax2.set_yticks(np.arange(min(y_nodeCount), max(y_nodeCount) + 1, 1))
ax2.plot(x_nodeCount, y_nodeCount)

ax3.set_title("c)")
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("CPU Utilization (%)")
ax3.set_ylim((-0.1, 1.1))
ax3.plot(x_avgCpuUtilization, y_avgCpuUtilization)
ax3.axhline(
    y=TARGET_CPU_UTILIZATION,
    color="tab:purple",
    ls="--",
    label="target CPU utilization",
)

ax4.set_title("d)")
ax4.set_xlabel("Time (s)")
ax4.set_ylabel("Memory Utilization (%)")
ax4.set_ylim((-0.1, 1.1))
ax4.plot(x_avgMemoryUtilization, y_avgMemoryUtilization)
ax4.axvspan(335, 610, color="red", alpha=0.3, label="k8ssandra reconsiliation")
ax4.axvspan(1050, 1400, color="red", alpha=0.3)
ax4.axhline(
    y=TARGET_MEMORY_UTILIZATION,
    color="tab:green",
    ls="--",
    label="target memory utilization",
)

plt.figlegend(fontsize=8, loc="upper center")

fig.tight_layout()

# plt.show()
plt.savefig(OUTPUT_FILENAME)
