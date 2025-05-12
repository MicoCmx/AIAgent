import os
import csv
import matplotlib.pyplot as plt
import seaborn as sns

# 确保输出目录存在
os.makedirs("outputs", exist_ok=True)

# 路径记录器
paths = {}

def init_paths(agents):
    global paths
    paths = {bot.name: [] for bot in agents}

def record_data(agent, step, count, filename="outputs/cleaning_data.csv"):
    data = {
        'step': step,
        'bot_name': agent.name,
        'cleaned': count.agent_stats[agent.name]["cleaned"],
        'total_cleaned': count.total_cleaned,
        'x': agent.x,
        'y': agent.y
    }
    with open(filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(data)

def record_path(bot):
    if bot.name in paths:
        paths[bot.name].append((bot.x, bot.y))

def generate_heatmap(title="Path Heatmap", output="outputs/path_heatmap.png", cmap="Blues"):
    all_coords = []
    for track in paths.values():
        all_coords.extend(track)
    if all_coords:
        x, y = zip(*all_coords)
        plt.figure(figsize=(8, 6))
        sns.kdeplot(x=x, y=y, cmap=cmap, fill=True, thresh=0, levels=100)
        plt.title(title)
        plt.savefig(output)
        plt.close()
