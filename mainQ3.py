#Question3

#3a
import numpy as np
import matplotlib.pyplot as plt

emg_signal = np.load('f.npy')

#our emg signal is 1024 hz
emg_frequency = 1024
length_signal=len(emg_signal[0]) #get the length of the signal
emg_time = np.arange(length_signal)/emg_frequency #creats a time vector/array
print(len(emg_time))
interference_f= 50
print (length_signal)
#y(t)=Asin(ωt+φ)=Asin(2πft+φ)
#our interference wave
interference = 0.15*np.sin(2*np.pi*interference_f*emg_time)
emg_interference = emg_signal[0] + interference


plt.figure(figsize=(10, 6))
plt.plot(emg_time, emg_interference, label="EMG with 50 Hz Interference", color='red', alpha=0.7)
plt.plot(emg_time, emg_signal[0], label="Interference-Free EMG", color='blue', alpha=0.7)

plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.title('EMG Signal with and without 50 Hz Power Line Interference')
plt.legend()  # Only call legend once
plt.show()
print("done")

#3c
emg_fft = np.fft.fft(emg_signal[0])
emg_interference_ftt = np.fft.fft(emg_interference)
# 1/emg_frequency since we want sampling period, the distance between samples
#fft.fftfreq(n, d=1.0, device=None)
frequencies = np.fft.fftfreq(len(emg_signal[0]), 1/emg_frequency)


plt.figure(figsize=(10, 6))
plt.plot(frequencies[:len(frequencies)//2], np.abs(emg_interference_ftt)[:len(emg_fft)//2], color = 'red')  # Plot only positive frequencies
plt.plot(frequencies[:len(frequencies)//2], np.abs(emg_fft)[:len(emg_fft)//2], color = 'blue')
plt.title('Magnitude Spectrum of EMG Signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (A.U)')
plt.grid()
plt.show()