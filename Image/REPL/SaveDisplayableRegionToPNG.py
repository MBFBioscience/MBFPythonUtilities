# ==================================================================================
# MBFPython REPL - SaveDisplayableRegionToPNG.py
# ==================================================================================
#
# PURPOSE:
#
#   This script demonstrates how to access "displayable" image data from any image
#	in a supported format (i.e., any image which can be opened in MBF applications).
#	and save it to a PNG file for visualization or publication.
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
# ==================================================================================

# import "numpy" for array access, "mbfimage" for image access in MBF applications,
# and "PIL.Image" for creation of the final PNG image on disk.
import numpy as np
import mbfimage as mbfimg
from PIL import Image

# Note: please see AccessDisplayableImageData.py for complete detailed usage 
# examples of how to access displayable image data - the below loading steps
# will be extremely terse since the focus of this script is on saving to PNG,
# not loading the data.

mimg = mbfimg.pyimg_display()
mimg.init_with_string("C:/MyPath/MyImageFile.jp2")
mimg.load_region_xyz([0,0,0],[100,150,1],0)
arr = np.array(mimg, copy = False)
print(arr.shape) #tczyx - note that the data is always returned in TCZYX order, even if the original image is 2D or 3D

# following loading, squeeze the numpy array
sqzar = np.squeeze(arr) # remove all "singleton" dimensions (i.e., dimensions with size = 1)
print(sqzar.shape) #cyx

# following squeezing, transpose the numpy array
tsar = sqzar.transpose(1,2,0)
print(tsar.shape) #yxc - this is the correct shape for saving as a PNG image using PIL

# finally, create a PIL image and save to disk as a PNG file
im = Image.fromarray(tsar, 'RGB')
im.save("C:/MyPath/PythonOUT.png")