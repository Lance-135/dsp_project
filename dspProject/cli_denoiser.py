import argparse
import numpy as np
import scipy.io.wavfile
import os
from src.utils import load_wav, calculate_snr
from src.filters import apply_fir_filter
from src.freq_filters import freq_filter
from src.spectral import spectral_subtraction
from src.wavelet import wavelet_denoise

def denoise_audio(input_path, output_path, method="spectral", chunk_size=256):
    """
    Denoise an audio file using the specified method.
    
    Args:
        input_path (str): Path to input audio file
        output_path (str): Path to save denoised audio
        method (str): Denoising method ('spectral', 'wavelet', 'fir', 'freq')
        chunk_size (int): Chunk size for processing
    
    Returns:
        dict: Processing results and statistics
    """
    print(f"Loading audio file: {input_path}")
    fs, noisy = load_wav(input_path)
    length = len(noisy)
    
    print(f"Audio info: {length} samples, {fs} Hz, {length/fs:.2f} seconds")
    print(f"Applying {method.upper()} denoising...")
    
    # Apply selected denoising method
    if method == "spectral":
        # Estimate noise from first 256 samples
        noise_est = noisy[:256]
        denoised = np.zeros_like(noisy)
        for i in range(0, length, chunk_size):
            chunk = noisy[i:i+chunk_size]
            denoised[i:i+chunk_size] = spectral_subtraction(chunk, noise_est, fs)
            
    elif method == "wavelet":
        denoised = wavelet_denoise(noisy)
        
    elif method == "fir":
        denoised = np.zeros_like(noisy)
        for i in range(0, length, chunk_size):
            chunk = noisy[i:i+chunk_size]
            denoised[i:i+chunk_size] = apply_fir_filter(chunk, cutoff=[300, 3400], fs=fs, numtaps=101, pass_type='band')
            
    elif method == "freq":
        denoised = np.zeros_like(noisy)
        for i in range(0, length, chunk_size):
            chunk = noisy[i:i+chunk_size]
            denoised[i:i+chunk_size] = freq_filter(chunk, fs, low=300, high=3400)
    
    # Save the denoised audio
    print(f"Saving denoised audio to: {output_path}")
    final_int16 = np.int16(denoised / np.max(np.abs(denoised)) * 32767)
    scipy.io.wavfile.write(output_path, fs, final_int16)
    
    # Calculate statistics
    snr_noisy = calculate_snr(noisy, noisy)  # This will be 0 dB
    snr_denoised = calculate_snr(noisy, denoised)
    
    results = {
        'input_file': input_path,
        'output_file': output_path,
        'method': method,
        'sample_rate': fs,
        'duration': length/fs,
        'snr_noisy': snr_noisy,
        'snr_denoised': snr_denoised,
        'snr_improvement': snr_denoised - snr_noisy
    }
    
    return results

def select_file_with_explorer():
    """Open file explorer to select input file."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        # Create a hidden root window
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        
        root.destroy()
        return filename
    except ImportError:
        print("Error: tkinter not available. Please install tkinter or specify file path directly.")
        return None

def select_output_directory_with_explorer():
    """Open file explorer to select output directory."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        # Create a hidden root window
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        dirname = filedialog.askdirectory(title="Select Output Directory")
        
        root.destroy()
        return dirname
    except ImportError:
        print("Error: tkinter not available. Please install tkinter or specify output path directly.")
        return None

def main():
    parser = argparse.ArgumentParser(description='Audio Denoiser - Command Line Interface')
    parser.add_argument('input', nargs='?', help='Input audio file path (or use --explorer to select)')
    parser.add_argument('output', nargs='?', help='Output audio file path (or use --explorer to select)')
    parser.add_argument('--method', '-m', 
                       choices=['spectral', 'wavelet', 'fir', 'freq'],
                       default='spectral',
                       help='Denoising method to use (default: spectral)')
    parser.add_argument('--chunk-size', '-c',
                       type=int,
                       default=256,
                       help='Chunk size for processing (default: 256)')
    parser.add_argument('--explorer', '-e',
                       action='store_true',
                       help='Use file explorer to select input and output files')
    
    args = parser.parse_args()
    
    # Handle file selection
    input_path = args.input
    output_path = args.output
    
    if args.explorer or input_path is None:
        print("Opening file explorer to select input file...")
        input_path = select_file_with_explorer()
        if not input_path:
            print("No input file selected. Exiting.")
            return
    
    if args.explorer or output_path is None:
        print("Opening file explorer to select output directory...")
        output_dir = select_output_directory_with_explorer()
        if not output_dir:
            print("No output directory selected. Exiting.")
            return
        
        # Create output filename based on input filename
        if input_path:
            input_filename = os.path.basename(input_path)
            name, ext = os.path.splitext(input_filename)
            output_filename = f"{name}_denoised_{args.method}{ext}"
            output_path = os.path.join(output_dir, output_filename)
    
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' does not exist")
        return
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        results = denoise_audio(input_path, output_path, args.method, args.chunk_size)
        
        print("\n" + "="*50)
        print("PROCESSING COMPLETE")
        print("="*50)
        print(f"Input file: {results['input_file']}")
        print(f"Output file: {results['output_file']}")
        print(f"Method: {results['method'].upper()}")
        print(f"Sample rate: {results['sample_rate']} Hz")
        print(f"Duration: {results['duration']:.2f} seconds")
        print(f"Input SNR: {results['snr_noisy']:.2f} dB")
        print(f"Denoised SNR: {results['snr_denoised']:.2f} dB")
        print(f"SNR improvement: {results['snr_improvement']:.2f} dB")
        print("="*50)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 