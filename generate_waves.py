import numpy as np
import matplotlib.pyplot as plt

# Sample rate and time vector
fs = 1000  # Sample rate in Hz
t = np.arange(0, 40, 1/fs)  # Time vector for 10 seconds

# Sine wave parameters
A1, A2, A3, A4 = 0.5, 0.5, 0.5, 1  # Amplitudes
f1, f2, f3, f4 = 1, 1, 1, 1  # Frequencies in Hz
p1, p2, p3, p4 = -0.226*np.pi, np.pi, np.pi * \
    0.226, np.pi  # Phase shifts in radians

# Generate the sine waves
wave1_accel1 = A1 * np.sin(2 * np.pi * f1 * t + p1)
wave1_accel2 = A2 * np.sin(2 * np.pi * f2 * t + p2)
wave1_accel3 = A3 * np.sin(2 * np.pi * f3 * t + p3)
wave1_accel4 = wave1_accel2


f1, f2, f3, f4 = 0.5, 0.5, 0.5, 0.5  # Frequencies in Hz
p1, p2, p3, p4 = np.pi, -0.226*np.pi, np.pi, np.pi * \
    0.226  # Phase shifts in radians
# wave2_accel1 = A1 * np.sin(2 * np.pi * f1 * t + p1)
# wave2_accel2 = A2 * np.sin(2 * np.pi * f2 * t + p2)
# wave2_accel3 = wave2_accel1
# wave2_accel4 = A4 * np.sin(2 * np.pi * f4 * t + p4)


# def wake_amplitude(boat_length, coefficient=1, exponent=1):
#     """
#     Calculate the amplitude of the wake wave based on the length of the boat.

#     :param boat_length: Length of the boat (assumed to be a proxy for size)
#     :param coefficient: Empirical coefficient that relates boat size to wave amplitude
#     :param exponent: The power to which the boat length is raised
#     :return: Amplitude of the wake wave
#     """
#     return coefficient * (boat_length ** exponent)


# # Example usage:
# boat_length = 10  # Length of the boat in meters
# A = wake_amplitude(boat_length)
# print(f"The amplitude of the wake wave is approximately {A} meters.")


A = 1      # Amplitude
alpha = 0.1  # Decay factor
f = 0.5     # Frequency (Hz)
lambda_ = 2  # Wavelength (m)
c = lambda_ * f  # Wave speed = wavelength * frequency
x0 = 0      # Initial position (m)
phi = -2 * np.pi * x0 / lambda_
wave_full1 = A1 * np.sin(2 * np.pi * f1 * t + p1)
wave_full2 = A2 * np.sin(2 * np.pi * f2 * t + p2)
wave_full4 = A4 * np.sin(2 * np.pi * f4 * t + p4)
wake_wave_1 = A * np.exp(-alpha * c * t) * np.sin(2 * np.pi * f * t + phi)
wake_wave_2 = A * np.exp(-alpha * c * t) * \
    np.sin(2 * np.pi * f * t + -0.226*phi)
wake_wave_4 = A * np.exp(-alpha * c * t) * \
    np.sin(2 * np.pi * f * t + 0.226*phi)

# Apply piecewise condition
wave2_accel1 = np.where((t >= 7) & (t < 40), wake_wave_1, 0)
wave2_accel2 = np.where((t >= 7) & (t < 40), wake_wave_2, 0)
wave2_accel3 = wave2_accel1
wave2_accel4 = np.where((t >= 7) & (t < 40), wake_wave_4, 0)
# wave2_accel2 = np.where((t >= 3) & (t < 8), wave_full2, 0)
# wave2_accel3 = wave2_accel1  # Duplicate of wave2_accel1 as per your definition
# wave2_accel4 = np.where((t >= 3) & (t < 8), wave_full4, 0)


accel1 = wave1_accel1 + wave2_accel1
accel2 = wave1_accel2 + wave2_accel2
accel3 = wave1_accel3 + wave2_accel3
accel4 = wave1_accel4 + wave2_accel4
# Initialize figure and axes grid
fig, axs = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=True)

# Flatten the array of axes for easy indexing
axs = axs.flatten()

# Plot each accelerometer data in a different subplot
axs[0].plot(t, accel1, label='Accel 1')
axs[1].plot(t, accel2, label='Accel 2')
axs[2].plot(t, accel3, label='Accel 3')
axs[3].plot(t, accel4, label='Accel 4')

# Adding titles, labels, and legends for each subplot
for i, ax in enumerate(axs):
    ax.set_title(f'Quadrant {i+1}')
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Amplitude')
    ax.legend()
    ax.grid(True)

# Adjust layout to prevent overlapping
plt.tight_layout()

# Display the plot
plt.show()
