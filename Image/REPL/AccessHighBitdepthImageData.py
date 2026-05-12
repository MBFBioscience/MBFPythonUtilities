# ==================================================================================
# MBFPython REPL - AccessHighBitdepthImageData.py
# ==================================================================================
#
# PURPOSE:
#
#   This script demonstrates how to access "high bit-depth" image data from any image
#	in a supported format (i.e., any image which can be opened in MBF applications).
#	The data returned will always reflect the original bit-depth of the image, will
#   always be "unsigned" data, and is suitable for image analysis (e.g, N-channel 16-bit )
#   
# --- ENVIRONMENT SETUP ---
#
# 1. Simply click the "Python REPL" button in the Image -> Tools ribonbar section
#    in order to start MBF Python. Note that if the correct version of MBF Python
#    is not installed, you will be promted to download and install it.
#
#    Note: you cannot access image data in a standard Python environment started
#    from the command line - you must be start python from the "Python REPL" button
#    inside a given MBF application!
#
# --- HOW TO USE THIS SCRIPT ---
#
# 1. You can copy/paste code from this file directly into an MBF Python REPL, or
#    simply use this script as an example to create your own custom scripts for
#    accessing image data.
#
#	**All image data is returned as a 5D NumPy array object in TCZYX order**
#
# ==================================================================================

# import "numpy" for array access, "mbfimage" for image access in MBF applications,
# and [optionally] "json" for metadata access (only needed if metadata is desired)
import numpy as np
import mbfimage as mbfimg
import json

# create an instance of the "pyimg_data" class, for "high bit-depth" image data
mimg = mbfimg.pyimg_data()

# Note: the above call is the only difference between loading "high bit-depth" 
# image data vs. "displayable" image data. The rest of the code is identical to 
# the file "AccessDisplayableImageData.py" script, and the same methods are
# used to initialize and query the image. For that reason, please refer to the
# "AccessDisplayableImageData.py" script for complete detailed usage examples.

# mbfimg.pyimg_data() vs mbfimg.pyimg_display() is the only difference
# between this script and AccessDisplayableImageData.py!