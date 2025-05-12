import random
import math
import numpy as np
from core_components import Bot, Dirt
from data_logger import record_data, record_path, generate_heatmap, init_paths

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

def createObjects(canvas, num_agents, brain_factory):
    agents = []
    passiveObjects = []
    count = StatsCounter(num_agents)
    shared_map = np.zeros((100, 100), dtype=int)

    # Generate dirt
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

        # Create strategy brain
        brain = brain_factory(bot, shared_map) if shared_map is not None else brain_factory(bot)
        bot.setBrain(brain)
        agents.append(bot)
        bot.draw(canvas)

    init_paths(agents)
    return agents, passiveObjects, count, shared_map

def moveIt(canvas, agents, passiveObjects, count, heatmap_title="Path Heatmap", heatmap_file="path_heatmap.png", cmap="Blues", max_steps=1000):
    def step(current_step=0, passive=passiveObjects):
        if current_step >= max_steps or not passive:
            print("--- Simulation Complete ---")
            for bot in agents:
                name = bot.name
                cleaned = count.agent_stats[name]["cleaned"]
                steps = bot.brain.steps
                print(f"{name}: Cleaned {cleaned} dirt | Steps taken: {steps}")

            generate_heatmap(title=heatmap_title, output=heatmap_file, cmap=cmap)
            return

        for bot in agents:
            bot.thinkAndAct(agents, passive)
            bot.update(canvas, passive, 1.0)
            passive = bot.collectDirt(canvas, passive, count)
            record_data(bot, current_step, count)
            record_path(bot)

        canvas.after(50, step, current_step + 1, passive)

    step()
