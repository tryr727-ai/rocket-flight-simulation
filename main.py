import numpy as np
import matplotlib.pyplot as plt

# Constants
GRAVITY = 9.81  # m/s^2

class Rocket:
    def __init__(self, mass, thrust, drag_coefficient):
        self.mass = mass  # kg
        self.thrust = thrust  # N
        self.drag_coefficient = drag_coefficient  # kg/m
        self.velocity = 0  # m/s
        self.altitude = 0  # m

    def update(self, dt):
        # Calculate forces
        weight = self.mass * GRAVITY
        drag = self.drag_coefficient * self.velocity**2
        net_force = self.thrust - weight - drag

        # Update velocity and altitude
        acceleration = net_force / self.mass
        self.velocity += acceleration * dt
        self.altitude += self.velocity * dt

    def simulate(self, total_time, dt):
        times = np.arange(0, total_time, dt)
        altitudes = []
        for _ in times:
            self.update(dt)
            altitudes.append(self.altitude)
        return times, altitudes

# Sensitivity Analysis
# Varying thrust and observing altitude at the end of the simulation
thrusts = [500, 600, 700]  # N
final_altitudes = []
for thrust in thrusts:
    rocket = Rocket(mass=1000, thrust=thrust, drag_coefficient=0.5)
    times, altitudes = rocket.simulate(total_time=100, dt=1)
    final_altitudes.append(altitudes[-1])

# Visualizing the results
plt.figure()
plt.plot(thrusts, final_altitudes, marker='o')
plt.title('Final Altitude vs. Thrust')
plt.xlabel('Thrust (N)')
plt.ylabel('Final Altitude (m)')
plt.grid(True)
plt.show()

# Comparative Simulations
thrusts = [500, 600, 700]  # N
colors = ['r', 'g', 'b']
plt.figure()
for i, thrust in enumerate(thrusts):
    rocket = Rocket(mass=1000, thrust=thrust, drag_coefficient=0.5)
    times, altitudes = rocket.simulate(total_time=100, dt=1)
    plt.plot(times, altitudes, label=f'Thrust = {thrust} N', color=colors[i])

plt.title('Altitude over Time for Different Thrusts')
plt.xlabel('Time (s)')
plt.ylabel('Altitude (m)')
plt.legend()
plt.grid(True)
plt.show()