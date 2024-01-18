import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

matplotlib.use("pgf")

AVG_WRITE_LOAD_DATA = "../data/diagonal-elasticity-avgWriteLoadPerNode.csv"

OUTPUT_FILENAME = "../diagonal-elasticity_cluster-write-load.pgf"

sns.set_theme()

SCRAPE_INTERVAL = 5


def correct_nodecount(data):
    result = []
    multiplier = 0
    multiplier_added = False

    for x in data:
        if int(x) == 0 and not multiplier_added:
            multiplier += 1
            multiplier_added = True
        elif int(x) > 0:
            multiplier_added = False

        result.append(x * multiplier)

    return result


columns_writeLoad = ["Time", "avgWriteLoadPerNode"]
df_writeLoad = pd.read_csv(AVG_WRITE_LOAD_DATA, usecols=columns_writeLoad)
x_writeLoad = pd.Series(
    [int(val.timestamp() * 1000000) for val in pd.to_datetime(df_writeLoad["Time"])]
).tolist()
x_writeLoad = [i * SCRAPE_INTERVAL for i in range(len(x_writeLoad))]
y_writeLoad = df_writeLoad["avgWriteLoadPerNode"].tolist()

fig, ax = plt.subplots(figsize=(4.5, 2.7))

ax.set_xlabel("Time (s)")
ax.set_ylabel("Average Write Load")

ax.plot(x_writeLoad, y_writeLoad, label="write load per node")
ax.plot(
    x_writeLoad, correct_nodecount(y_writeLoad), label="write load of cluster"
)

ax.legend(fontsize=8)

fig.tight_layout()

# plt.show()
plt.savefig(OUTPUT_FILENAME)
