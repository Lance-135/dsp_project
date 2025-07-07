import numpy as np

def freq_filter(signal, fs, low=None, high=None):
    N = len(signal)
    freqs = np.fft.rfftfreq(N, 1/fs)
    spectrum = np.fft.rfft(signal)
    mask = np.ones_like(spectrum, dtype=bool)
    if low is not None:
        mask &= freqs >= low
    if high is not None:
        mask &= freqs <= high
    filtered_spectrum = spectrum * mask
    return np.fft.irfft(filtered_spectrum, n=N) 