import numpy as np
import matplotlib.pyplot as plt


# Load the action potentials and firing samples
action_potentials = np.load('action_potentials.npy')  # 8x100 matrix
firing_samples = np.load('firing_samples.npy', allow_pickle=True)  # 8 firing vectors


#a time vector
duration = 20  # seconds                                                                    
fs = 10000  # sampling frequency in Hz
total_samples = duration * fs  # total number of samples in the EMG signal
t = np.arange(0, duration, 1/fs)

# Initialize list to store trains
ap_trains = []
binary_vectors= []
# For each motor creat a binary (200,000 samples)
for i in range(8):
    binary_vector = np.zeros(total_samples)
    for firing in firing_samples[0][i]:
        if 0 <= firing < total_samples:
            binary_vector[int(firing)] = 1
    
    # Store the binary vector
    binary_vectors.append(binary_vector)
    
 #Convolve with action potential
 #This operation effectively places the action potential waveform at each firing time, 
 #creating a continuous signal that represents the action potential train.
    ap_train = np.convolve(binary_vector, action_potentials[i], mode='same')
    ap_trains.append(ap_train)



# Choose one of the action potential trains (e.g., the first one)
chosen_train = ap_trains[0]

# Plot the full train
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t, chosen_train, linewidth=0.5)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [A.U.]')
plt.title('Action Potential Train for Motor Unit 1')

# Plot the train in the interval 10-10.5 s
plt.subplot(2, 1, 2)
mask = (t >= 10) & (t <= 10.5)
plt.plot(t[mask], chosen_train[mask], linewidth=0.5)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [A.U.]')
plt.title('Action Potential Train for Motor Unit 1 (10-10.5 s)')

plt.tight_layout()
plt.show()

# Sum the 8 action potential trains
emg_signal = np.sum(ap_trains, axis=0)

# Plot the EMG signal in the interval 10-10.5 s
plt.figure(figsize=(12, 4))
mask = (t >= 10) & (t <= 10.5)
plt.plot(t[mask], emg_signal[mask], linewidth=0.5)
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [A.U.]')
plt.title('EMG Signal (10-10.5 s)')
plt.show()


#___Question 2___

#1a: Create a Hanning window of 10000 points
#filter with hanning
#i second = 10000 points when we have 10000Hz
window =  np.hanning(10000)
hanning_filter=[]

for train in binary_vectors:
    smooth = np.convolve(train, window, mode = 'same')
    hanning_filter.append(smooth)

#2c
#plot the binary and filtered signals for all 8 units
plt.figure(figsize=(12, 4))

for i, signal_filter in enumerate(hanning_filter):
    plt.plot(t, signal_filter, label=f'Unit {i + 1}')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude [A.U.]')
plt.title('Filtered Signals for 8 units')
plt.show()

#2d
#plot the binary and filtered signals for unit 4
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t, binary_vectors[3], label='Binary')
plt.title('Binary Signal - Unit 4')
plt.subplot(2, 1, 2)
plt.plot(t, hanning_filter[3], label='Filtered')
plt.title('Filtered Signal - Unit 4')
plt.xlabel('Time (s)')
plt.tight_layout()
plt.show()

#2e
#plot the binary and filtered signals for unit 4 and 7
plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.plot(t, binary_vectors[3], label='Binary')
plt.plot(t, hanning_filter[3], label='Filtered')
plt.title('Unit 4')
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(t, binary_vectors[6], label='Binary')
plt.plot(t, hanning_filter[6], label='Filtered')
plt.title('Unit 7')
plt.xlabel('Time (s)')
plt.legend()
plt.tight_layout()
plt.show()

