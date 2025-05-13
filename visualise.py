import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_cleaning_progress(indep_file, coord_file):
    df_i = pd.read_csv(indep_file)
    df_c = pd.read_csv(coord_file)

    indep = df_i.groupby("step")["cleaned"].sum().cumsum()
    coord = df_c.groupby("step")["cleaned"].sum().cumsum()

    plt.plot(indep, label="Independent", color="red")
    plt.plot(coord, label="Coordinated", color="blue")
    plt.title("Cumulative Dirt Cleaned")
    plt.xlabel("Step")
    plt.ylabel("Total Cleaned")
    plt.legend()
    plt.savefig("outputs/cleaning_progress_plot.png")
    plt.close()

def plot_agent_barplot(indep_file, coord_file):
    df_i = pd.read_csv(indep_file)
    df_c = pd.read_csv(coord_file)

    df_i['Strategy'] = 'Independent'
    df_c['Strategy'] = 'Coordinated'
    df_all = pd.concat([df_i, df_c])
    df_sum = df_all.groupby(['bot_name', 'Strategy'])['cleaned'].sum().reset_index()

    plt.figure(figsize=(8, 4))
    sns.barplot(x="bot_name", y="cleaned", hue="Strategy", data=df_sum)
    plt.title("Total Dirt Cleaned Per Agent")
    plt.savefig("outputs/agent_barplot.png")
    plt.close()

def plot_trajectories(indep_file, coord_file):
    for file, label in [(indep_file, "Independent"), (coord_file, "Coordinated")]:
        df = pd.read_csv(file)
        plt.figure(figsize=(6, 6))
        for bot in df["bot_name"].unique():
            bot_df = df[df["bot_name"] == bot]
            plt.plot(bot_df["x"], bot_df["y"], label=bot, alpha=0.7)
        plt.title(f"Agent Trajectories - {label}")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid(True)
        plt.axis("equal")
        outname = f"outputs/trajectory_{label.lower()}.png"
        plt.tight_layout()
        plt.savefig(outname)
        plt.close()


if __name__ == "__main__":
    indep_csv = "outputs/cleaning_data_independent.csv"
    coord_csv = "outputs/cleaning_data_coordinated.csv"

    plot_cleaning_progress(indep_csv, coord_csv)
    plot_agent_barplot(indep_csv, coord_csv)
    plot_trajectories(indep_csv, coord_csv)

