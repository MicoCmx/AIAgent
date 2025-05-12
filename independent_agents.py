import tkinter as tk
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
from core_components import Bot, Dirt, initialise

random.seed(42)
np.random.seed(42)

COLORS = ["red", "green", "blue", "purple", "orange"]

class StatsCounter:
    def __init__(self, num_agents):
        self.agent_stats = {f"Bot{i}": {"cleaned": 0} for i in range(num_agents)}
        self.total_cleaned = 0

    def itemCollected(self, canvas, agent_name):
        self.agent_stats[agent_name]["cleaned"] += 1
        self.total_cleaned += 1
        canvas.delete("dirtCount")
        canvas.create_text(50, 50, anchor="w",
                           text="Total dirt collected: " + str(self.total_cleaned),
                           tags="dirtCount")

# --- 数据记录与热力图相关功能 ---
def record_data(agent, step, count):
    data = {
        'step': step,
        'bot_name': agent.name,
        'cleaned': count.agent_stats[agent.name]["cleaned"],
        'total_cleaned': count.total_cleaned,
        'x': agent.x,
        'y': agent.y
    }
    with open("cleaning_data.csv", mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writerow(data)

paths = {}

def record_path(bot):
    if bot.name not in paths:
        paths[bot.name] = []
    paths[bot.name].append((bot.x, bot.y))

# --- 独立智能体策略类 ---
class IndependentBrain:
    def __init__(self, bot):
        self.bot = bot
        self.turningCount = 0
        self.movingCount = random.randint(50, 100)
        self.currentlyTurning = False
        self.steps = 0

    def thinkAndAct(self, x, y, sl, sr, count, agents):
        self.steps += 1

        avoid_result = self.bot.avoidOthers(agents)
        if avoid_result:
            return avoid_result

        if self.currentlyTurning:
            speedLeft = -2.0
            speedRight = 2.0
            self.turningCount -= 1
        else:
            speedLeft = 5.0
            speedRight = 5.0
            self.movingCount -= 1

        if self.movingCount <= 0 and not self.currentlyTurning:
            self.turningCount = random.randint(20, 40)
            self.currentlyTurning = True
        if self.turningCount <= 0 and self.currentlyTurning:
            self.movingCount = random.randint(50, 100)
            self.currentlyTurning = False

        return speedLeft, speedRight, None, None

# --- 初始化对象 ---
def createObjects(canvas, num_agents=5):
    agents = []
    passiveObjects = []
    count = StatsCounter(num_agents)

    i = 0
    for xx in range(10):
        for _ in range(50 + random.randint(-10, 10)):
            x = xx * 100 + random.randint(0, 100)
            y = random.randint(0, 100)
            dirt = Dirt("Dirt" + str(i), x, y)
            i += 1
            passiveObjects.append(dirt)
            dirt.draw(canvas)
    for yy in range(1, 10):
        for _ in range(100 + random.randint(-10, 10)):
            x = 900 + random.randint(0, 100)
            y = yy * 100 + random.randint(0, 100)
            dirt = Dirt("Dirt" + str(i), x, y)
            i += 1
            passiveObjects.append(dirt)
            dirt.draw(canvas)
    for xx in range(9):
        for yy in range(1, 10):
            for _ in range(10 + random.randint(-3, 3)):
                x = xx * 100 + random.randint(0, 100)
                y = yy * 100 + random.randint(0, 100)
                dirt = Dirt("Dirt" + str(i), x, y)
                i += 1
                passiveObjects.append(dirt)
                dirt.draw(canvas)

    placed = []
    for k in range(num_agents):
        x = random.randint(100, 900)
        y = random.randint(100, 900)
        while any(math.hypot(x - px, y - py) < 100 for px, py in placed):
            x = random.randint(100, 900)
            y = random.randint(100, 900)
        placed.append((x, y))
        color = COLORS[k % len(COLORS)]
        bot = Bot(f"Bot{k}", passiveObjects, count, color=color)
        bot.x = x
        bot.y = y
        brain = IndependentBrain(bot)
        bot.setBrain(brain)
        agents.append(bot)
        bot.draw(canvas)

    return agents, passiveObjects, count

# --- 运行循环 ---
def moveIt(canvas, agents, passiveObjects, count, max_steps=1000):
    def step(current_step=0, passive=passiveObjects):
        if current_step >= max_steps or not passive:
            print("--- Simulation Complete ---")
            for bot in agents:
                name = bot.name
                cleaned = count.agent_stats[name]["cleaned"]
                steps = bot.brain.steps
                print(f"{name}: Cleaned {cleaned} dirt | Steps taken: {steps}")

            all_paths = []
            for path in paths.values():
                all_paths.extend(path)
            if all_paths:
                x, y = zip(*all_paths)
                plt.figure(figsize=(8, 6))
                sns.kdeplot(x=x, y=y, cmap="Reds", fill=True, thresh=0, levels=100)
                plt.title("Independent Agent Path Heatmap")
                plt.savefig("independent_path_heatmap.png")
                plt.close()
            return

        for bot in agents:
            bot.thinkAndAct(agents, passive)
            bot.update(canvas, passive, 1.0)
            passive = bot.collectDirt(canvas, passive, count)
            record_data(bot, current_step, count)
            record_path(bot)

        canvas.after(50, step, current_step + 1, passive)

    step()

# --- 主函数 ---
def main():
    window = tk.Tk()
    canvas = initialise(window)
    agents, passiveObjects, count = createObjects(canvas, num_agents=5)
    moveIt(canvas, agents, passiveObjects, count)
    window.mainloop()

if __name__ == "__main__":
    main()
