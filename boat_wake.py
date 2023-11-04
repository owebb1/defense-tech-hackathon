import numpy as np
import matplotlib.pyplot as plt

# Constants for the Kelvin wake pattern
kelvin_angle = 19.47  # half angle of the wake in degrees
boat_velocity = 5     # arbitrary boat velocity in m/s (just for illustration)

# Function to calculate the positions of the wake lines


def kelvin_wavefronts(distance, angle_deg, boat_speed):
    angle_rad = np.radians(angle_deg)
    return distance * np.tan(angle_rad), distance / np.cos(angle_rad)


# Create a figure and axis
fig, ax = plt.subplots()

# Generate the wake lines
distance = np.linspace(0, 100, 500)
for side in [-1, 1]:
    transverse_wavefront, divergent_wavefront = kelvin_wavefronts(
        distance, side * kelvin_angle, boat_velocity)

    # Plot the transverse waves (inner part of the V)
    ax.plot(side * transverse_wavefront, -distance, 'b',
            linestyle='--', label='Transverse waves' if side == 1 else "")

    # Plot the divergent waves (arms of the V)
    ax.plot(side * divergent_wavefront, -distance, 'r', linestyle='-',
            label='Divergent waves' if side == 1 else "")

# Add a representation of the boat path
ax.plot([0, 0], [0, -100], 'k', label='Boat path')

# Set the aspect of the plot to be equal
ax.set_aspect('equal')

# Set labels and title
ax.set_xlabel('Width (m)')
ax.set_ylabel('Distance behind boat (m)')
ax.set_title('Simplified Representation of Kelvin Wake Pattern')

# Add legend
ax.legend()

# Show the plot
plt.show()
