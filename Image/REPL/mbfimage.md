Python: module mbfimage

**mbfimage**

mbfimage module for exposing pyimg class types to Python
   
**Classes**

[pycoords](mbfimage.html#pycoords)

[pyimg\_base](mbfimage.html#pyimg_base)

[pyimg\_data](mbfimage.html#pyimg_data)

[pyimg\_display](mbfimage.html#pyimg_display)

[pyreg](mbfimage.html#pyreg)


class **pycoords**

Method resolution order:

[pycoords](mbfimage.html#pycoords)

* * *

Methods defined here:  

**\_\_init\_\_**(...)

[\_\_init\_\_](#pycoords-__init__)(\*args, \*\*kwargs)  
Overloaded function.  
   
1. [\_\_init\_\_](#pycoords-__init__)(self: mbfimage.[pycoords](#pycoords)) -> None  
   
Construct a new empty instance  
   
2. [\_\_init\_\_](#pycoords-__init__)(self: mbfimage.[pycoords](#pycoords), arg0: typing.SupportsInt | typing.SupportsIndex, arg1: typing.SupportsInt | typing.SupportsIndex, arg2: typing.SupportsInt | typing.SupportsIndex, arg3: typing.SupportsInt | typing.SupportsIndex, arg4: typing.SupportsInt | typing.SupportsIndex) -> None  
   
Construct a new instance with specified coordinates

**\_\_str\_\_**(...)

[\_\_str\_\_](#pycoords-__str__)(self: mbfimage.[pycoords](#pycoords)) -> str

**arr**(...)

[arr](#pycoords-arr)(self: mbfimage.[pycoords](#pycoords)) -> typing.Annotated\[list\[int\], "FixedSize(5)"\]  
   
Return list of coordinates \[XYZCT\]

* * *

Static methods inherited from :  

**\_\_new\_\_**(\*args, \*\*kwargs) class method of

Create and return a new object.  See help(type) for accurate signature.

class **pyimg\_base**

Method resolution order:

[pyimg\_base](mbfimage.html#pyimg_base)

* * *

Methods defined here:  

**\_\_init\_\_**(...)

[\_\_init\_\_](#pyimg_base-__init__)(self: mbfimage.[pyimg\_base](#pyimg_base)) -> None  
   
Construct a new empty instance

* * *

Static methods inherited from :  

**\_\_new\_\_**(\*args, \*\*kwargs) class method of

Create and return a new object.  See help(type) for accurate signature.

class **pyimg\_data**([pyimg\_base](mbfimage.html#pyimg_base))

Method resolution order:

[pyimg\_data](mbfimage.html#pyimg_data)

[pyimg\_base](mbfimage.html#pyimg_base)

* * *

Methods defined here:  

**\_\_buffer\_\_**(self, flags, /)

Return a buffer object that exposes the underlying memory of the object.

**\_\_init\_\_**(...)

[\_\_init\_\_](#pyimg_data-__init__)(self: mbfimage.[pyimg\_data](#pyimg_data)) -> None  
   
Construct a new empty instance

**\_\_release\_buffer\_\_**(self, buffer, /)

Release the buffer object that exposes the underlying memory of the object.

**bytes\_per\_pixel\_loaded**(...)

[bytes\_per\_pixel\_loaded](#pyimg_data-bytes_per_pixel_loaded)(self: mbfimage.[pyimg\_data](#pyimg_data)) -> int  
   
Return the size in bytes-per-pixel for loaded data \[updated during load\_region calls\]

**bytes\_per\_pixel\_source**(...)

[bytes\_per\_pixel\_source](#pyimg_data-bytes_per_pixel_source)(self: mbfimage.[pyimg\_data](#pyimg_data)) -> int  
   
Return the size in bytes-per-pixel for source image

**debug\_output**(...)

[debug\_output](#pyimg_data-debug_output)(self: mbfimage.[pyimg\_data](#pyimg_data), arg0: bool) -> None  
   
Enable debugging output

**get\_force\_16bit**(...)

[get\_force\_16bit](#pyimg_data-get_force_16bit)(self: mbfimage.[pyimg\_data](#pyimg_data)) -> bool  
   
Get force data setting to always be returned in 16-bit space \[even if source data is <= 8-bit\]

**get\_result**(...)

[get\_result](#pyimg_data-get_result)(self: mbfimage.[pyimg\_data](#pyimg_data)) -> mbfimage.[pyreg](#pyreg)  
   
Get result from last call to load\_region \[returned object methods: pos, sz, lvl\]

**img\_sizes\_xyzct**(...)

[img\_sizes\_xyzct](#pyimg_data-img_sizes_xyzct)(self: mbfimage.[pyimg\_data](#pyimg_data)) -> typing.Annotated\[list\[int\], "FixedSize(5)"\]  
   
Returns list of sizes \[XYZCT\]

**init\_selected**(...)

[init\_selected](#pyimg_data-init_selected)(self: mbfimage.[pyimg\_data](#pyimg_data)) -> bool  
   
Initialize using selected image in associated application \[e.g., selected image in image organizer\]

**init\_with\_index**(...)

[init\_with\_index](#pyimg_data-init_with_index)(self: mbfimage.[pyimg\_data](#pyimg_data), idx: typing.SupportsInt | typing.SupportsIndex) -> bool  
   
Initialize using index of an image already opened in associated application \[e.g. 1, 2, 3, ...\]

**init\_with\_string**(...)

[init\_with\_string](#pyimg_data-init_with_string)(self: mbfimage.[pyimg\_data](#pyimg_data), path: str) -> bool  
   
Initialize using name of image already opened in associated application \[e.g. "image.jpx"\] or path to file on disk \[e.g. "C:/path/to/image.jpx"\]

**load\_metadata**(...)

[load\_metadata](#pyimg_data-load_metadata)(self: mbfimage.[pyimg\_data](#pyimg_data)) -> str  
   
Load associated image metadata and return in json format

**load\_region**(...)

[load\_region](#pyimg_data-load_region)(self: mbfimage.[pyimg\_data](#pyimg_data), reg: mbfimage.[pyreg](#pyreg)) -> bool  
   
Perform load on initialized image

**load\_region\_xyz**(...)

[load\_region\_xyz](#pyimg_data-load_region_xyz)(self: mbfimage.[pyimg\_data](#pyimg_data), pos: typing.Annotated\[collections.abc.Sequence\[typing.SupportsInt | typing.SupportsIndex\], "FixedSize(3)"\] = \[0, 0, 0\], sz: typing.Annotated\[collections.abc.Sequence\[typing.SupportsInt | typing.SupportsIndex\], "FixedSize(3)"\], lvl: typing.SupportsInt | typing.SupportsIndex = 0) -> bool  
   
Perform load on initialized image

**load\_region\_xyzct**(...)

[load\_region\_xyzct](#pyimg_data-load_region_xyzct)(self: mbfimage.[pyimg\_data](#pyimg_data), pos: typing.Annotated\[collections.abc.Sequence\[typing.SupportsInt | typing.SupportsIndex\], "FixedSize(5)"\] = \[0, 0, 0, 0, 0\], sz: typing.Annotated\[collections.abc.Sequence\[typing.SupportsInt | typing.SupportsIndex\], "FixedSize(5)"\], lvl: typing.SupportsInt | typing.SupportsIndex = 0) -> bool  
   
Perform load on initialized image

**load\_timeout\_seconds**(...)

[load\_timeout\_seconds](#pyimg_data-load_timeout_seconds)(self: mbfimage.[pyimg\_data](#pyimg_data), val: typing.SupportsInt | typing.SupportsIndex) -> None  
   
Assign max-time in seconds to wait for loads to complete before error state \[0 will wait indefinitely\]

**num\_levels**(...)

[num\_levels](#pyimg_data-num_levels)(self: mbfimage.[pyimg\_data](#pyimg_data)) -> int  
   
Returns the number of pyramidal resolution levels in the image

**set\_force\_16bit**(...)

[set\_force\_16bit](#pyimg_data-set_force_16bit)(self: mbfimage.[pyimg\_data](#pyimg_data), force: bool) -> None  
   
Force data to always be returned in 16-bit space \[even if source data is <= 8-bit\]

**size\_c**(...)

[size\_c](#pyimg_data-size_c)(self: mbfimage.[pyimg\_data](#pyimg_data)) -> int  
   
Returns the number of channels in the image

**size\_t**(...)

[size\_t](#pyimg_data-size_t)(self: mbfimage.[pyimg\_data](#pyimg_data)) -> int  
   
Returns the number of time points in the image

**size\_x**(...)

[size\_x](#pyimg_data-size_x)(self: mbfimage.[pyimg\_data](#pyimg_data), lvl: typing.SupportsInt | typing.SupportsIndex = 0) -> int  
   
Returns the width in pixels of initialized image at the specified pyramid level \[e.g., [size\_x](#pyimg_data-size_x)(0)\]

**size\_y**(...)

[size\_y](#pyimg_data-size_y)(self: mbfimage.[pyimg\_data](#pyimg_data), lvl: typing.SupportsInt | typing.SupportsIndex = 0) -> int  
   
Returns the height in pixels of initialized image at the specified pyramid level \[e.g., [size\_y](#pyimg_data-size_y)(0)\]

**size\_z**(...)

[size\_z](#pyimg_data-size_z)(self: mbfimage.[pyimg\_data](#pyimg_data)) -> int  
   
Returns the depth in pixels of initialized image

**valid\_result**(...)

[valid\_result](#pyimg_data-valid_result)(self: mbfimage.[pyimg\_data](#pyimg_data)) -> bool  
   
Return true or false if last load\_region call returned valid data

* * *

Static methods inherited from :  

**\_\_new\_\_**(\*args, \*\*kwargs) class method of

Create and return a new object.  See help(type) for accurate signature.

class **pyimg\_display**([pyimg\_base](mbfimage.html#pyimg_base))

Method resolution order:

[pyimg\_display](mbfimage.html#pyimg_display)

[pyimg\_base](mbfimage.html#pyimg_base)

* * *

Methods defined here:  

**\_\_buffer\_\_**(self, flags, /)

Return a buffer object that exposes the underlying memory of the object.

**\_\_init\_\_**(...)

[\_\_init\_\_](#pyimg_display-__init__)(self: mbfimage.[pyimg\_display](#pyimg_display)) -> None  
   
Construct a new empty instance

**\_\_release\_buffer\_\_**(self, buffer, /)

Release the buffer object that exposes the underlying memory of the object.

**bytes\_per\_pixel\_loaded**(...)

[bytes\_per\_pixel\_loaded](#pyimg_display-bytes_per_pixel_loaded)(self: mbfimage.[pyimg\_display](#pyimg_display)) -> int  
   
Return the size in bytes-per-pixel for loaded data \[updated during load\_region calls\]

**bytes\_per\_pixel\_source**(...)

[bytes\_per\_pixel\_source](#pyimg_display-bytes_per_pixel_source)(self: mbfimage.[pyimg\_display](#pyimg_display)) -> int  
   
Return the size in bytes-per-pixel for source image

**debug\_output**(...)

[debug\_output](#pyimg_display-debug_output)(self: mbfimage.[pyimg\_display](#pyimg_display), arg0: bool) -> None  
   
Enable debugging output

**get\_force\_16bit**(...)

[get\_force\_16bit](#pyimg_display-get_force_16bit)(self: mbfimage.[pyimg\_display](#pyimg_display)) -> bool  
   
Get force data setting to always be returned in 16-bit space \[even if source data is <= 8-bit\]

**get\_result**(...)

[get\_result](#pyimg_display-get_result)(self: mbfimage.[pyimg\_display](#pyimg_display)) -> mbfimage.[pyreg](#pyreg)  
   
Get result from last call to load\_region \[returned object methods: pos, sz, lvl\]

**img\_sizes\_xyzct**(...)

[img\_sizes\_xyzct](#pyimg_display-img_sizes_xyzct)(self: mbfimage.[pyimg\_display](#pyimg_display)) -> typing.Annotated\[list\[int\], "FixedSize(5)"\]  
   
Returns list of sizes \[XYZCT\]

**init\_selected**(...)

[init\_selected](#pyimg_display-init_selected)(self: mbfimage.[pyimg\_display](#pyimg_display)) -> bool  
   
Initialize using selected image in associated application \[e.g., selected image in image organizer\]

**init\_with\_index**(...)

[init\_with\_index](#pyimg_display-init_with_index)(self: mbfimage.[pyimg\_display](#pyimg_display), idx: typing.SupportsInt | typing.SupportsIndex) -> bool  
   
Initialize using index of an image already opened in associated application \[e.g. 1, 2, 3, ...\]

**init\_with\_string**(...)

[init\_with\_string](#pyimg_display-init_with_string)(self: mbfimage.[pyimg\_display](#pyimg_display), path: str) -> bool  
   
Initialize using name of image already opened in associated application \[e.g. "image.jpx"\] or path to file on disk \[e.g. "C:/path/to/image.jpx"\]

**load\_metadata**(...)

[load\_metadata](#pyimg_display-load_metadata)(self: mbfimage.[pyimg\_display](#pyimg_display)) -> str  
   
Load associated image metadata and return in json format

**load\_region**(...)

[load\_region](#pyimg_display-load_region)(self: mbfimage.[pyimg\_display](#pyimg_display), reg: mbfimage.[pyreg](#pyreg)) -> bool  
   
Perform load on initialized image

**load\_region\_xyz**(...)

[load\_region\_xyz](#pyimg_display-load_region_xyz)(self: mbfimage.[pyimg\_display](#pyimg_display), pos: typing.Annotated\[collections.abc.Sequence\[typing.SupportsInt | typing.SupportsIndex\], "FixedSize(3)"\] = \[0, 0, 0\], sz: typing.Annotated\[collections.abc.Sequence\[typing.SupportsInt | typing.SupportsIndex\], "FixedSize(3)"\], lvl: typing.SupportsInt | typing.SupportsIndex = 0) -> bool  
   
Perform load on initialized image

**load\_region\_xyzct**(...)

[load\_region\_xyzct](#pyimg_display-load_region_xyzct)(self: mbfimage.[pyimg\_display](#pyimg_display), pos: typing.Annotated\[collections.abc.Sequence\[typing.SupportsInt | typing.SupportsIndex\], "FixedSize(5)"\] = \[0, 0, 0, 0, 0\], sz: typing.Annotated\[collections.abc.Sequence\[typing.SupportsInt | typing.SupportsIndex\], "FixedSize(5)"\], lvl: typing.SupportsInt | typing.SupportsIndex = 0) -> bool  
   
Perform load on initialized image

**load\_timeout\_seconds**(...)

[load\_timeout\_seconds](#pyimg_display-load_timeout_seconds)(self: mbfimage.[pyimg\_display](#pyimg_display), val: typing.SupportsInt | typing.SupportsIndex) -> None  
   
Assign max-time in seconds to wait for loads to complete before error state \[0 will wait indefinitely\]

**num\_levels**(...)

[num\_levels](#pyimg_display-num_levels)(self: mbfimage.[pyimg\_display](#pyimg_display)) -> int  
   
Returns the number of pyramidal resolution levels in the image

**set\_force\_16bit**(...)

[set\_force\_16bit](#pyimg_display-set_force_16bit)(self: mbfimage.[pyimg\_display](#pyimg_display), force: bool) -> None  
   
Force data to always be returned in 16-bit space \[even if source data is <= 8-bit\]

**size\_c**(...)

[size\_c](#pyimg_display-size_c)(self: mbfimage.[pyimg\_display](#pyimg_display)) -> int  
   
Returns the number of channels in the image

**size\_t**(...)

[size\_t](#pyimg_display-size_t)(self: mbfimage.[pyimg\_display](#pyimg_display)) -> int  
   
Returns the number of time points in the image

**size\_x**(...)

[size\_x](#pyimg_display-size_x)(self: mbfimage.[pyimg\_display](#pyimg_display), lvl: typing.SupportsInt | typing.SupportsIndex = 0) -> int  
   
Returns the width in pixels of initialized image at the specified pyramid level \[e.g., [size\_x](#pyimg_display-size_x)(0)\]

**size\_y**(...)

[size\_y](#pyimg_display-size_y)(self: mbfimage.[pyimg\_display](#pyimg_display), lvl: typing.SupportsInt | typing.SupportsIndex = 0) -> int  
   
Returns the height in pixels of initialized image at the specified pyramid level \[e.g., [size\_y](#pyimg_display-size_y)(0)\]

**size\_z**(...)

[size\_z](#pyimg_display-size_z)(self: mbfimage.[pyimg\_display](#pyimg_display)) -> int  
   
Returns the depth in pixels of initialized image

**valid\_result**(...)

[valid\_result](#pyimg_display-valid_result)(self: mbfimage.[pyimg\_display](#pyimg_display)) -> bool  
   
Return true or false if last load\_region call returned valid data

* * *

Static methods inherited from :  

**\_\_new\_\_**(\*args, \*\*kwargs) class method of

Create and return a new object.  See help(type) for accurate signature.

class **pyreg**

Method resolution order:

[pyreg](mbfimage.html#pyreg)

* * *

Methods defined here:  

**\_\_init\_\_**(...)

[\_\_init\_\_](#pyreg-__init__)(\*args, \*\*kwargs)  
Overloaded function.  
   
1. [\_\_init\_\_](#pyreg-__init__)(self: mbfimage.[pyreg](#pyreg)) -> None  
   
Construct a new empty instance  
   
2. [\_\_init\_\_](#pyreg-__init__)(self: mbfimage.[pyreg](#pyreg), arg0: mbfimage.[pycoords](#pycoords), arg1: mbfimage.[pycoords](#pycoords), arg2: typing.SupportsInt | typing.SupportsIndex) -> None  
   
Construct a new instance with specified region and level

**\_\_str\_\_**(...)

[\_\_str\_\_](#pyreg-__str__)(self: mbfimage.[pyreg](#pyreg)) -> str

**lvl**(...)

[lvl](#pyreg-lvl)(self: mbfimage.[pyreg](#pyreg)) -> int  
   
Return level

**pos**(...)

[pos](#pyreg-pos)(self: mbfimage.[pyreg](#pyreg)) -> typing.Annotated\[list\[int\], "FixedSize(5)"\]  
   
Return list of positions \[XYZCT\]

**size**(...)

[size](#pyreg-size)(self: mbfimage.[pyreg](#pyreg)) -> typing.Annotated\[list\[int\], "FixedSize(5)"\]  
   
Return list of sizes \[XYZCT\]

* * *

Static methods inherited from :  

**\_\_new\_\_**(\*args, \*\*kwargs) class method of

Create and return a new object.  See help(type) for accurate signature.