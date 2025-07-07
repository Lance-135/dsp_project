import pywt
import numpy as np

def wavelet_denoise(signal, wavelet='db8', level=4, threshold_factor=0.5):
    coeffs = pywt.wavedec(signal, wavelet, level=level)
    sigma = np.median(np.abs(coeffs[-1])) / 0.6745
    uthresh = threshold_factor * sigma * np.sqrt(2 * np.log(len(signal)))
    denoised_coeffs = [pywt.threshold(c, value=uthresh, mode='soft') for c in coeffs]
    return pywt.waverec(denoised_coeffs, wavelet)[:len(signal)] 