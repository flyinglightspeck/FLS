import numpy as np
import matplotlib.pyplot as plt

def heartbeat_brightness(t, A=1, T=.9, tau1=0.1, tau2=.3, sigma=0.05):
    t_mod = t % T  # Loop the function every T seconds
    return A * (np.exp(-((t_mod - tau1) ** 2) / sigma**2) +
                0.5 * np.exp(-((t_mod - tau2) ** 2) / sigma**2))

# Time axis for visualization
t_values = np.linspace(0, 2.6, 300)  # Simulating 3 seconds
brightness_values = [heartbeat_brightness(t) for t in t_values]

# Plot the heartbeat brightness pattern
plt.plot(t_values, brightness_values)
plt.xlabel("Time (s)")
plt.ylabel("Brightness")
plt.title("Heartbeat LED Brightness Pattern")
plt.show()