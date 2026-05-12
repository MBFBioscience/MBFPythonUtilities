# ==================================================================================
# MBFPython REPL - AccessDisplayableImageData.py
# ==================================================================================
#
# PURPOSE:
#
#   This script demonstrates how to access "displayable" image data from any image
#	in a supported format (i.e., any image which can be opened in MBF applications).
#	The data returned will always be either 8-bit (1-channel Grayscale), or 24-bit
#   (3-channel RGB) and is suitable for visualization, publication, or export to
#   other image formats.
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

# create an instance of the "pyimg_display" class, for "displayable" image data
mimg = mbfimg.pyimg_display()

# initialize the created instance using one of three available methods:
#
# - "init_with_string" allows you to specify either the full file-path to an image
#                      on disk or just the filename. If using only the filename, the
#                      image must already be open in the associated MBF application.
#
# - "init_with_index" allows you to specify the index of an image to open. The index
#                     is zero-based and corresponds to the order listed inside image
#                     organizer in the associated MBF application.
#
# - "init_selected" allows you to initialize the image which is currently selected
#                     in the associated MBF application (highlighted in organizer)
# examples:
mimg.init_with_string("C:/MyPath/MyImageFile.jp2")
	# OR
mimg.init_with_index(0)
	# OR
mimg.init_selected()

# prior to loading image data, you should query the initialized image using one of
# the "size" methods for determining the full size of the image in each dimension:
mimg.img_sizes_xyzct()	# example return: [1972, 2258, 1, 3, 1]
mimg.size_x()			# example return: 1972
mimg.size_y()			# example return: 2258
mimg.size_z()			# example return: 1
mimg.size_c()			# example return: 3
mimg.size_t()			# example return: 1

# you can also query the number of bytes per pixel for both the source data and
# the loaded data (loaded "displayable" data will always be 8-bit or 24-bit, but
# the underlying data on disk could be, for example, an N-channel 16-bit image).
# Note: see AccessHighBitdepthImageData.py for examples on accessing this data.
mimg.bytes_per_pixel_source() # example return: 2
mimg.bytes_per_pixel_loaded() # example return: 1

# all images in MBF applications are multi-resolution, meaning that they have
# multiple levels of resolution available for loading. The number of levels can
# be queried using the "num_levels" method:"
mimg.num_levels() # example return: 5

# if you wish to know the available size of any given multi-resolution level,
# you can query the size of the associated dimension using one of the size
# methods and the desired level as an argument:
mimg.size_x(0) # example return: 1972
mimg.size_x(1) # example return: 986
mimg.size_x(2) # example return: 493
mimg.size_x(3) # example return: 247
mimg.size_x(4) # example return: 124
mimg.size_x(5) # example return: 0
# Note: as you can see: a *lower* index level means *higher* resolution data

# if you wish to accces metadata for an initialized image, you can do so using
# the "load_metadata" method, which returns a json string of all metadata:
mimg.load_metadata() # example return: '{"Info:SpacingX": "1.000000", ...}'

# you can also convert the returned json string to a Python dictionary:
python_dict = json.loads(mimg.load_metadata())
print(python_dict) # example return: {'Info:SpacingX': '1.000000', ...}

# for loading image data, you can use one of three available methods:
#
# - "load_region_xyz" accepts two [xyz] arrays for the region to be loaded,
#                     and the multi-resolution level to perform the load on;
#                     the first array being the pixel starting indices and 
#                     the second being the sizes of each dimension to load.
#                     Note: *all* channels and timepoints are loaded.
#
# - "load_region_xyzct" is identical to the above method, but allows you to
#                       also specify the C and T dimensions for this load.
#
# - "load_region" accepts a special "region" object for loading, which can
#                 be created using the "pyreg" and "pycoords" methods.

pos = mbfimg.pycoords(0,0,0,0,0)
siz = mbfimg.pycoords(100,100,1,1,1)
reg = mbfimg.pyreg(pos,siz,0)

print(pos) # example return: (x:0, y:0, z:0, c:0, t:0)
print(siz) # example return: (x:100, y:100, z:1, c:1, t:1)
print(reg) # example return: (pos:(x:0, y:0, z:0, c:0, t:0), sz:(x:100, y:100, z:1, c:1, t:1), lvl:0)

# the below calls all load the exact same region from resolution level 0 (highest resolution)
mimg.load_region_xyz([0,0,0], [100,100,1], 0)           # example return: True
mimg.load_region_xyzct([0,0,0,0,0], [100,100,1,1,1], 0) # example return: True
mimg.load_region(reg)                                   # example return: True

# following a load you can query for both the success of a load, and also the
# size of the loaded data using the "get_result" method. The latter is useful
# if you requested a region larger than exists in the source image; in that
# case we still perform the load, but only using available underlying data.
mimg.valid_result() # example return: True
reg = mimg.get_result()
print(reg) # example return: (pos:(x:0, y:0, z:0, c:0, t:0), sz:(x:100, y:100, z:1, c:3, t:1), lvl:0)

# to get access to the loaded data in a numpy array, send the loaded "mimg" object
# to the numpy array constructor. Note that the "copy=False" argument means no data
# copying will occur, and the returned array will be a direct reference to the loaded
# mimg object. You should take care to not perform another "load_region" using the
# mimg object while arr is being used; if required, use copy = True to create a deep
# copy of the data when creating the numpy array.
arr = np.array(mimg, copy = False)
print(arr.shape) # example return: (1, 3, 1, 100, 100)

print(arr)
# example return:
#[[[[[25 25 25 ... 25 25 25]
#    [25 25 25 ... 25 25 25]
#    [24 24 24 ... 24 24 24]
#    ...
#    [22 22 22 ... 22 22 22]
#    [22 22 22 ... 22 22 22]
#    [22 22 22 ... 22 22 22]]]
#
#  [[[25 25 25 ... 25 25 25]
#    [25 25 25 ... 25 25 25]
#    [25 25 25 ... 25 25 25]
#    ...
#    [27 27 27 ... 27 27 27]
#    [27 27 27 ... 27 27 27]
#    [27 27 27 ... 27 27 27]]]
#
#  [[[25 25 25 ... 27 27 27]
#    [25 25 25 ... 27 27 27]
#    [25 25 25 ... 27 27 27]
#    ...
#    [25 25 25 ... 27 27 27]
#    [25 25 25 ... 27 27 27]
#    [25 25 25 ... 27 27 27]]]]]