# Multi-Agent Vacuum Cleaner Simulation

This project simulates multiple intelligent robot vacuum cleaners navigating and cleaning a dirt-filled grid. The simulation compares two agent strategies:

- **Independent Agents**: Each robot acts randomly and independently.
- **Coordinated Agents**: Robots share a global map and plan more efficiently to avoid redundancy.

## Features

- Grid-based environment with dirt particles
- Tkinter-based visual interface
- Two agent strategies (`independent` and `coordinated`)
- Collision avoidance logic
- Shared map coordination for cooperative agents
- Real-time performance data recording
- Path heatmap generation with seaborn
- Reproducible experiments via fixed random seed

## Project Structure
├── core_components.py # Robot, Dirt, and drawing logic
├── strategy_independent.py # Independent strategy class
├── strategy_coordinated.py # Coordinated strategy class
├── simulation_core.py # Common createObjects and moveIt
├── data_logger.py # Records data and heatmap
├── main_runner.py # Unified runner with strategy selection
├── independent_agents.py # Shortcut to run independent strategy
├── coordinated_agents.py # Shortcut to run coordinated strategy

## 🚀 Usage

Run one of the following scripts to start a simulation:


```bash
python independent_agents.py
python coordinated_agents.py
```

Or run manually:
```bash
python main_runner.py independent
python main_runner.py coordinated
```


## Outputs

- `cleaning_data.csv`: recorded metrics for each robot every step
- `*_path_heatmap.png`: visual heatmaps of agent movement paths

## Experiments

You can modify the number of agents or map layout inside `main_runner.py` or `simulation_core.py`.

## Reproducibility

We use fixed seeds (`random.seed(42)` and `np.random.seed(42)`) to ensure consistent behavior across runs.

## Note

Coursework submission for MSc Computer Science COMP4105 — University of Nottingham

