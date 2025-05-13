
# Multi-Agent Vacuum Cleaner Simulation

This project simulates multiple intelligent robot vacuum cleaners navigating and cleaning a dirt-filled grid. The simulation compares two agent strategies:

- **Independent Agents**: Each robot acts randomly and independently.
- **Coordinated Agents**: Robots share a global map and plan more efficiently to avoid redundancy.

## Features

- Grid-based environment with dirt particles  
- Tkinter-based visual interface  
- Adjustable number of agents
- Two agent strategies (`independent` and `coordinated`)  
- Collision avoidance logic  
- Shared map coordination for cooperative agents
- Reproducible experiments via fixed random seed  
- Real-time performance data recording  
- Path heatmap generation with seaborn  
- Heatmap + trajectory visualization
- Dirt cleaning logs (CSV)
- Automatic generation of plots (efficiency, barplots)

## Requirements

- Python 3.10+
- numpy
- matplotlib
- seaborn

Install dependencies:

```bash
pip install -r requirements.txt
```

## Project Structure

```
├── core_components.py         # Robot, Dirt, and drawing logic  
├── strategy_independent.py    # Independent strategy class  
├── strategy_coordinated.py    # Coordinated strategy class  
├── simulation_core.py         # Common createObjects and moveIt  
├── data_logger.py             # Records data and heatmap  
├── visualise.py               # Generate visual graphics
├── main_runner.py             # Unified runner with strategy selection  
├── independent_agents.py      # Shortcut to run independent strategy  
└── coordinated_agents.py      # Shortcut to run coordinated strategy  
```

## Usage

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

Generate Visualisations:

```bash
python visualise.py
```

## Outputs

- `outputs/cleaning_data_*.csv`: agent cleaning logs 
- `outputs/*heatmap.png`: path heatmaps 
- `outputs/*trajectory.png`: trajectory plots 
- `outputs/cleaning_progress_plot.png`: overall efficiency 
- `outputs/agent_barplot.png`: per-agent performance

## Experiments

You can modify the number of agents or map layout inside `main_runner.py` or `simulation_core.py`.

## Reproducibility

This Project use fixed seeds (`random.seed(42)` and `np.random.seed(42)`) to ensure consistent behavior across runs.

## Note

Coursework submission for MSc Computer Science COMP4105 — University of Nottingham

## Report
A full report with analysis and results is available in the repository：https://www.overleaf.com/read/wvthpcyjgyjn#9a1cbf

## GitHub
Project repository: https://github.com/MicoCmx/AIAgent.git

Author: Mingxin Cao, University of Nottingham