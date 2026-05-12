# ==================================================================================
# Comprehensive Image Comparison Tool (For Aligned Images)
# ==================================================================================
#
# PURPOSE:
#   This script performs a deep, pixel-for-pixel and perceptual comparison
#   between a reference image and one or more comparison images. It is designed
#   for images that are SPATIALLY ALIGNED and have IDENTICAL DIMENSIONS.
#
# IDEAL USE CASE:
#   Quantifying the exact differences introduced by image compression, filtering,
#   or other processing steps where the underlying scene does not change.
#
# METRICS CALCULATED:
#   - Pixel-based error (MSE, MAE, PSNR)
#   - Structural similarity (SSIM, MS-SSIM)
#   - Perceptual difference (LPIPS)
#   - And more...
#
# --- ENVIRONMENT SETUP (do this only once) ---
#
# 1. Open your Anaconda Prompt or terminal.
#
# 2. Create and activate a new Conda environment:
#    conda create --name compare-env python=3.11 -y
#    conda activate compare-env
#
# 3. Install the required libraries:
#    conda install -c conda-forge itk scikit-image scipy pytorch tifffile
#    pip install pyiqa
#
# --- HOW TO USE THIS SCRIPT ---
#
# 1. Place your original reference image and all comparison versions in a
#    single folder.
#
# 2. Run the script from the command line, pointing it to the folder and
#    specifying the original image's filename.
#
# COMMAND STRUCTURE:
#   python <script_name>.py --folder "path/to/your/images" --original "original_image.tif" [OPTIONS]
#
# OPTIONS:
#   --output_csv "results.csv"  : Save all results to a CSV file.
#   --force                     : Calculate all metrics even if files are identical.
#   --lpips_net vgg             : Use the more sensitive VGG network for LPIPS
#                                 (default is 'alex').
#
# EXAMPLE:
#   python ImageComparissionTools_v032.py --folder "C:\MyProject\CompressionTest" --original "lossless.tif" --output_csv "compression_results.csv"
#
# ==================================================================================

import argparse
import csv
import tifffile
import numpy as np
from pathlib import Path
from scipy.stats import pearsonr

# --- Optional Imports with availability checks ---
try:
    from skimage.metrics import peak_signal_noise_ratio, structural_similarity
    skimage_available = True
except ImportError:
    print("Warning: scikit-image not installed. PSNR and SSIM will be skipped.")
    skimage_available = False

try:
    import itk
    itk_available = True
except ImportError:
    print("Warning: ITK not installed. ITK-based metrics will be skipped.")
    itk_available = False

try:
    import pyiqa
    import torch
    pyiqa_available = True
except ImportError:
    print("Warning: pyiqa or torch not installed. Perceptual metrics (MS-SSIM, VIF, LPIPS) will be skipped.")
    pyiqa_available = False

# --- Constants ---
CSV_HEADERS = [
    "Original File", "Compressed File", "Dimensions", "Lossless",
    "MSE", "MAE", "Median_SE", "Max_AE", "PSNR",
    "SSIM", "MS_SSIM", "VIF", "LPIPS", "LPIPS_Net",
    "Pearson_Corr", "Bhattacharyya_Dist", "Mutual_Info_ITK", "ITK_Slice_Idx"
]

# --- Metric Calculation Functions ---

def calculate_bhattacharyya_distance(hist1, hist2):
    """Calculates Bhattacharyya distance between two histograms."""
    hist1_norm = hist1 / (np.sum(hist1) + 1e-9)
    hist2_norm = hist2 / (np.sum(hist2) + 1e-9)
    bc = np.sum(np.sqrt(hist1_norm * hist2_norm))
    return -np.log(np.clip(bc, 1e-9, 1.0))

def calculate_itk_mutual_information(img1_np, img2_np):
    """Calculates Mattes Mutual Information using ITK on a central 2D slice."""
    if not itk_available:
        return "N/A", None
    try:
        slice_idx = img1_np.shape[0] // 2 if img1_np.ndim == 3 else 0
        img1_slice = img1_np[slice_idx] if img1_np.ndim == 3 else img1_np
        img2_slice = img2_np[slice_idx] if img2_np.ndim == 3 else img2_np

        img1_itk = itk.image_from_array(img1_slice.astype(np.float32))
        img2_itk = itk.image_from_array(img2_slice.astype(np.float32))

        metric = itk.MattesMutualInformationImageToImageMetricv4.New()
        metric.SetFixedImage(img1_itk)
        metric.SetMovingImage(img2_itk)
        metric.Initialize()
        return metric.GetValue(), slice_idx
    except Exception as e:
        print(f"Error calculating ITK Mutual Information: {e}")
        return "N/A", None

def calculate_pyiqa_metric(img1_np, img2_np, metric_name, data_range, batch_size=4, device=None, lpips_net='alex'):
    """
    Calculates a specified metric from the pyiqa library for a 3D volume.
    Handles device placement and batching to avoid GPU memory errors.
    """
    if not pyiqa_available:
        return "N/A"
    try:
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        if metric_name == 'lpips':
            metric_model = pyiqa.create_metric(metric_name, net=lpips_net, device=device)
        else:
            metric_model = pyiqa.create_metric(metric_name, device=device)

        scores = []
        is_3d = img1_np.ndim == 3
        num_slices = img1_np.shape[0] if is_3d else 1

        for i in range(0, num_slices, batch_size):
            batch_end = min(i + batch_size, num_slices)
            
            if is_3d:
                batch1 = np.stack([img1_np[j] for j in range(i, batch_end)])
                batch2 = np.stack([img2_np[j] for j in range(i, batch_end)])
            else:
                batch1 = img1_np[None, ...]
                batch2 = img2_np[None, ...]

            batch1_rgb = np.stack([batch1] * 3, axis=1) / data_range
            batch2_rgb = np.stack([batch2] * 3, axis=1) / data_range

            tensor1 = torch.tensor(batch1_rgb, dtype=torch.float32).to(device)
            tensor2 = torch.tensor(batch2_rgb, dtype=torch.float32).to(device)

            with torch.no_grad():
                score_tensor = metric_model(tensor1, tensor2)
                scores.extend(score_tensor.cpu().numpy())

            del tensor1, tensor2
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        return float(np.mean(scores))
    except Exception as e:
        print(f"Error calculating {metric_name.upper()}: {e}")
        return "N/A"

def calculate_ssim_3d(img1, img2, data_range):
    """Calculates the mean SSIM for a 3D volume, slice by slice."""
    if not skimage_available:
        return "N/A"
    if img1.ndim == 2:
        return structural_similarity(img1, img2, data_range=data_range)
    
    scores = [structural_similarity(img1[i], img2[i], data_range=data_range) for i in range(img1.shape[0])]
    return np.mean(scores)

def write_to_csv(filepath, data):
    """Appends a dictionary of data as a new row to a CSV file."""
    file_exists = filepath.exists()
    with open(filepath, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def verify_lossless(original_path, compressed_path, output_csv=None, force_calculate=False, lpips_net='alex'):
    """Main function to compare images and calculate quality metrics."""
    try:
        print(f"Loading original file: {original_path.name}")
        original_img = tifffile.imread(original_path)
        print(f"Loading compressed file: {compressed_path.name}")
        compressed_img = tifffile.imread(compressed_path)

        if original_img.shape != compressed_img.shape:
            print(f"Error: Image shapes do not match. Original: {original_img.shape}, Compressed: {compressed_img.shape}")
            return

        data_range = float(np.iinfo(original_img.dtype).max) if np.issubdtype(original_img.dtype, np.integer) else 1.0

        print("Comparing arrays for exact match...")
        is_lossless = np.array_equal(original_img, compressed_img)
        
        results = {
            "Original File": original_path.name,
            "Compressed File": compressed_path.name,
            "Dimensions": str(original_img.shape),
            "Lossless": is_lossless
        }

        if is_lossless and not force_calculate:
            print("\n✅ Compression was lossless.")
            print("   (Use --force to calculate metrics anyway for a full report)")
        else:
            if is_lossless:
                print("\n✅ Compression was lossless. Calculating metrics as requested by --force flag...")
            else:
                print("\n❌ Compression was lossy. Calculating quality metrics...")

            diff = original_img.astype(np.float32) - compressed_img.astype(np.float32)
            
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            if pyiqa_available:
                print(f"Using device: {device} for perceptual metrics.")
            
            mutual_info, slice_idx = calculate_itk_mutual_information(original_img, compressed_img)
            
            results.update({
                "MSE": np.mean(diff**2),
                "MAE": np.mean(np.abs(diff)),
                "Median_SE": np.median(diff**2),
                "Max_AE": np.max(np.abs(diff)),
                "PSNR": peak_signal_noise_ratio(original_img, compressed_img, data_range=data_range) if skimage_available else "N/A",
                "SSIM": calculate_ssim_3d(original_img, compressed_img, data_range),
                "MS_SSIM": calculate_pyiqa_metric(original_img, compressed_img, 'ms_ssim', data_range, device=device),
                "VIF": calculate_pyiqa_metric(original_img, compressed_img, 'vif', data_range, device=device),
                "LPIPS": calculate_pyiqa_metric(original_img, compressed_img, 'lpips', data_range, device=device, lpips_net=lpips_net),
                "LPIPS_Net": lpips_net,
                "Pearson_Corr": pearsonr(original_img.flatten(), compressed_img.flatten())[0],
                "Bhattacharyya_Dist": calculate_bhattacharyya_distance(np.histogram(original_img, bins=256)[0], np.histogram(compressed_img, bins=256)[0]),
                "Mutual_Info_ITK": mutual_info,
                "ITK_Slice_Idx": slice_idx
            })

        print("\n--- Comparison Report ---")
        for key, value in results.items():
            if isinstance(value, float):
                print(f"{key:<20}: {value:.6f}")
            else:
                print(f"{key:<20}: {value}")
        print("-------------------------\n")

        if output_csv:
            write_to_csv(Path(output_csv), results)

    except FileNotFoundError as e:
        print(f"Error: File not found. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="A comprehensive tool to compare an original image to all other images in a folder.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--folder", required=True, help="Path to the folder containing the original and compressed images.")
    parser.add_argument("--original", required=True, help="Filename of the original, uncompressed image within the folder.")
    parser.add_argument("--output_csv", help="Optional. Path to save all results to a single CSV file.")
    parser.add_argument("--force", action='store_true', help="Force calculation of all metrics even if files are identical.")
    parser.add_argument("--lpips_net", type=str, choices=['alex', 'vgg'], default='alex', help="Network for LPIPS: 'alex' or 'vgg' (default: alex).")
    
    args = parser.parse_args()

    input_folder = Path(args.folder)
    original_path = input_folder / args.original

    if not input_folder.is_dir():
        print(f"Error: Input folder not found at '{input_folder}'")
        return
    if not original_path.exists():
        print(f"Error: Original file '{args.original}' not found in the folder.")
        return

    comparison_files = [
        f for f in input_folder.glob('*.tif*') 
        if f.is_file() and f.name != args.original
    ]

    if not comparison_files:
        print("No other TIFF files found in the folder to compare against.")
        return
        
    print(f"Found {len(comparison_files)} file(s) to compare against '{args.original}'.")
    if args.output_csv:
        print(f"Results will be saved to: {args.output_csv}")
    print("="*50)

    for compressed_path in comparison_files:
        print(f"\n>>> Starting comparison: '{args.original}' vs '{compressed_path.name}'")
        verify_lossless(original_path, compressed_path, args.output_csv, args.force, args.lpips_net)
        print("="*50)

    print("\nAll comparisons complete.")

if __name__ == "__main__":
    main()