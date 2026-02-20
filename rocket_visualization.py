import matplotlib.pyplot as plt
from typing import List, Tuple

class FlightVisualizer:
    def __init__(self, trajectories: List[Tuple[float, float]]):
        self.trajectories = trajectories

    def plot_trajectory(self, trajectory: Tuple[float, float], label: str):
        x, y = zip(*trajectory)
        plt.plot(x, y, label=label)
        plt.xlabel('Time')
        plt.ylabel('Altitude')
        plt.title('Rocket Trajectory')
        plt.legend()

    def show(self):
        plt.show()

    @staticmethod
    def compare_trajectories(trajectories: List[Tuple[float, float]], labels: List[str]):
        for trajectory, label in zip(trajectories, labels):
            FlightVisualizer.plot_trajectory(trajectory, label)
        plt.show()