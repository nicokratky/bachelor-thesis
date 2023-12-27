import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import sys

# matplotlib.use("pgf")

AVG_WRITE_LOAD_DATA = "../data/horizontal-elasticity-avgWriteLoadPerNode.csv"
NODE_COUNT_DATA = "../data/horizontal-elasticity-node-count.csv"

OUTPUT_FILENAME = "../horizontal-elasticity.pgf"

sns.set()

SCRAPE_INTERVAL = 5

columns_writeLoad = ["Time", "avgWriteLoadPerNode"]
df_writeLoad = pd.read_csv(AVG_WRITE_LOAD_DATA, usecols=columns_writeLoad)

x_writeLoad = pd.Series([val.timestamp()
                        for val in pd.to_datetime(df_writeLoad["Time"])]).tolist()
first_timestamp = x_writeLoad[0] * 1000000000
x_writeLoad = [i * SCRAPE_INTERVAL for i in range(len(x_writeLoad))]
y_writeLoad = df_writeLoad["avgWriteLoadPerNode"].tolist()

scaling_event = 1703180193000
scaling_event_x = (scaling_event - first_timestamp) / 1000 / SCRAPE_INTERVAL

columns_nodeCount = ["Time", "nodeCount"]
df_nodeCount = pd.read_csv(NODE_COUNT_DATA, usecols=columns_nodeCount)

x_nodeCount = pd.Series([val.timestamp()
                        for val in pd.to_datetime(df_nodeCount["Time"])]).tolist()
x_nodeCount = [i * SCRAPE_INTERVAL for i in range(len(x_nodeCount))]
y_nodeCount = df_nodeCount["nodeCount"].tolist()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.6, 3))

ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Average Write Load Per Node")

ax2.set_xlabel("Time (s)")
ax2.set_ylabel("\\# nodes")

ax1.plot(x_writeLoad, y_writeLoad)
ax1.axvline(
    x=scaling_event_x,
    color="orange",
    ls="--",
    label="start of scaling action")
fig.legend(fontsize=8, loc="upper center")

ax2.set_ylim((0.5, 2.5))
ax2.set_yticks(np.arange(min(y_nodeCount), max(y_nodeCount) + 1, 1))
ax2.plot(x_nodeCount, y_nodeCount)

fig.tight_layout()

plt.show()
# plt.savefig(OUTPUT_FILENAME)
