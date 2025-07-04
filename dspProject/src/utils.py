import numpy as np
import matplotlib.pyplot as plt

def generate_noisy_signal(length=2048, fs=500, freq=5, noise_level=0.5):
    t = np.arange(length) / fs
    clean = np.sin(2 * np.pi * freq * t)
    noise = noise_level * np.random.randn(length)
    return clean + noise, clean, noise

def calculate_snr(clean, noisy):
    signal_power = np.mean(clean ** 2)
    noise_power = np.mean((noisy - clean) ** 2)
    return 10 * np.log10(signal_power / noise_power)

def plot_signals(signals, labels, fs, title=None):
    t = np.arange(len(signals[0])) / fs
    for sig, label in zip(signals, labels):
        plt.plot(t, sig, label=label)
    plt.xlabel('Time [s]')
    plt.legend()
    if title:
        plt.title(title)
    plt.show() 