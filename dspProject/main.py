import numpy as np
from src.utils import load_wav, calculate_snr, plot_signals
from src.filters import apply_fir_filter
from src.freq_filters import freq_filter
from src.spectral import spectral_subtraction
from src.wavelet import wavelet_denoise
import scipy.io.wavfile
import os

# --- Load real noisy signal ---
wav_path = os.path.join('data', '0dB', 'sp01_babble_sn0.wav')
fs, noisy = load_wav(wav_path)
length = len(noisy)
chunk_size = 256  # Simulate real-time processing

# If you have a clean reference, load it here (for SNR calculation)
# fs, clean = load_wav('data/0dB/sp01_clean.wav')
# For now, use noisy as a placeholder for clean
clean = noisy.copy()

# --- Time-domain FIR bandpass filtering (for speech: 300-3400 Hz) ---
filt_fir = np.zeros_like(noisy)
for i in range(0, length, chunk_size):
    chunk = noisy[i:i+chunk_size]
    filt_fir[i:i+chunk_size] = apply_fir_filter(chunk, cutoff=[300, 3400], fs=fs, numtaps=101, pass_type='band')

# --- Frequency-domain bandpass filtering ---
filt_freq = np.zeros_like(noisy)
for i in range(0, length, chunk_size):
    chunk = noisy[i:i+chunk_size]
    filt_freq[i:i+chunk_size] = freq_filter(chunk, fs, low=300, high=3400)

# --- Spectral subtraction ---
# Estimate noise from first 256 samples (assume mostly noise at start)
noise_est = noisy[:256]
filt_spec = np.zeros_like(noisy)
for i in range(0, length, chunk_size):
    chunk = noisy[i:i+chunk_size]
    filt_spec[i:i+chunk_size] = spectral_subtraction(chunk, noise_est, fs)

# --- Wavelet denoising ---
filt_wave = wavelet_denoise(noisy)

# --- Choose the best result to save (e.g., spectral subtraction) ---
final_denoised = filt_spec

# --- Save the denoised result as a WAV file ---
# Convert to int16 for WAV format
final_int16 = np.int16(final_denoised / np.max(np.abs(final_denoised)) * 32767)
out_path = os.path.join('data', '0dB', 'sp01_babble_sn0_denoised.wav')
scipy.io.wavfile.write(out_path, fs, final_int16)
print(f"Denoised audio saved to {out_path}")

# --- Plot results (zoomed window) ---
plot_window = (1000, 1400)  # Plot only the first 400 samples for better detail
plot_signals([noisy], ['Noisy'], fs, title='Original Noisy Signal', window=plot_window)
plot_signals([noisy, filt_fir], ['Noisy', 'FIR Bandpass Filtered'], fs, title='FIR Bandpass Filtering', window=plot_window)
plot_signals([noisy, filt_freq], ['Noisy', 'Freq-Domain Bandpass'], fs, title='Frequency-Domain Bandpass Filtering', window=plot_window)
plot_signals([noisy, filt_spec], ['Noisy', 'Spectral Subtraction'], fs, title='Spectral Subtraction', window=plot_window)
plot_signals([noisy, filt_wave], ['Noisy', 'Wavelet Denoised'], fs, title='Wavelet Denoising', window=plot_window)

# --- Print SNRs ---
print('SNR (Noisy):', calculate_snr(clean, noisy))
print('SNR (FIR Bandpass):', calculate_snr(clean, filt_fir))
print('SNR (Freq Bandpass):', calculate_snr(clean, filt_freq))
print('SNR (Spectral):', calculate_snr(clean, filt_spec))
print('SNR (Wavelet):', calculate_snr(clean, filt_wave)) 