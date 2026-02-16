import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Integration parameters
u_tilde_values = [1, 2, 3, 4, 5]
u_0_min = 0.1
u_0_max = 10
steps = 100

# Define integrands with safety checks
def energy_integrand(y, i, u_tilde):
    try:
        base = i**2 * y**2 + u_tilde**2
        num = base**2 / (i**2 + u_tilde**2)
        denom_squared = (base**4 / (i**2 + u_tilde**2)**2) - base**2
        if denom_squared <= 0:
            return 0
        return (i / (2 * np.pi)) * num / np.sqrt(denom_squared)
    except:
        return 0

def length_integrand(y, i, u_tilde):
    try:
        base = i**2 * y**2 + u_tilde**2
        denom_squared = (base**4 / (i**2 + u_tilde**2)**2) - base**2
        if denom_squared <= 0:
            return 0
        return i / np.sqrt(denom_squared)
    except:
        return 0

color = ["red","green","blue","orange", "black"]
n=0

# --- Plot 1: Energy vs. L ---
plt.figure(figsize=(10, 7))
for u_tilde in u_tilde_values:
    e_list = []
    l_list = []
    u_0_values = np.linspace(u_0_min, u_0_max, steps)

    for i in u_0_values:
        f = lambda y: energy_integrand(y, i, u_tilde)
        g = lambda y: length_integrand(y, i, u_tilde)

        E, _ = quad(f, 1, np.inf, limit=1000)
        L, _ = quad(g, 1, np.inf, limit=1000)

        if np.isfinite(E) and np.isfinite(L) and L > 0:
            e_list.append(E)
            l_list.append(L)

    plt.plot(l_list, e_list, color=color[n], marker='o', linestyle='-', label=f'$\\tilde{{U}}$ = {u_tilde}')
    n = n+1

plt.xlabel("L")
plt.ylabel("Energy")
plt.title("Energy vs. L for varying $\\tilde{U}$")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

n=0
# --- Plot 2: E/L vs. L ---
plt.figure(figsize=(10, 7))
for u_tilde in u_tilde_values:
    el_list = []
    l_list = []
    u_0_values = np.linspace(u_0_min, u_0_max, steps)

    for i in u_0_values:
        f = lambda y: energy_integrand(y, i, u_tilde)
        g = lambda y: length_integrand(y, i, u_tilde)

        E, _ = quad(f, 1, np.inf, limit=5000)
        L, _ = quad(g, 1, np.inf, limit=5000)

        if np.isfinite(E) and np.isfinite(L) and L > 0:
            el_list.append(E / L)
            l_list.append(L)

    plt.plot(l_list, el_list, marker='x', linestyle='--', color=color[n], label=f'$\\tilde{{U}}$ = {u_tilde}')
    n = n+1


n = 0
for u_tilde in u_tilde_values:
    asymptote = u_tilde**2 / (2 * np.pi)
    plt.axhline(y=asymptote, linestyle='-', color=color[n], label=f'$\\tilde{{U}}^2/2\\pi$ ({u_tilde})')
    n = n+1
    

plt.xlabel("L")
plt.ylabel("E / L")
plt.title("E/L vs. L (with asymptotes) for varying $\\tilde{U}$")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

