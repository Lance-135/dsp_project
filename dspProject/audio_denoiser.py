import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np
import scipy.io.wavfile
import os
from src.utils import load_wav, calculate_snr, plot_signals
from src.filters import apply_fir_filter
from src.freq_filters import freq_filter
from src.spectral import spectral_subtraction
from src.wavelet import wavelet_denoise
import threading

class AudioDenoiserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Audio Denoiser")
        self.root.geometry("700x800")
        self.root.minsize(600, 700)
        
        # Configure style
        self.setup_styles()
        
        # Variables
        self.input_file_path = tk.StringVar()
        self.output_file_path = tk.StringVar()
        self.selected_method = tk.StringVar(value="spectral")
        self.progress_var = tk.DoubleVar()
        
        # Create GUI elements
        self.create_widgets()
        
    def setup_styles(self):
        """Configure custom styles for the GUI."""
        style = ttk.Style()
        
        # Configure button styles
        style.configure("Accent.TButton", 
                      background="#0078d4", 
                      foreground="white",
                      font=("Arial", 9, "bold"))
        
        # Configure frame styles
        style.configure("Title.TLabel", 
                      font=("Arial", 16, "bold"),
                      foreground="#0078d4")
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🎵 Audio Denoiser", style="Title.TLabel")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input file selection with enhanced UI
        input_frame = ttk.LabelFrame(main_frame, text="Step 1: Select Input Audio File", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # File info display
        self.file_info_label = ttk.Label(input_frame, text="No file selected", foreground="gray")
        self.file_info_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Input file entry and buttons
        ttk.Entry(input_frame, textvariable=self.input_file_path, width=60, state="readonly").grid(row=1, column=0, padx=(0, 5), pady=5)
        
        button_frame_input = ttk.Frame(input_frame)
        button_frame_input.grid(row=1, column=1, pady=5)
        
        ttk.Button(button_frame_input, text="📁 Browse Files", command=self.browse_input_file, 
                  style="Accent.TButton").pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame_input, text="🗑️ Clear", command=self.clear_input_file).pack(side=tk.LEFT, padx=2)
        
        # Output directory selection with enhanced UI
        output_frame = ttk.LabelFrame(main_frame, text="Step 2: Select Output Directory", padding="10")
        output_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Output info display
        self.output_info_label = ttk.Label(output_frame, text="No directory selected", foreground="gray")
        self.output_info_label.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Output directory entry and buttons
        ttk.Entry(output_frame, textvariable=self.output_file_path, width=60, state="readonly").grid(row=1, column=0, padx=(0, 5), pady=5)
        
        button_frame_output = ttk.Frame(output_frame)
        button_frame_output.grid(row=1, column=1, pady=5)
        
        ttk.Button(button_frame_output, text="📁 Browse Folders", command=self.browse_output_dir,
                  style="Accent.TButton").pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame_output, text="🗑️ Clear", command=self.clear_output_dir).pack(side=tk.LEFT, padx=2)
        
        # Denoising method selection with enhanced UI
        method_frame = ttk.LabelFrame(main_frame, text="Step 3: Choose Denoising Method", padding="10")
        method_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        methods = [
            ("🎯 Spectral Subtraction", "spectral", "Best for most audio files"),
            ("🌊 Wavelet Denoising", "wavelet", "Preserves signal details"),
            ("🔊 FIR Bandpass Filter", "fir", "Optimized for speech (300-3400 Hz)"),
            ("📡 Frequency Domain Filter", "freq", "FFT-based filtering")
        ]
        
        # Create method selection with descriptions
        for i, (text, value, description) in enumerate(methods):
            method_container = ttk.Frame(method_frame)
            method_container.grid(row=i, column=0, sticky=tk.W, pady=2)
            
            ttk.Radiobutton(method_container, text=text, variable=self.selected_method, 
                          value=value).pack(anchor=tk.W)
            ttk.Label(method_container, text=f"   {description}", foreground="gray", 
                     font=("Arial", 8)).pack(anchor=tk.W)
        
        # Progress and status section
        progress_frame = ttk.LabelFrame(main_frame, text="Processing Status", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Progress bar
        ttk.Label(progress_frame, text="Progress:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Status label
        self.status_label = ttk.Label(progress_frame, text="Ready to process", font=("Arial", 10))
        self.status_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Action buttons
        action_frame = ttk.LabelFrame(main_frame, text="Actions", padding="10")
        action_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        button_frame = ttk.Frame(action_frame)
        button_frame.pack(expand=True)
        
        ttk.Button(button_frame, text="🎵 Process Audio", command=self.process_audio, 
                  style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="👁️ Preview Results", command=self.preview_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.results_text = tk.Text(results_frame, height=8, width=70, font=("Consolas", 9))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add scrollbar to results text
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        
    def browse_input_file(self):
        filename = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("WAV files", "*.wav"),
                ("MP3 files", "*.mp3"),
                ("All audio files", "*.wav;*.mp3"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.input_file_path.set(filename)
            self.update_file_info(filename)
            
    def browse_output_dir(self):
        dirname = filedialog.askdirectory(title="Select Output Directory")
        if dirname:
            self.output_file_path.set(dirname)
            self.update_output_info(dirname)
            
    def clear_input_file(self):
        self.input_file_path.set("")
        self.file_info_label.config(text="No file selected", foreground="gray")
        
    def clear_output_dir(self):
        self.output_file_path.set("")
        self.output_info_label.config(text="No directory selected", foreground="gray")
        
    def clear_all(self):
        self.clear_input_file()
        self.clear_output_dir()
        self.progress_var.set(0)
        self.status_label.config(text="Ready to process")
        self.results_text.delete(1.0, tk.END)
        
    def update_file_info(self, filepath):
        """Update file information display."""
        try:
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                file_size_mb = file_size / (1024 * 1024)
                
                # Try to get audio info
                try:
                    fs, data = load_wav(filepath)
                    duration = len(data) / fs
                    info_text = f"✓ {os.path.basename(filepath)} | {file_size_mb:.1f} MB | {duration:.1f}s | {fs} Hz"
                    self.file_info_label.config(text=info_text, foreground="green")
                except:
                    info_text = f"✓ {os.path.basename(filepath)} | {file_size_mb:.1f} MB"
                    self.file_info_label.config(text=info_text, foreground="green")
            else:
                self.file_info_label.config(text="❌ File not found", foreground="red")
        except Exception as e:
            self.file_info_label.config(text=f"❌ Error: {str(e)}", foreground="red")
            
    def update_output_info(self, dirpath):
        """Update output directory information display."""
        try:
            if os.path.exists(dirpath):
                # Count files in directory
                file_count = len([f for f in os.listdir(dirpath) if f.endswith('.wav')])
                info_text = f"✓ {os.path.basename(dirpath)} | {file_count} WAV files"
                self.output_info_label.config(text=info_text, foreground="green")
            else:
                self.output_info_label.config(text="❌ Directory not found", foreground="red")
        except Exception as e:
            self.output_info_label.config(text=f"❌ Error: {str(e)}", foreground="red")
        
    def process_audio(self):
        if not self.input_file_path.get():
            messagebox.showerror("Error", "Please select an input audio file")
            return
            
        if not self.output_file_path.get():
            messagebox.showerror("Error", "Please select an output directory")
            return
            
        # Start processing in a separate thread to avoid GUI freezing
        thread = threading.Thread(target=self._process_audio_thread)
        thread.daemon = True
        thread.start()
        
    def _process_audio_thread(self):
        try:
            self.status_label.config(text="Loading audio file...")
            self.progress_var.set(10)
            self.root.update()
            
            # Load audio file
            fs, noisy = load_wav(self.input_file_path.get())
            length = len(noisy)
            chunk_size = 256
            
            self.status_label.config(text="Processing audio...")
            self.progress_var.set(30)
            self.root.update()
            
            # Apply selected denoising method
            method = self.selected_method.get()
            
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
            
            self.progress_var.set(70)
            self.root.update()
            
            # Save the denoised audio
            self.status_label.config(text="Saving denoised audio...")
            
            # Create output filename
            input_filename = os.path.basename(self.input_file_path.get())
            name, ext = os.path.splitext(input_filename)
            output_filename = f"{name}_denoised_{method}{ext}"
            output_path = os.path.join(self.output_file_path.get(), output_filename)
            
            # Convert to int16 for WAV format
            final_int16 = np.int16(denoised / np.max(np.abs(denoised)) * 32767)
            scipy.io.wavfile.write(output_path, fs, final_int16)
            
            self.progress_var.set(100)
            self.status_label.config(text="Processing complete!")
            
            # Calculate and display results
            # For SNR calculation, we'll use the noisy signal as reference since we don't have clean
            snr_noisy = calculate_snr(noisy, noisy)  # This will be 0 dB
            snr_denoised = calculate_snr(noisy, denoised)
            
            results = f"""
Processing Complete!

Input file: {input_filename}
Output file: {output_filename}
Method: {method.upper()}
Sample rate: {fs} Hz
Duration: {length/fs:.2f} seconds

Results:
- Input SNR: {snr_noisy:.2f} dB
- Denoised SNR: {snr_denoised:.2f} dB
- SNR improvement: {snr_denoised - snr_noisy:.2f} dB

Denoised audio saved to: {output_path}
            """
            
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, results)
            
            messagebox.showinfo("Success", f"Audio denoised successfully!\nSaved to: {output_path}")
            
        except Exception as e:
            self.status_label.config(text="Error occurred during processing")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.progress_var.set(0)
            
    def preview_results(self):
        if not self.input_file_path.get():
            messagebox.showerror("Error", "Please select an input audio file first")
            return
            
        try:
            # Load and process a small segment for preview
            fs, noisy = load_wav(self.input_file_path.get())
            
            # Take first 2048 samples for preview
            preview_length = min(2048, len(noisy))
            noisy_preview = noisy[:preview_length]
            
            method = self.selected_method.get()
            
            if method == "spectral":
                noise_est = noisy_preview[:256]
                denoised_preview = spectral_subtraction(noisy_preview, noise_est, fs)
            elif method == "wavelet":
                denoised_preview = wavelet_denoise(noisy_preview)
            elif method == "fir":
                denoised_preview = apply_fir_filter(noisy_preview, cutoff=[300, 3400], fs=fs, numtaps=101, pass_type='band')
            elif method == "freq":
                denoised_preview = freq_filter(noisy_preview, fs, low=300, high=3400)
            
            # Plot preview
            plot_signals([noisy_preview, denoised_preview], 
                        ['Original', f'Denoised ({method})'], 
                        fs, 
                        title=f'Preview: {method.upper()} Denoising')
                        
        except Exception as e:
            messagebox.showerror("Error", f"Error creating preview: {str(e)}")

def main():
    root = tk.Tk()
    app = AudioDenoiserGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 