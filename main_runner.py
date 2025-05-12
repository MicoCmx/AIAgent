import tkinter as tk
import random
import numpy as np
from core_components import initialise
from simulation_core import createObjects, moveIt
from strategy_independent import IndependentBrain
from strategy_coordinated import CoordinatedBrain

def run_simulation(strategy_name: str, num_agents=5):
    random.seed(42)
    np.random.seed(42)

    window = tk.Tk()
    canvas = initialise(window)

    if strategy_name == "independent":
        print("Running Independent Strategy...")
        brain_factory = lambda bot, _: IndependentBrain(bot)
        cmap = "Reds"
        title = "Independent Agents Path Heatmap"
        file = "outputs/independent_path_heatmap.png"
    elif strategy_name == "coordinated":
        print("Running Coordinated Strategy...")
        brain_factory = lambda bot, shared_map: CoordinatedBrain(bot, shared_map)
        cmap = "Blues"
        title = "Coordinated Agents Path Heatmap"
        file = "outputs/coordinated_path_heatmap.png"
    else:
        raise ValueError("Unknown strategy: choose 'independent' or 'coordinated'")

    agents, passiveObjects, count, shared_map = createObjects(canvas, num_agents, brain_factory)
    moveIt(canvas, agents, passiveObjects, count, heatmap_title=title, heatmap_file=file, cmap=cmap)
    window.mainloop()

if __name__ == "__main__":
    import sys
    strategy = sys.argv[1] if len(sys.argv) > 1 else "independent"
    run_simulation(strategy)
