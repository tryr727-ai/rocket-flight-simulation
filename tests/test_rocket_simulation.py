"""
Unit tests for rocket flight simulation module.

Tests cover physics calculations, configuration validation, and simulation behavior.
"""

import pytest
import logging
from src.physics.rocket_simulation import (
    RocketConfig,
    RocketSimulation,
    SimulationState,
    SensitivityAnalysis,
)
from src.physics.constants import (
    GRAVITY,
    DEFAULT_MASS,
    DEFAULT_THRUST,
    DEFAULT_BURN_TIME,
    DEFAULT_DRAG_COEFFICIENT,
)

logger = logging.getLogger(__name__)


class TestRocketConfig:
    """Test RocketConfig validation and initialization."""
    
    def test_valid_configuration(self):
        """Test creation of valid rocket configuration."""
        config = RocketConfig(
            mass=1000,
            thrust=500000,
            burn_time=30,
            drag_coefficient=0.5
        )
        assert config.mass == 1000
        assert config.thrust == 500000
        assert config.burn_time == 30
        assert config.drag_coefficient == 0.5
    
    def test_default_configuration(self):
        """Test default configuration values."""
        config = RocketConfig()
        assert config.mass == DEFAULT_MASS
        assert config.thrust == DEFAULT_THRUST
        assert config.burn_time == DEFAULT_BURN_TIME
        assert config.drag_coefficient == DEFAULT_DRAG_COEFFICIENT
    
    def test_invalid_mass_negative(self):
        """Test that negative mass raises ValueError."""
        with pytest.raises(ValueError):
            RocketConfig(mass=-100)
    
    def test_invalid_mass_too_large(self):
        """Test that mass exceeding maximum raises ValueError."""
        with pytest.raises(ValueError):
            RocketConfig(mass=2e6)  # Exceeds max
    
    def test_invalid_thrust_negative(self):
        """Test that negative thrust raises ValueError."""
        with pytest.raises(ValueError):
            RocketConfig(thrust=-100000)
    
    def test_invalid_burn_time_negative(self):
        """Test that negative burn time raises ValueError."""
        with pytest.raises(ValueError):
            RocketConfig(burn_time=-10)
    
    def test_invalid_drag_coefficient(self):
        """Test that invalid drag coefficient raises ValueError."""
        with pytest.raises(ValueError):
            RocketConfig(drag_coefficient=-0.5)


class TestSimulationState:
    """Test SimulationState class."""
    
    def test_initial_state(self):
        """Test initial simulation state."""
        state = SimulationState()
        assert state.time == 0.0
        assert state.altitude == 0.0
        assert state.velocity == 0.0
        assert state.acceleration == 0.0
        assert state.is_burning is True
    
    def test_has_landed_true(self):
        """Test has_landed detection."""
        state = SimulationState(altitude=0.0, velocity=0.05)
        assert state.has_landed() is True
    
    def test_has_landed_false_altitude(self):
        """Test has_landed returns False when above ground."""
        state = SimulationState(altitude=100.0, velocity=10.0)
        assert state.has_landed() is False
    
    def test_has_landed_false_velocity(self):
        """Test has_landed returns False when moving too fast."""
        state = SimulationState(altitude=0.0, velocity=5.0)
        assert state.has_landed() is False


class TestRocketSimulation:
    """Test RocketSimulation engine."""
    
    def test_basic_simulation(self):
        """Test basic rocket simulation runs successfully."""
        config = RocketConfig(mass=1000, thrust=500000, burn_time=30, drag_coefficient=0.5)
        sim = RocketSimulation(config)
        times, altitudes, velocities = sim.simulate(total_time=100, dt=0.1)
        
        assert len(times) > 0
        assert len(altitudes) > 0
        assert len(velocities) > 0
        assert max(altitudes) > 0  # Rocket should reach altitude
    
    def test_simulation_history(self):
        """Test that simulation history is recorded correctly."""
        config = RocketConfig()
        sim = RocketSimulation(config)
        sim.simulate(total_time=10, dt=1.0)
        
        assert len(sim.history["times"]) == len(sim.history["altitudes"])
        assert len(sim.history["times"]) == len(sim.history["velocities"])
        assert len(sim.history["times"]) == len(sim.history["accelerations"])
    
    def test_zero_thrust(self):
        """Test simulation with zero thrust (free fall)."""
        config = RocketConfig(mass=1000, thrust=0, drag_coefficient=0.01)
        sim = RocketSimulation(config)
        sim.step(1.0)
        
        # Rocket should have downward acceleration
        assert sim.state.acceleration < 0
        # Velocity should become negative (falling)
        assert sim.state.velocity < 0
    
    def test_max_altitude_calculation(self):
        """Test max altitude calculation."""
        config = RocketConfig()
        sim = RocketSimulation(config)
        sim.simulate(total_time=100, dt=0.1)
        
        max_alt = sim.get_max_altitude()
        assert max_alt == max(sim.history["altitudes"])
        assert max_alt > 0
    
    def test_max_velocity_calculation(self):
        """Test max velocity calculation."""
        config = RocketConfig()
        sim = RocketSimulation(config)
        sim.simulate(total_time=100, dt=0.1)
        
        max_vel = sim.get_max_velocity()
        assert max_vel >= 0
    
    def test_simulation_statistics(self):
        """Test statistics retrieval."""
        config = RocketConfig()
        sim = RocketSimulation(config)
        sim.simulate(total_time=50, dt=1.0)
        
        stats = sim.get_statistics()
        assert "max_altitude" in stats
        assert "max_velocity" in stats
        assert "flight_time" in stats
        assert stats["max_altitude"] > 0
    
    def test_reset_simulation(self):
        """Test simulation reset."""
        config = RocketConfig()
        sim = RocketSimulation(config)
        sim.simulate(total_time=10, dt=1.0)
        
        assert len(sim.history["times"]) > 0
        sim.reset()
        assert len(sim.history["times"]) == 0
        assert sim.state.altitude == 0.0
    
    def test_invalid_time_step(self):
        """Test that invalid time step raises ValueError."""
        config = RocketConfig()
        sim = RocketSimulation(config)
        
        with pytest.raises(ValueError):
            sim.step(0)
        
        with pytest.raises(ValueError):
            sim.step(-1.0)
    
    def test_forces_calculation(self):
        """Test force calculations during flight."""
        config = RocketConfig(mass=1000, thrust=20000, drag_coefficient=0)
        sim = RocketSimulation(config)
        
        thrust, weight, drag, net_force = sim._calculate_forces()
        
        assert thrust == 20000
        assert weight == 1000 * GRAVITY
        assert drag == 0
        assert net_force == thrust - weight - drag
    
    def test_drag_increases_with_velocity(self):
        """Test that drag force increases with velocity."""
        config = RocketConfig(drag_coefficient=0.5)
        sim = RocketSimulation(config)
        
        # Low velocity
        sim.state.velocity = 10
        _, _, drag_low, _ = sim._calculate_forces()
        
        # High velocity
        sim.state.velocity = 100
        _, _, drag_high, _ = sim._calculate_forces()
        
        assert drag_high > drag_low
    
    def test_thrust_stops_after_burn_time(self):
        """Test that thrust stops after burn time."""
        config = RocketConfig(burn_time=10)
        sim = RocketSimulation(config)
        
        # During burn
        sim.state.time = 5
        thrust1, _, _, _ = sim._calculate_forces()
        assert thrust1 > 0
        
        # After burn
        sim.state.time = 15
        thrust2, _, _, _ = sim._calculate_forces()
        assert thrust2 == 0


class TestSensitivityAnalysis:
    """Test SensitivityAnalysis class."""
    
    def test_vary_parameter_mass(self):
        """Test varying mass parameter."""
        base_config = RocketConfig(mass=1000, thrust=500000)
        analyzer = SensitivityAnalysis(base_config)
        
        new_config = analyzer.vary_parameter("mass", 2000)
        assert new_config.mass == 2000
        assert new_config.thrust == 500000  # Other params unchanged
    
    def test_vary_parameter_thrust(self):
        """Test varying thrust parameter."""
        base_config = RocketConfig(thrust=500000)
        analyzer = SensitivityAnalysis(base_config)
        
        new_config = analyzer.vary_parameter("thrust", 600000)
        assert new_config.thrust == 600000
    
    def test_invalid_parameter(self):
        """Test that invalid parameter name raises ValueError."""
        base_config = RocketConfig()
        analyzer = SensitivityAnalysis(base_config)
        
        with pytest.raises(ValueError):
            analyzer.vary_parameter("invalid_param", 100)
    
    def test_sensitivity_analysis_thrust(self):
        """Test sensitivity analysis on thrust."""
        base_config = RocketConfig(mass=1000, thrust=500000, burn_time=30)
        analyzer = SensitivityAnalysis(base_config)
        
        results = analyzer.run_analysis(
            "thrust",
            [400000, 500000, 600000],
            total_time=50,
            dt=1.0
        )
        
        assert "values" in results
        assert "max_altitudes" in results
        assert len(results["values"]) == 3
        # Higher thrust should give higher altitude
        assert results["max_altitudes"][-1] > results["max_altitudes"][0]
    
    def test_sensitivity_analysis_mass(self):
        """Test sensitivity analysis on mass."""
        base_config = RocketConfig()
        analyzer = SensitivityAnalysis(base_config)
        
        results = analyzer.run_analysis(
            "mass",
            [800, 1000, 1200],
            total_time=50,
            dt=1.0
        )
        
        assert len(results["values"]) == 3
        # Higher mass should give lower altitude
        assert results["max_altitudes"][0] > results["max_altitudes"][-1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
