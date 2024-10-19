import numpy as np
from scipy.fft import fft
import matplotlib.pyplot as plt

def cart2pol(x, y):
    # Converts cartesian coordinates to polar coordinates
    theta = np.arctan2(y, x)
    rho = np.sqrt(x**2 + y**2)
    return [theta, rho]

# Add 50 Hz power line interference 
def powerline_interference(signal, fs, f_interference=50, amplitude=0.15):
    t = np.arange(len(signal)) / fs 
    interference = amplitude * np.sin(2 * np.pi * f_interference * t)
    return signal + interference # Return modified signal

def main():
    # Load f.npy
    f_signal = np.load('f.npy').flatten()
    
    # Variables
    fs = 1024  
    T = 1 / fs  
    N = len(f_signal)  # N samples
    T0 = N * T  # Total time
    t = np.arange(N) * T  
    
    # a) 50Hz power line interference 
    corrupted_signal = powerline_interference(f_signal, fs, amplitude=0.15)
    
    # Plot
    plt.figure()
    plt.plot(t, corrupted_signal, label="Corrupted Signal", color='red', linestyle='dashed', linewidth=0.75)
    plt.plot(t, f_signal, label="Original Signal", color='blue', linewidth=0.75)
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude [a.u.]')
    plt.legend()
    plt.xlim(t[0], t[-1])
    plt.grid(True)
    plt.show()

    # Perform FFT on both signals
    fft_original = fft(f_signal)
    fft_corrupted = fft(corrupted_signal)

    # Compute magnitude and phase for both signals
    [Fm_orig] = cart2pol(fft_original.real, fft_original.imag)
    [Fm_corr] = cart2pol(fft_corrupted.real, fft_corrupted.imag)

    # Frequency axis
    k = np.arange(0, N, step=1)
    f_axis = k / T0  # Frequency
    half_f_axis = f_axis[:N//2]  # Only positive frequencies

    # c) Plot the magnitude of the DFTs for comparison
    plt.figure()
    plt.plot(half_f_axis, Fm_corr[:N//2], label="Corrupted Signal", color='red', linestyle='dashed', linewidth=0.75)
    plt.plot(half_f_axis, Fm_orig[:N//2], label="Original Signal", color='blue', linewidth=0.75)
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Magnitude / Phase [A.U.]')
    plt.xlim(0, 512)  
    plt.legend()
    plt.grid(True)
    plt.show()



   
if __name__ == '__main__':
    main()
