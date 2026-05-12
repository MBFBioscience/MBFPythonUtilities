***Note:** While this only uses base python packages, we still recommend creating a virtual environment. Steps are outlined below.*

## Set Up

1. Navigate to the directory with assembly_file.py.

2. Using your preferred python package manager, create a virtual environment:

	```
	conda create --name my_env
	```

	OR in current directory:

	```
	python -m venv my_env
	```

3. Activate the environment:

	```
	conda activate my_env
	```

	OR in current directory:

	```
	my_env\Scripts\activate
	```

## Running the Script

1. Run the script with the following command:

	```
	python -u assembly_file.py
	```

2. Follow the instructions given in the prompt to generate the assembly file.

***Note:** Source directory is where the original jpx images are. Target directory is where you want the assembly file written. Path to .txt file is where the measurementInfo.txt file is.
Multiple runs will create a new directory each time, i.e. 00001, 000002. Deleting the folder will restart the numbering from 000001.* 


**EXAMPLE** 

1. ```conda create --name assembly_file```
2. ```conda activate assembly_file```
3. ```python -u assembly_file.py```

	> Process assembly file. Please ensure all source files are in .jpx
	> format for fast processing. Then follow the instructions below:
	> 
	> Enter the source directory:

	    G:/data/temp/assembly/raw_jpx_files

	> Enter the target directory:

	    G:/data/temp/assembly

	> Enter the path to the measurement info .txt file:

	    G:/data/temp/assembly/raw_jpx_files/measurementInfo.txt

	> Do you want to manually add additional information for blending,
	> multichannel acquire, compression and file format? (yes/no):

	    n
