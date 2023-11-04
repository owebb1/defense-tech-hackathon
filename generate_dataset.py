import numpy as np
import pandas as pd
import pickle


def generate_wave(boat_type, t, steady_state_params, boat_wake_params, noise_level=0.1):
    # Steady state wave
    steady_wave = steady_state_params['A'] * np.sin(
        2 * np.pi * steady_state_params['f'] * t + steady_state_params['phi'])

    # Add Gaussian noise to the steady state wave
    noise = np.random.normal(0, noise_level, size=t.shape)
    steady_wave += noise

    # Boat wave (if boat_type is not None, otherwise steady state continues)
    if boat_type:
        boat_wave = boat_wake_params[boat_type]['A'] * np.sin(
            2 * np.pi * boat_wake_params[boat_type]['f'] * t + boat_wake_params[boat_type]['phi'])
        # Add the boat wave to the steady state wave for the duration of the boat passing
        wave_duration = int(10 * fs)  # 10 seconds boat wave duration
        start = np.random.randint(0, len(t) - wave_duration)
        boat_wave_segment = boat_wave[start:start+wave_duration] + \
            np.random.normal(0, noise_level, size=wave_duration)
        steady_wave[start:start+wave_duration] += boat_wave_segment

    return steady_wave


def create_dataset(num_samples, fs, t_max, boat_wake_probability=0.1):
    """Create a dataset with a steady state signal and intermittent boat wake signals."""
    t = np.arange(0, t_max, 1/fs)  # Time vector
    # Example steady state parameters
    steady_state_params = {'A': 8, 'f': 111, 'phi': 0}

    # Generate the steady state and boat wake data
    data = []
    for _ in range(num_samples):
        # Decide whether to insert a boat wave in this sample
        if np.random.rand() < boat_wake_probability:
            boat_type = np.random.choice(list(boat_wake_params.keys()))
        else:
            boat_type = None

        wave = generate_wave(
            boat_type, t, steady_state_params, boat_wake_params)
        data.append(wave)

    return np.array(data)


# Define the boat types and their parameters for the wakes
boat_wake_params = {
    'Destroyer': {'A': 14, 'f': 90, 'phi': 0},
    'Battleship': {'A': 12, 'f': 95, 'phi': 0},
    'Carrier': {'A': 16, 'f': 100, 'phi': 0},
    'Cruiser': {'A': 10, 'f': 85, 'phi': 0}
}

fs = 1000  # Sample rate in Hz
t_max = 1000  # Maximum time in seconds

# Generate the dataset
num_samples = 100  # Number of samples to generate
dataset = create_dataset(num_samples, fs, t_max)

# Use pickle to save the dataset to a file
with open('boat_dataset.pkl', 'wb') as file:
    pickle.dump(dataset, file)

# Optionally, to load the dataset back:
# with open('boat_dataset.pkl', 'rb') as file:
#     loaded_dataset = pickle.load(file)

# Example: Verify the shape of the loaded dataset
# print(loaded_dataset.shape)
