import numpy as np

def spectral_subtraction(signal, noise_est, fs):
    N = len(signal)
    S = np.fft.rfft(signal)
    N_est = np.fft.rfft(noise_est)
    S_mag = np.abs(S)
    N_mag = np.abs(N_est)
    S_phase = np.angle(S)
    clean_mag = np.maximum(S_mag - N_mag, 0)
    clean_S = clean_mag * np.exp(1j * S_phase)
    return np.fft.irfft(clean_S, n=N) 