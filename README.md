# 🚀 Rocket Flight Simulation

**Physics-based rocket flight simulator with real-time visualization and interactive web interface.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [Physics Model](#physics-model)
- [API Documentation](#api-documentation)
- [Examples](#examples)
- [Contributing](#contributing)
- [References](#references)

## Overview

This project implements a comprehensive physics-based rocket flight simulator that accurately models:

- **Thrust dynamics** - Engine burn characteristics and fuel consumption
- **Aerodynamic forces** - Drag coefficient and air resistance
- **Gravitational effects** - Altitude-dependent gravity
- **Real-time visualization** - Interactive plots and 3D trajectory display

The simulator supports sensitivity analysis, comparative simulations, and can be deployed as a web service.

## Features

✨ **Core Capabilities**
- Accurate physics-based flight dynamics
- Configurable rocket parameters (mass, thrust, burn time, drag)
- Multiple simulation modes (single run, comparative, sensitivity analysis)
- Real-time altitude, velocity, and acceleration calculations
- Energy and fuel consumption tracking

🎨 **Visualization**
- Interactive altitude vs. time plots
- Comparative trajectory visualization
- Sensitivity analysis heatmaps
- Web-based real-time dashboard

⚡ **API**
- RESTful API for simulation control
- JSON-based data interchange
- CORS support for frontend integration
- Configurable simulation parameters

## Quick Start

```bash
# Clone the repository
git clone https://github.com/tryr727-ai/rocket-flight-simulation.git
cd rocket-flight-simulation

# Install dependencies
pip install -r requirements.txt

# Run the CLI simulator
python src/cli/main.py

# Start the Flask web server
python app.py
# Open http://localhost:5000 in your browser
```

## Installation

### Requirements
- Python 3.9 or higher
- pip or conda package manager

### Setup

```bash
# Clone repository
git clone https://github.com/tryr727-ai/rocket-flight-simulation.git
cd rocket-flight-simulation

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

### Docker Setup (Optional)

```bash
# Build Docker image
docker build -t rocket-simulator .

# Run container
docker run -p 5000:5000 rocket-simulator
```

## Usage

### Command Line Interface

```python
from src.physics.rocket_simulation import RocketSimulation, RocketConfig

# Create rocket configuration
config = RocketConfig(
    mass=1000,           # kg
    thrust=500000,       # N (Newtons)
    burn_time=30,        # seconds
    drag_coefficient=0.5 # dimensionless
)

# Run simulation
sim = RocketSimulation(config)
times, altitudes, velocities = sim.simulate(total_time=100, dt=0.1)

# Visualize results
from src.visualization.visualizer import FlightVisualizer
visualizer = FlightVisualizer()
visualizer.plot_trajectory(times, altitudes, "Flight Trajectory")
visualizer.show()
```

### Web API

```bash
# Start server
python app.py

# Make simulation request
curl -X POST http://localhost:5000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "mass": 1000,
    "thrust": 500000,
    "burn_time": 30,
    "drag_coefficient": 0.5,
    "simulation_time": 100,
    "time_step": 0.1
  }'

# Response
{
  "status": "success",
  "data": {
    "trajectory": [...],
    "max_altitude": 5000,
    "max_velocity": 250
  }
}
```

## Architecture

```
rocket-flight-simulation/
├── src/
│   ├── physics/              # Physics engine
│   │   ├── constants.py      # Physical constants
│   │   ├── rocket.py         # Rocket class
│   │   └── simulator.py      # Simulation engine
│   ├── visualization/        # Plotting and graphs
│   │   ├── visualizer.py     # Main visualizer
│   │   └── styles.py         # Plot styling
│   ├── api/                  # Backend API
│   │   ├── routes.py         # API endpoints
│   │   └── models.py         # Pydantic models
│   └── cli/                  # Command-line interface
│       └── main.py           # CLI entry point
├── tests/                    # Unit tests
│   ├── test_physics.py
│   ├── test_simulation.py
│   └── test_api.py
├── docs/                     # Documentation
│   ├── PHYSICS.md            # Physics explanation
│   └── API.md                # API reference
├── templates/                # HTML templates
├── static/                   # CSS/JavaScript assets
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── app.py                    # Flask application entry point
└── README.md
```

## Physics Model

### Equations of Motion

The simulator uses the following kinematic equations:

```
F_net = F_thrust - F_weight - F_drag

where:
  F_thrust = thrust (N) [0 after burn_time]
  F_weight = mass × g (N)
  F_drag = drag_coefficient × velocity² (N)

acceleration (a) = F_net / mass
velocity (v) = v₀ + a × Δt
altitude (h) = h₀ + v × Δt
```

### Key Assumptions

1. **No wind resistance** (can be extended)
2. **Constant gravitational field** (g = 9.81 m/s²)
3. **No thrust vector control** (vertical flight only)
4. **Simplified drag model** (quadratic drag)
5. **Point mass approximation** (negligible rocket size)

### Limitations

- Single-stage rocket only (no staging)
- No atmospheric modeling (constant air density)
- No fuel mass loss modeling
- Vertical flight only (no angle control)

## API Documentation

### POST /api/simulate

Run a rocket flight simulation with specified parameters.

**Request:**
```json
{
  "mass": 1000,
  "thrust": 500000,
  "burn_time": 30,
  "drag_coefficient": 0.5,
  "simulation_time": 100,
  "time_step": 0.1
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "trajectory": {
      "times": [0, 0.1, 0.2, ...],
      "altitudes": [0, 0.05, 0.25, ...],
      "velocities": [0, 1, 2, ...],
      "accelerations": [0, 10, 10, ...]
    },
    "statistics": {
      "max_altitude": 5234.5,
      "max_velocity": 287.3,
      "max_acceleration": 45.2,
      "flight_time": 100.0
    }
  }
}
```

### GET /api/defaults

Get default simulation parameters.

### POST /api/sensitivity-analysis

Run sensitivity analysis on specified parameter.

## Examples

See the `examples/` directory for detailed examples:

- `simple_simulation.py` - Basic usage
- `comparative_analysis.py` - Multiple rocket comparison
- `sensitivity_study.py` - Parameter sensitivity
- `custom_engine.py` - Custom engine profiles

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_physics.py -v
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and commit them (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## References

### Physics & Rocket Science
- NASA: Rocket Thrust Equations - https://www.nasa.gov/
- Tsiolkovsky Rocket Equation - https://en.wikipedia.org/wiki/Tsiolkovsky_rocket_equation
- Anderson, J. D. (2000). Introduction to Flight (4th ed.)
- Sutton, G. P., & Biblarz, O. (2001). Rocket Propulsion Elements

### Python Libraries
- NumPy Documentation: https://numpy.org/doc/
- Matplotlib Documentation: https://matplotlib.org/
- Flask Documentation: https://flask.palletsprojects.com/
- Pytest Documentation: https://docs.pytest.org/

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to the physics and aerospace communities
- Inspired by real rocket flight dynamics
- Built with Python, NumPy, and Flask

## Contact

- **Author**: tryr727-ai
- **Repository**: https://github.com/tryr727-ai/rocket-flight-simulation
- **Issues**: https://github.com/tryr727-ai/rocket-flight-simulation/issues

---

**Last Updated**: 2026-05-09
