import numpy as np
from scipy.signal import lfilter, butter, firwin

def apply_fir_filter(signal, cutoff, fs, numtaps=101, pass_type='low'):
    # Map to valid firwin pass_zero values and handle bandpass/bandstop
    if pass_type == 'low':
        pass_zero = 'lowpass'
    elif pass_type == 'high':
        pass_zero = 'highpass'
    elif pass_type == 'band':
        pass_zero = 'bandpass'
    elif pass_type == 'stop':
        pass_zero = 'bandstop'
    else:
        pass_zero = pass_type
    taps = firwin(numtaps, cutoff, fs=fs, pass_zero=pass_zero)
    return lfilter(taps, 1.0, signal)

def apply_iir_filter(signal, cutoff, fs, order=4, pass_type='low'):
    b, a = butter(order, cutoff, fs=fs, btype=pass_type)
    return lfilter(b, a, signal) 