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

if __name__ == "__main__":
    plot_cleaning_progress("outputs/cleaning_data_independent.csv", "outputs/cleaning_data_coordinated.csv")
    plot_agent_barplot("outputs/cleaning_data_independent.csv", "outputs/cleaning_data_coordinated.csv")
