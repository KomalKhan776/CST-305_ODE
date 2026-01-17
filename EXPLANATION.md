# CPU Temperature Model - Detailed Explanation

**Project:** CST-305 Project 1 - Visualize ODE With SciPy  
**Programmers:** Thi Nguyen, Komal Khan

---

## Overview

This program simulates how a CPU heats up and cools down using differential equations.

**What it simulates (60 seconds):**
1. **Idle** - Low power (10W)
2. **Step Load** - Sudden jump from 10W to 80W at t=5s
3. **Periodic** - Oscillating workload (sine wave pattern)

**Files:**
- `cpu_temperature_model.py` - Main program
- `requirements.txt` - Dependencies (numpy, scipy, matplotlib)
- `EXPLANATION.md` - This file
- `README.md` - Installation instructions

---

## The Problem

CPUs generate heat. Too much heat causes:
- Slower performance (CPU throttles to protect itself)
- Hardware damage
- System crashes

**Question we answer:** How does temperature change over time under different workloads?

---
## The Math

### The ODE (Ordinary Differential Equation)

```
dT/dt = (1/C)[P(t) - k(T - T_env)]
```

**What each part means:**
- **T** = CPU temperature (°C)
- **dT/dt** = How fast temperature changes (°C/second)
- **P(t)** = Power/heat from CPU (Watts)
- **k** = How fast heat escapes (W/°C)
- **C** = Heat capacity - resistance to temperature change (J/°C)
- **T_env** = Room temperature (°C)

### Simple Explanation

Think of a bathtub:
- **Faucet (P)** = Heat coming in
- **Drain (k×ΔT)** = Heat leaving
- **Water level (T)** = Temperature
- **Tub size (C)** = How much heat needed to change temperature

**The equation says:** Temperature change = (Heat in - Heat out) / Heat capacity

### Exact Solution (When Power is Constant)

```
T(t) = T_env + (P/k) + [T0 - T_env - (P/k)] × e^(-t/τ)
```

Where **τ = C/k** (time constant)

**What this means:** Temperature approaches a final value exponentially. After time τ, you're 63% of the way there.

---

## Example Calculation

**Given:** T=30°C, P=80W, C=50, k=5, T_env=25°C

**Find:** How fast is temperature changing?

```
Step 1: Heat loss = k × (T - T_env) = 5 × (30-25) = 25W
Step 2: Net heat = P - heat_loss = 80 - 25 = 55W
Step 3: dT/dt = 55 / 50 = 1.1 °C/second
```

**Answer:** Temperature rising at 1.1°C per second.

**In code:**
```python
def cpu_ode(T, t, power_func):
    P = power_func(t)
    heat_loss = k * (T - T_env)
    dT_dt = (P - heat_loss) / C
    return dT_dt
```

---

## How It Works

### Algorithm

1. Set parameters (C=50, k=5, T_env=25, T0=25)
2. Define power scenarios (idle/step/periodic)
3. Define ODE function (calculates dT/dt)
4. Use `odeint` to solve:
   - Starts at T0
   - Steps forward using dT/dt
   - Returns temperature at each time point
5. Plot results (4 subplots)

### Why Use odeint?

`odeint` is a Python function that solves ODEs automatically:
- Uses smart algorithms (LSODA)
- Adjusts step size for accuracy
- Much better than manual methods

**Usage:** `odeint(ode_function, initial_value, time_array, args=(extra_params,))`

---

## Results

### Parameters Used
- C = 50 J/°C
- k = 5 W/°C  
- τ = 10 seconds (time constant)

### Final Temperatures
- **Idle (10W)**: 27°C
- **Load (80W)**: 41°C
- **Each watt adds**: 0.2°C

### Response Times
- After 10s (1τ): 63% there
- After 30s (3τ): 95% there
- After 50s (5τ): 99% there

---

## The Plots

**Plot 1 - Idle with Validation**
* when CPU is basically resting - doing very little or no work 
- Blue = Numerical solution (odeint)
- Red = Exact math solution
- Should overlap perfectly (confirms odeint works)

**Plot 2 - Step Load**
* The CPU suddenly jumps from one activity level to another, like flipping a light switch.
- Temperature jumps when power increases
- Like opening a demanding program

**Plot 3 - Periodic Load**
*The CPU workload goes up and down in a repeating pattern, like waves. 
- Temperature follows power pattern
- Like rendering video frames

**Plot 4 - Comparison**
- All scenarios together
- Shows different behaviors

---

## Code Packages

**NumPy** - Arrays and math functions  
**SciPy** - ODE solver (odeint)  
**Matplotlib** - Plotting and visualization

---

## References

- SciPy docs: https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.odeint.html
- Newton's Law of Cooling
- First-order ODEs (standard differential equations)
