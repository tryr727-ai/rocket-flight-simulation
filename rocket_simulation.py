from dataclasses import dataclass, replace

@dataclass
class RocketConfig:
    mass: float  # Mass of the rocket in kg
    thrust: float  # Thrust produced by the engines in N
    burn_time: float  # Time in seconds for which engines burn
    drag_coefficient: float  # Drag coefficient of the rocket

@dataclass
class RocketSimulation:
    config: RocketConfig
    altitude: float = 0.0  # Initial altitude
    velocity: float = 0.0  # Initial velocity
    time: float = 0.0  # Simulated time

    def step(self, delta_time: float):
        # Compute forces
        weight = self.config.mass * 9.81  # Weight of the rocket
        thrust = self.config.thrust if self.time < self.config.burn_time else 0
        drag = self.config.drag_coefficient * self.velocity ** 2

        # Net force
        net_force = thrust - weight - drag

        # Update acceleration
        acceleration = net_force / self.config.mass

        # Update velocity and altitude
        self.velocity += acceleration * delta_time
        self.altitude += self.velocity * delta_time
        self.time += delta_time

@dataclass
class SensitivityAnalysis:
    base_config: RocketConfig

    def vary_parameter(self, parameter_name: str, variation: float):
        # Vary a parameter and return the new configuration
        new_config = replace(self.base_config, **{parameter_name: variation})
        return new_config

    def run_analysis(self, parameter_name: str, variations: list):
        results = []
        for variation in variations:
            new_config = self.vary_parameter(parameter_name, variation)
            simulation = RocketSimulation(new_config)
            # Run simulation here (for simplicity, just recording final altitude)
            for _ in range(100):  # Simulate for 100 seconds
                simulation.step(1)  # 1 second time step
            results.append(simulation.altitude)
        return results
