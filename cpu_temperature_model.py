"""
CPU Temperature Model - CST-305 Project 1
Programmers: Thi Nguyen, Komal Khan
Packages: numpy, scipy.integrate.odeint, matplotlib.pyplot
Approach: First-order linear ODE solved with odeint

Models CPU temperature changes based on power consumption and cooling.

The ODE: dT/dt = (1/C)[P(t) - k(T - T_env)]
- dT/dt = rate of temperature change
- P(t) = power/heat generated
- k(T - T_env) = heat escaping
- C = heat capacity

See EXPLANATION.md for full details.
"""

# Import libraries
import numpy as np
from scipy.integrate import odeint  # Solves ODEs
import matplotlib.pyplot as plt


# Physical parameters
C = 50          # Heat capacity (J/°C)
k = 5           # Thermal conductivity (W/°C)
T_env = 25      # Room temperature (°C)
T0 = 25         # Initial CPU temperature (°C)


# Power scenarios
def power_idle(t):
    """Constant low power (10W) - CPU idle"""
    return 10


def power_step(t):
    """Step load: 10W → 80W at t=5s"""
    return 10 if t < 5 else 80


def power_periodic(t):
    """Periodic workload: oscillates 10-80W"""
    omega = 2 * np.pi / 20  # Period = 20 seconds
    return 45 + 35 * np.sin(omega * t)


def cpu_ode(T, t, power_func):
    """
    ODE function: calculates dT/dt
    
    dT/dt = (1/C)[P(t) - k(T - T_env)]
    
    Note: odeint needs parameters in order (T, t, *args)
    """
    P = power_func(t)                # Heat in
    heat_loss = k * (T - T_env)      # Heat out
    dT_dt = (P - heat_loss) / C      # Rate of change
    return dT_dt


def analytical_solution(t, T0, P_const):
    """
    Exact solution for constant power (for validation)
    
    T(t) = T_steady + (T0 - T_steady) * exp(-t/τ)
    """
    tau = C / k
    T_steady = T_env + P_const / k
    T = T_steady + (T0 - T_steady) * np.exp(-t / tau)
    return T


def solve_scenario(power_func, t_span=(0, 60), label=""):
    """
    Solve ODE using odeint
    
    Returns time and temperature arrays
    """
    t = np.linspace(t_span[0], t_span[1], 500)  # 500 time points
    T = odeint(cpu_ode, T0, t, args=(power_func,))  # Solve ODE
    T = T.flatten()  # Convert to 1D array
    return t, T



def plot_results():
    """Generate 4-panel visualization"""
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('CPU Temperature Dynamics - CST-305 Project 1', fontsize=16, fontweight='bold')
    
    # Plot 1: Idle with validation
    ax1 = axes[0, 0]
    t_idle, T_numerical = solve_scenario(power_idle, label="Idle")
    T_analytical = analytical_solution(t_idle, T0, power_idle(0))
    
    ax1.plot(t_idle, T_numerical, 'b-', linewidth=2, label='Numerical (odeint)')
    ax1.plot(t_idle, T_analytical, 'r--', linewidth=2, label='Analytical (exact)')
    ax1.axhline(y=T_env, color='gray', linestyle=':', alpha=0.7, label='Ambient')
    ax1.set_xlabel('Time (s)', fontsize=11)
    ax1.set_ylabel('Temperature (°C)', fontsize=11)
    ax1.set_title('Idle Load (P = 10 W)', fontsize=12, fontweight='bold')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Step load
    ax2 = axes[0, 1]
    t_step, T_step = solve_scenario(power_step, label="Step Load")
    P_step = np.array([power_step(t) for t in t_step])
    
    ax2_power = ax2.twinx()
    ax2.plot(t_step, T_step, 'b-', linewidth=2, label='Temperature')
    ax2_power.plot(t_step, P_step, 'r--', linewidth=2, alpha=0.7, label='Power')
    ax2.axhline(y=T_env, color='gray', linestyle=':', alpha=0.7)
    ax2.set_xlabel('Time (s)', fontsize=11)
    ax2.set_ylabel('Temperature (°C)', fontsize=11, color='b')
    ax2_power.set_ylabel('Power (W)', fontsize=11, color='r')
    ax2.set_title('Step Load (10 W → 80 W at t=5s)', fontsize=12, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor='b')
    ax2_power.tick_params(axis='y', labelcolor='r')
    ax2.grid(True, alpha=0.3)
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_power.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='best')
    
    # Plot 3: Periodic load
    ax3 = axes[1, 0]
    t_periodic, T_periodic = solve_scenario(power_periodic, label="Periodic Load")
    P_periodic = np.array([power_periodic(t) for t in t_periodic])
    
    ax3_power = ax3.twinx()
    ax3.plot(t_periodic, T_periodic, 'b-', linewidth=2, label='Temperature')
    ax3_power.plot(t_periodic, P_periodic, 'r--', linewidth=1.5, alpha=0.7, label='Power')
    ax3.axhline(y=T_env, color='gray', linestyle=':', alpha=0.7)
    ax3.set_xlabel('Time (s)', fontsize=11)
    ax3.set_ylabel('Temperature (°C)', fontsize=11, color='b')
    ax3_power.set_ylabel('Power (W)', fontsize=11, color='r')
    ax3.set_title('Periodic Load (45 + 35·sin(ωt) W)', fontsize=12, fontweight='bold')
    ax3.tick_params(axis='y', labelcolor='b')
    ax3_power.tick_params(axis='y', labelcolor='r')
    ax3.grid(True, alpha=0.3)
    lines1, labels1 = ax3.get_legend_handles_labels()
    lines2, labels2 = ax3_power.get_legend_handles_labels()
    ax3.legend(lines1 + lines2, labels1 + labels2, loc='best')
    
    # Plot 4: Comparison
    ax4 = axes[1, 1]
    ax4.plot(t_idle, T_numerical, 'g-', linewidth=2, label='Idle (10 W)')
    ax4.plot(t_step, T_step, 'b-', linewidth=2, label='Step Load')
    ax4.plot(t_periodic, T_periodic, 'r-', linewidth=2, label='Periodic Load')
    ax4.axhline(y=T_env, color='gray', linestyle=':', alpha=0.7, label='Ambient')
    ax4.set_xlabel('Time (s)', fontsize=11)
    ax4.set_ylabel('Temperature (°C)', fontsize=11)
    ax4.set_title('Comparison of All Scenarios', fontsize=12, fontweight='bold')
    ax4.legend(loc='best')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('cpu_temperature_results.png', dpi=300, bbox_inches='tight')
    print("✓ Plot saved as 'cpu_temperature_results.png'")
    plt.show()


def print_analysis():
    """Print key results and insights"""
    tau = C / k
    T_steady_idle = T_env + power_idle(0) / k
    T_steady_load = T_env + 80 / k
    
    print("\n" + "="*60)
    print("CPU TEMPERATURE MODEL ANALYSIS")
    print("="*60)
    print(f"\nPhysical Parameters:")
    print(f"  Heat capacity (C):         {C} J/°C")
    print(f"  Thermal conductivity (k):  {k} W/°C")
    print(f"  Ambient temperature:       {T_env} °C")
    print(f"  Initial temperature:       {T0} °C")
    
    print(f"\nSystem Characteristics:")
    print(f"  Time constant (τ = C/k):   {tau:.1f} seconds")
    print(f"  63% response time:         {tau:.1f} seconds")
    print(f"  95% response time:         {3*tau:.1f} seconds")
    print(f"  99% response time:         {5*tau:.1f} seconds")
    
    print(f"\nSteady-State Temperatures:")
    print(f"  Idle (10 W):               {T_steady_idle:.1f} °C")
    print(f"  Full Load (80 W):          {T_steady_load:.1f} °C")
    print(f"  Temperature rise at load:  {T_steady_load - T_env:.1f} °C")
    
    print(f"\nKey Insights:")
    print(f"  • System reaches steady state in ~{int(5*tau)} seconds")
    print(f"  • Each additional watt increases steady temp by {1/k:.2f} °C")
    print(f"  • Larger heat capacity → slower temperature changes")
    print(f"  • Higher conductivity → better cooling efficiency")
    print("="*60 + "\n")


def main():
    """Main function - runs simulation and generates plots"""
    print("\n" + "="*60)
    print("CPU TEMPERATURE MODEL - CST-305 PROJECT 1")
    print("First-Order Linear ODE Simulation using odeint")
    print("="*60 + "\n")
    
    print("Running simulations...")
    print_analysis()
    
    print("Generating plots...")
    plot_results()
    
    print("\n✓ Simulation complete!")
    print("Check 'cpu_temperature_results.png' for visualizations.\n")


if __name__ == "__main__":
    main()
