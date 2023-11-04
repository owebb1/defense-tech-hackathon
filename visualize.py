import pickle
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset from the .pkl file
with open('boat_dataset.pkl', 'rb') as file:
    dataset = pickle.load(file)

fs = 1000  # Sample rate in Hz
# Time vector, assuming fs is unchanged
t = np.arange(0, len(dataset[0]) / fs, 1/fs)

# Plotting settings
plt.figure(figsize=(15, 8))

# Plot the first few waveforms
num_waveforms_to_plot = 5  # Adjust this to plot the desired number of waveforms
for i in range(num_waveforms_to_plot):
    plt.plot(t, dataset[i], label=f'Sample {i+1}')

plt.title('Boat Wake Signals')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()
plt.show()
