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
- **NEW**: User-friendly interfaces for audio denoising

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the main script:
   ```bash
   python main.py
   ```

## Audio Denoising Interfaces

### GUI Interface
For a graphical user interface to denoise audio files:
```bash
python audio_denoiser.py
```

**Features:**
- File browser for selecting input audio files
- Output directory selection
- Multiple denoising method options:
  - Spectral Subtraction
  - Wavelet Denoising
  - FIR Bandpass Filter
  - Frequency Domain Filter
- Progress tracking
- Preview functionality
- Results display with SNR statistics

### Command Line Interface
For command-line processing:
```bash
python cli_denoiser.py input.wav output.wav --method spectral
```

**Usage:**
```bash
python cli_denoiser.py <input_file> <output_file> [options]

Options:
  --method, -m    Denoising method: spectral, wavelet, fir, freq (default: spectral)
  --chunk-size, -c  Chunk size for processing (default: 256)
  --explorer, -e  Use file explorer to select input and output files
```

**Examples:**
```bash
# Basic usage with spectral subtraction
python cli_denoiser.py noisy_audio.wav denoised_audio.wav

# Use file explorer to select files
python cli_denoiser.py --explorer

# Use wavelet denoising with file explorer
python cli_denoiser.py --explorer --method wavelet

# Use FIR bandpass filter
python cli_denoiser.py noisy_audio.wav denoised_audio.wav --method fir

# Use frequency domain filter
python cli_denoiser.py noisy_audio.wav denoised_audio.wav --method freq
```

### Interactive Interface (Easiest)
For the simplest experience with automatic file explorers:
```bash
python interactive_denoiser.py
```

**Features:**
- Automatically opens file explorer for input file selection
- Automatically opens file explorer for output directory selection
- Interactive method selection
- Step-by-step guided process
- Option to process multiple files in sequence

### Batch Processing
For processing multiple files at once:
```bash
python batch_denoiser.py input_directory output_directory --method spectral
```

**Usage:**
```bash
python batch_denoiser.py <input_dir> <output_dir> [options]

Options:
  --method, -m    Denoising method: spectral, wavelet, fir, freq (default: spectral)
  --pattern, -p   File pattern to match (default: *.wav)
```

**Examples:**
```bash
# Process all WAV files in a directory
python batch_denoiser.py ./noisy_files ./denoised_files

# Process with specific method
python batch_denoiser.py ./noisy_files ./denoised_files --method wavelet

# Process specific file pattern
python batch_denoiser.py ./noisy_files ./denoised_files --pattern "*.wav"
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
├── audio_denoiser.py    # GUI interface for audio denoising
├── cli_denoiser.py      # Command-line interface for audio denoising
├── interactive_denoiser.py  # Interactive interface with file explorers
├── batch_denoiser.py    # Batch processing for multiple files
├── requirements.txt     # Python dependencies
└── README.md            # Project overview and instructions
```

## Denoising Methods

1. **Spectral Subtraction**: Estimates noise from the beginning of the audio and subtracts it from the signal spectrum
2. **Wavelet Denoising**: Uses wavelet transform to separate signal from noise in different frequency bands
3. **FIR Bandpass Filter**: Applies a bandpass filter (300-3400 Hz) optimized for speech signals
4. **Frequency Domain Filter**: Uses FFT-based filtering in the frequency domain

## Notes
- You can use your own 1D signals or generate synthetic ones.
- The code is modular for easy experimentation with different DSP techniques.
- The GUI interface requires tkinter (usually included with Python).
- Supported audio format: WAV files.
- Output files are automatically named with the method used (e.g., `input_denoised_spectral.wav`). 