import numpy as np
from src.utils import generate_noisy_signal, calculate_snr, plot_signals
from src.filters import apply_fir_filter, apply_iir_filter
from src.freq_filters import freq_filter
from src.adaptive import lms_filter
from src.spectral import spectral_subtraction
from src.wavelet import wavelet_denoise

# Parameters
fs = 500  # Sampling frequency
length = 2048  # Signal length
chunk_size = 256  # Simulate real-time processing

# Generate synthetic noisy signal
noisy, clean, noise = generate_noisy_signal(length=length, fs=fs, freq=5, noise_level=0.7)

# --- Time-domain FIR filtering ---
filt_fir = np.zeros_like(noisy)
for i in range(0, length, chunk_size):
    chunk = noisy[i:i+chunk_size]
    filt_fir[i:i+chunk_size] = apply_fir_filter(chunk, cutoff=10, fs=fs, numtaps=51, pass_type='low')

# --- Frequency-domain filtering ---
filt_freq = np.zeros_like(noisy)
for i in range(0, length, chunk_size):
    chunk = noisy[i:i+chunk_size]
    filt_freq[i:i+chunk_size] = freq_filter(chunk, fs, low=None, high=10)

# --- Adaptive filtering (LMS) ---
# Use noise as reference (in real case, use correlated noise reference)
adapt_out = lms_filter(noisy, noise, mu=0.01, order=8)

# --- Spectral subtraction ---
# Estimate noise from first 256 samples
noise_est = noisy[:256]
filt_spec = np.zeros_like(noisy)
for i in range(0, length, chunk_size):
    chunk = noisy[i:i+chunk_size]
    filt_spec[i:i+chunk_size] = spectral_subtraction(chunk, noise_est, fs)

# --- Wavelet denoising ---
filt_wave = wavelet_denoise(noisy)

# --- Plot results ---
plot_signals([noisy, clean], ['Noisy', 'Clean'], fs, title='Original Signals')
plot_signals([noisy, filt_fir], ['Noisy', 'FIR Filtered'], fs, title='FIR Filtering')
plot_signals([noisy, filt_freq], ['Noisy', 'Freq-Domain Filtered'], fs, title='Frequency-Domain Filtering')
plot_signals([noisy, adapt_out], ['Noisy', 'Adaptive LMS Output'], fs, title='Adaptive Filtering (LMS)')
plot_signals([noisy, filt_spec], ['Noisy', 'Spectral Subtraction'], fs, title='Spectral Subtraction')
plot_signals([noisy, filt_wave], ['Noisy', 'Wavelet Denoised'], fs, title='Wavelet Denoising')

# --- Print SNRs ---
print('SNR (Noisy):', calculate_snr(clean, noisy))
print('SNR (FIR):', calculate_snr(clean, filt_fir))
print('SNR (Freq):', calculate_snr(clean, filt_freq))
print('SNR (LMS):', calculate_snr(clean, adapt_out))
print('SNR (Spectral):', calculate_snr(clean, filt_spec))
print('SNR (Wavelet):', calculate_snr(clean, filt_wave)) 