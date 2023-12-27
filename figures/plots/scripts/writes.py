import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys

matplotlib.use("pgf")

sns.set()


def get_data_path(number_of_nodes):
    return f"../data/stress-1000000writes-{number_of_nodes}node.csv"


def get_output_path(number_of_nodes):
    return f"../stress-1000000writes-{number_of_nodes}node.pgf"


SCRAPE_INTERVAL = 5

for num_nodes in range(1, 4):
    # CPU Utilization

    columns = ["Time", "write"]
    df = pd.read_csv(get_data_path(num_nodes), usecols=columns)

    x = pd.Series([val.timestamp()
                  for val in pd.to_datetime(df["Time"])]).tolist()
    x = [i * SCRAPE_INTERVAL for i in range(len(x))]
    y = df["write"].tolist()

    ymean = sum(y) / len(y)
    print(ymean)

    fig, axs = plt.subplots(figsize=(5.6, 2.5))

    axs.set_xlabel("Time (s)")
    axs.set_ylabel("Writes (op/s)")

    axs.plot(x, y)

    axs.axhline(
        y=ymean,
        color="red",
        label="average write operations per second")
    axs.legend(fontsize=8)

    fig.tight_layout()

    # plt.show()
    plt.savefig(get_output_path(num_nodes))
