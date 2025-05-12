# Multi-Agent Vacuum Cleaner Simulation

This project simulates a multi-agent environment where several vacuum robots clean a dirt-filled grid. Two strategies are implemented:

- `independent_agents.py`: Robots wander randomly with basic collision avoidance.
- `coordinated_agents.py`: Robots share a global map and navigate toward the nearest reachable dirt.

## Project Structure

- `core_components.py`: Common classes (Bot, Dirt, avoid logic, sensors, etc.)
- `independent_agents.py`: Non-coordinated agent behavior.
- `coordinated_agents.py`: Map-sharing and dirt-targeting agent logic.

## Requirements

Run this to install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Simulation

Use the following commands:

```bash
python independent_agents.py
```

or

```bash
python coordinated_agents.py
```

## Notes

- Window canvas: 990x990
- Bots are square-shaped with 8 directional sensors.
- Dirt regenerates randomly across the grid in fixed zones.
- Robots have avoidance logic and movement animation.

## Notice

This code was developed as part of a coursework project for the Designing Intelligent Agents module (COMP4105) at the University of Nottingham.

