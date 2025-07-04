# Real-Time Noise Reduction and Signal Enhancement in 1D Signals

## Overview
This project demonstrates real-time noise reduction and signal enhancement for 1D signals (e.g., voice, ECG, vibration) using digital signal processing (DSP) techniques. It includes time-domain filtering, frequency-domain filtering, adaptive filtering, spectral subtraction, and optional wavelet denoising.

## Features
- FIR/IIR low-pass and high-pass filters
- Frequency-domain (FFT-based) filtering
- Adaptive filtering (LMS/NLMS)
- Spectral subtraction
- Wavelet denoising (optional)
- Real-time (chunked) processing simulation
- Visualization of input and output signals

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the main script:
   ```bash
   python main.py
   ```

## Directory Structure
```
dspProject/
├── data/                # Datasets (synthetic or real)
├── src/
│   ├── filters.py       # Time-domain filters (FIR/IIR)
│   ├── freq_filters.py  # Frequency-domain filtering (FFT/iFFT)
│   ├── adaptive.py      # Adaptive filtering (LMS/NLMS)
│   ├── spectral.py      # Spectral subtraction
│   ├── wavelet.py       # Wavelet denoising (optional)
│   └── utils.py         # Signal generation, SNR, plotting, etc.
├── main.py              # Main script: real-time pipeline
├── requirements.txt     # Python dependencies
└── README.md            # Project overview and instructions
```

## Notes
- You can use your own 1D signals or generate synthetic ones.
- The code is modular for easy experimentation with different DSP techniques. 