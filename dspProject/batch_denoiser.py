import os
import glob
import argparse
from cli_denoiser import denoise_audio

def batch_denoise(input_dir, output_dir, method="spectral", file_pattern="*.wav"):
    """
    Process multiple audio files in a directory.
    
    Args:
        input_dir (str): Directory containing input audio files
        output_dir (str): Directory to save denoised audio files
        method (str): Denoising method to use
        file_pattern (str): File pattern to match (e.g., "*.wav")
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Find all matching files
    pattern = os.path.join(input_dir, file_pattern)
    input_files = glob.glob(pattern)
    
    if not input_files:
        print(f"No files found matching pattern: {pattern}")
        return
    
    print(f"Found {len(input_files)} files to process")
    print(f"Using method: {method}")
    print(f"Output directory: {output_dir}")
    print("-" * 50)
    
    results = []
    
    for i, input_file in enumerate(input_files, 1):
        print(f"\nProcessing file {i}/{len(input_files)}: {os.path.basename(input_file)}")
        
        # Create output filename
        filename = os.path.basename(input_file)
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}_denoised_{method}{ext}"
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            # Process the file
            result = denoise_audio(input_file, output_path, method)
            results.append(result)
            
            print(f"✓ Successfully processed: {filename}")
            print(f"  SNR improvement: {result['snr_improvement']:.2f} dB")
            
        except Exception as e:
            print(f"✗ Error processing {filename}: {str(e)}")
    
    # Print summary
    print("\n" + "="*50)
    print("BATCH PROCESSING SUMMARY")
    print("="*50)
    print(f"Total files: {len(input_files)}")
    print(f"Successfully processed: {len(results)}")
    print(f"Failed: {len(input_files) - len(results)}")
    
    if results:
        avg_improvement = sum(r['snr_improvement'] for r in results) / len(results)
        print(f"Average SNR improvement: {avg_improvement:.2f} dB")
        
        # Show best and worst results
        best_result = max(results, key=lambda x: x['snr_improvement'])
        worst_result = min(results, key=lambda x: x['snr_improvement'])
        
        print(f"Best improvement: {best_result['snr_improvement']:.2f} dB ({os.path.basename(best_result['input_file'])})")
        print(f"Worst improvement: {worst_result['snr_improvement']:.2f} dB ({os.path.basename(worst_result['input_file'])})")

def main():
    parser = argparse.ArgumentParser(description='Batch Audio Denoiser')
    parser.add_argument('input_dir', help='Directory containing input audio files')
    parser.add_argument('output_dir', help='Directory to save denoised audio files')
    parser.add_argument('--method', '-m', 
                       choices=['spectral', 'wavelet', 'fir', 'freq'],
                       default='spectral',
                       help='Denoising method to use (default: spectral)')
    parser.add_argument('--pattern', '-p',
                       default='*.wav',
                       help='File pattern to match (default: *.wav)')
    
    args = parser.parse_args()
    
    # Check if input directory exists
    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist")
        return
    
    # Check if input directory is actually a directory
    if not os.path.isdir(args.input_dir):
        print(f"Error: '{args.input_dir}' is not a directory")
        return
    
    try:
        batch_denoise(args.input_dir, args.output_dir, args.method, args.pattern)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 