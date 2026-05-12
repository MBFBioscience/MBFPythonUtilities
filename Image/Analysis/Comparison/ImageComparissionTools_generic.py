# ==================================================================================
# Statistical Image Comparison Tool (For General Images)
# ==================================================================================
#
# PURPOSE:
#   This script compares the global statistical properties of two images. It is
#   designed for general-purpose comparison and DOES NOT require the images
#   to be spatially aligned or have the same dimensions.
#
# IDEAL USE CASE:
#   Getting a high-level statistical comparison between two different images
#   (e.g., "covered" vs. "uncovered") to see how their overall brightness and
#   intensity distributions differ.
#
# METRICS CALCULATED:
#   - Bhattacharyya Distance: Measures the similarity of the image histograms.
#   - Mattes Mutual Information: Measures the statistical dependency between
#     the images' intensity values.
#
# --- ENVIRONMENT SETUP (do this only once) ---
#
# 1. Open your Anaconda Prompt or terminal.
#
# 2. Create and activate a new, lightweight Conda environment:
#    conda create --name stats-env python=3.11 -y
#    conda activate stats-env
#
# 3. Install the required libraries:
#    conda install -c conda-forge itk tifffile numpy
#
# --- HOW TO USE THIS SCRIPT ---
#
# 1. Place your reference image and all comparison images in a single folder.
#
# 2. Run the script from the command line, pointing it to the folder and
#    specifying the reference image's filename.
#
# COMMAND STRUCTURE:
#   python <script_name>.py --folder "path/to/your/images" --reference "reference_image.tif" [OPTIONS]
#
# OPTIONS:
#   --output_csv "results.csv"  : Save all results to a CSV file.
#
# EXAMPLE:
#   python ImageComparissionTools_generic_v001.py --folder "C:\MyProject\Experiments" --reference "covered_image.tif" --output_csv "statistical_results.csv"
#
# ==================================================================================

import argparse
import csv
import tifffile
import numpy as np
from pathlib import Path

try:
    import itk
    itk_available = True
except ImportError:
    print("Warning: ITK not installed. Mutual Information will be skipped.")
    itk_available = False

# --- Constants ---
CSV_HEADERS = [
    "Reference File", "Comparison File", "Reference Dimensions", "Comparison Dimensions",
    "Bhattacharyya_Dist", "Mutual_Info_ITK"
]

# --- Metric Calculation Functions ---

def calculate_bhattacharyya_distance(hist1, hist2):
    """Calculates Bhattacharyya distance between two histograms."""
    # Normalize histograms to create probability distributions
    hist1_norm = hist1 / (np.sum(hist1) + 1e-9)
    hist2_norm = hist2 / (np.sum(hist2) + 1e-9)
    
    # Calculate Bhattacharyya coefficient
    bc = np.sum(np.sqrt(hist1_norm * hist2_norm))
    
    # Return the distance. Clip bc to avoid log(0)
    return -np.log(np.clip(bc, 1e-9, 1.0))

def calculate_itk_mutual_information(img1_np, img2_np):
    """Calculates Mattes Mutual Information using ITK on a central 2D slice."""
    if not itk_available:
        return "N/A"
    try:
        # Get a central slice from each image for a 2D comparison
        slice_idx1 = img1_np.shape[0] // 2 if img1_np.ndim == 3 else 0
        img1_slice = img1_np[slice_idx1] if img1_np.ndim == 3 else img1_np

        slice_idx2 = img2_np.shape[0] // 2 if img2_np.ndim == 3 else 0
        img2_slice = img2_np[slice_idx2] if img2_np.ndim == 3 else img2_np

        img1_itk = itk.image_from_array(img1_slice.astype(np.float32))
        img2_itk = itk.image_from_array(img2_slice.astype(np.float32))

        # Use a resampler to handle potentially different slice sizes
        resampler = itk.ResampleImageFilter.New(img2_itk)
        resampler.SetOutputParametersFromImage(img1_itk)
        resampler.SetDefaultPixelValue(0)
        resampler.Update()
        img2_resampled_itk = resampler.GetOutput()

        metric = itk.MattesMutualInformationImageToImageMetricv4.New()
        metric.SetFixedImage(img1_itk)
        metric.SetMovingImage(img2_resampled_itk)
        metric.Initialize()
        return metric.GetValue()
    except Exception as e:
        print(f"Error calculating ITK Mutual Information: {e}")
        return "N/A"

def write_to_csv(filepath, data):
    """Appends a dictionary of data as a new row to a CSV file."""
    file_exists = filepath.exists()
    with open(filepath, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# --- Main Processing Function ---

def compare_images_statistically(reference_path, comparison_path, output_csv=None):
    """Compares two images using only global statistical metrics."""
    try:
        print(f"Loading reference file: {reference_path.name}")
        reference_img = tifffile.imread(reference_path)
        print(f"Loading comparison file: {comparison_path.name}")
        comparison_img = tifffile.imread(comparison_path)

        print(f"Dimensions: {reference_img.shape} vs {comparison_img.shape}")

        results = {
            "Reference File": reference_path.name,
            "Comparison File": comparison_path.name,
            "Reference Dimensions": str(reference_img.shape),
            "Comparison Dimensions": str(comparison_img.shape),
        }
        
        # Calculate histogram-based metric
        results["Bhattacharyya_Dist"] = calculate_bhattacharyya_distance(
            np.histogram(reference_img, bins=256)[0],
            np.histogram(comparison_img, bins=256)[0]
        )

        # Calculate mutual information
        results["Mutual_Info_ITK"] = calculate_itk_mutual_information(reference_img, comparison_img)

        print("\n--- Statistical Comparison Report ---")
        for key, value in results.items():
            if isinstance(value, float):
                print(f"{key:<25}: {value:.6f}")
            else:
                print(f"{key:<25}: {value}")
        print("-------------------------------------\n")

        if output_csv:
            write_to_csv(Path(output_csv), results)

    except FileNotFoundError as e:
        print(f"Error: File not found. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Command-Line Interface ---

def main():
    parser = argparse.ArgumentParser(
        description="A tool to compare images using non-spatial, statistical metrics.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--folder", required=True, help="Path to the folder containing the images.")
    parser.add_argument("--reference", required=True, help="Filename of the reference image within the folder.")
    parser.add_argument("--output_csv", help="Optional. Path to save all results to a single CSV file.")
    
    args = parser.parse_args()

    input_folder = Path(args.folder)
    reference_path = input_folder / args.reference

    if not input_folder.is_dir():
        print(f"Error: Input folder not found at '{input_folder}'")
        return
    if not reference_path.exists():
        print(f"Error: Reference file '{args.reference}' not found in the folder.")
        return

    # Find all TIFF files to compare against the reference
    comparison_files = [
        f for f in input_folder.glob('*.tif*') 
        if f.is_file() and f.name != args.reference
    ]

    if not comparison_files:
        print("No other TIFF files found in the folder to compare against.")
        return
        
    print(f"Found {len(comparison_files)} file(s) to compare against '{args.reference}'.")
    if args.output_csv:
        print(f"Results will be saved to: {args.output_csv}")
    print("="*50)

    for comparison_path in comparison_files:
        print(f"\n>>> Starting comparison: '{args.reference}' vs '{comparison_path.name}'")
        compare_images_statistically(reference_path, comparison_path, args.output_csv)
        print("="*50)

    print("\nAll comparisons complete.")

if __name__ == "__main__":
    main()