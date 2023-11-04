import numpy as np
import matplotlib.pyplot as plt

# Define parameters for the wake wave equation
A = 1       # Initial amplitude of the wake wave
alpha = 0.1  # Decay factor
f = 0.5     # Frequency of the wake waves (Hz)
lambda_ = 2  # Wavelength of the wake waves (m)
x_max = 20  # Maximum distance to simulate (m)
t = 0       # Time at which the wave is evaluated (seconds)

# Space vector (representing distance behind the boat)
x = np.linspace(0, x_max, 1000)

# Wake wave equation
wake_wave = A * np.exp(-alpha * x) * np.sin(2 * np.pi * (f * t - x / lambda_))

# Plotting the wake wave
plt.figure(figsize=(14, 5))
plt.plot(x, wake_wave, label='Wake Wave at t={}'.format(t))
plt.title('Wake Wave Profile')
plt.xlabel('Distance behind the boat (m)')
plt.ylabel('Wave Amplitude')
plt.legend()
plt.grid(True)
plt.show()
