import os
import shutil
import re
import subprocess

class AssemblyFileProcessor:
    """
    A class to handle operations related to creating an assembly file for .jpx compilation.
    """

    def __init__(self, source_directory, target_directory, assembly_info_file):
        """
        Initializes the AssemblyFileProcessor with the given directories and assembly info file.

        Args:
            source_directory (str): The directory containing .jpx files.
            target_directory (str): The directory where new folders will be created.
            assembly_info_file (str): The path to the assembly information file.
        """
        if not os.path.isdir(source_directory):
            raise ValueError(f"The provided source path '{source_directory}' is not a valid directory.")
        if not os.path.isdir(target_directory):
            raise ValueError(f"The provided target path '{target_directory}' is not a valid directory.")
        if not os.path.isfile(assembly_info_file):
            raise ValueError(f"The provided assembly info file '{assembly_info_file}' is not a valid file.")
        self.source_directory = source_directory
        self.target_directory = target_directory
        self.attempt_folder_path = None

        self.assembly_info = self.parse_info_file(assembly_info_file)
        self.assembly_data = {}

        self.attempt_folder_num = 1
        self.base_file_name = self.extract_base_name()

        self.trim_percentage = 0
        self.overlap_percentage = 0

        self.tile_coordinates = {}
        self.background_channel_filters = {}

        self.rows = 1
        self.columns = 1
        self.x_spacing = 1
        self.y_spacing = 1

    def parse_info_file(self, assembly_info_file):
        """
        Reads and parses a text file with information and stores it in a nested dictionary.

        Args:
            assembly_info_file (str): The path to the text file containing the information.

        Returns:
            dict: A nested dictionary containing the parsed information.
        """
        if not os.path.isfile(assembly_info_file):
            raise ValueError(f"The provided info file '{assembly_info_file}' is not a valid file.")

        parsed_data = {}
        current_section = None
        current_subsection = None
        previous_line = "";

        with open(assembly_info_file, 'r') as file:
            for line in file:
                # Skip blank lines
                if not line.strip():
                    continue

                # Check if the line is a new section (no tabs, e.g., "xyz-Table")
                if '\t' not in line:
                    current_section = line.strip()
                    parsed_data[current_section] = {}
                    current_subsection = None
                    continue

                # Check if the line is a subsection (starts with tabs, subsection title, ends with tab)
                # e.g. "    Z   ")
                if re.search("^\t*[^\t]*\t$", line):
                    try:
                        key, value = line.strip().split('\t', 1)
                        parsed_data[current_section][key.strip()] = value.strip()
                    except ValueError:
                        current_subsection = line.strip()
                        parsed_data[current_section][current_subsection] = {}
                        continue

                # Check if the line is a key-value pair (starts with tabs, key, tab, ends with value)
                if re.search("^\t*[^\t]*\t[^\t]*$", line):
                    key, value = line.strip().split('\t', 1)
                    if current_subsection:
                        parsed_data[current_section][current_subsection][key.strip()] = value.strip()
                    else:
                        parsed_data[current_section][key.strip()] = value.strip()
                        
        return parsed_data

    def extract_base_name(self):
        """
        Extracts the base name from the first .jpx file in the source directory.

        Returns:
            str: The base name of the first .jpx file.
        """
        for file_name in os.listdir(self.source_directory):
            if file_name.endswith('.jpx'):
                return os.path.splitext(file_name)[0].split('[')[0]
        raise ValueError("No .jpx files found in the source directory.")
        
    def extract_channel_name(self, file_name):
        """
        Extracts the channel name (i.e. C00) from the end of the .jpx file name.
        
        Returns:
            str: The channel name of the .jpx file
        """
        if file_name.endswith('.jpx'):
            return file_name.split('_')[-1]
        raise ValueError("Extract Channel Name: Filename is not a jpx file.")
        
    def extract_channel_names(self):
        """
        Extracts all the channel names from all the .jpx files in the source directory.
        
        Returns:
            list: All of the channel names
        """
        channel_names = []
        
        for file_name in os.listdir(self.source_directory):
            if file_name.endswith('.jpx'):
                channel_names.append(self.extract_channel_name(file_name))
                
        return channel_names

    def create_folders(self, base_name):
        """
        Creates a base folder and an attempt folder in the target directory, or uses an existing attempt folder.

        Args:
            base_name (str): The base name to use for the folder structure.

        Returns:
            str: The path to the attempt folder.
        """
        # Create the base folder
        base_folder_path = os.path.join(self.target_directory, base_name)
        if not os.path.exists(base_folder_path):
            os.makedirs(base_folder_path)

        # Check for an existing attempt folder
        for folder_name in sorted(os.listdir(base_folder_path)):
            attempt_folder_path = os.path.join(base_folder_path, folder_name)
            if os.path.isdir(attempt_folder_path) and folder_name.isdigit():
                self.attempt_folder_num = int(folder_name)
                self.attempt_folder_path = attempt_folder_path
                print(f"Using existing attempt folder: {self.attempt_folder_path}")
                return self.attempt_folder_path

        # Create a new attempt folder if none exists
        attempt_number = 1
        while True:
            attempt_folder_name = f"{attempt_number:04}"
            attempt_folder_path = os.path.join(base_folder_path, attempt_folder_name)
            
            if not os.path.exists(attempt_folder_path):
                os.makedirs(attempt_folder_path)
                self.attempt_folder_num = attempt_number
                self.attempt_folder_path = attempt_folder_path
                print(f"Created new attempt folder: {self.attempt_folder_path}")
                return self.attempt_folder_path
            attempt_number += 1

    def copy_files(self, attempt_folder_path):
        """
        Copies all .jpx files from the source directory to the attempt folder if they are not already present.

        Args:
            attempt_folder_path (str): The path to the attempt folder.
        """
        # Check for existing renamed files in the target directory
        existing_files = [file for file in os.listdir(attempt_folder_path) if re.match(r"\d{6}_\d{6}\.jpx", file)]

        if existing_files:
            print("Renamed files already exist in the target directory. Skipping copy.")
            return

        for file_name in os.listdir(self.source_directory):
            if file_name.endswith('.jpx'):
                source_file_path = os.path.join(self.source_directory, file_name)
                target_file_path = os.path.join(attempt_folder_path, file_name)
                if not os.path.exists(target_file_path):
                    shutil.copy(source_file_path, target_file_path)
                    print(f"Copied: {file_name}")
                else:
                    print(f"File already exists, skipping: {file_name}")

    def rename_jpx_files(self):
        """
        Renames all .jpx files in the target directory to a numerical order format starting with 000000_000001.jpx.
        """
        jpx_files = [file for file in os.listdir(self.attempt_folder_path) if file.endswith('.jpx')]
        jpx_files.sort()  # Sort files alphabetically to ensure consistent renaming order

        for index, file_name in enumerate(jpx_files):
            # Generate the new file name
            new_file_name = f"{0:06}_{index + 1:06}.jpx"
            source_file_path = os.path.join(self.attempt_folder_path, file_name)
            target_file_path = os.path.join(self.attempt_folder_path, new_file_name)

            # Rename the file
            os.rename(source_file_path, target_file_path)
            print(f"Renamed: {file_name} -> {new_file_name}")

    def process_directory_structure(self, multi_chan_acquire, compression_amount):
        """
        Orchestrates the entire process of creating folders, moving files, and generating the assembly file.
        """
        self.base_file_name = self.extract_base_name()
        attempt_folder_path = self.create_folders(self.base_file_name)
        if multi_chan_acquire:
            #C:\Python\MicroFile+ Distributable\Microfile+.exe
            args = [r'MicroFile+ Distributable\Microfile+.exe', '-multi', self.source_directory, attempt_folder_path, str(compression_amount)]
            subprocess.call(args)
        else:
            self.copy_files(attempt_folder_path)
        self.rename_jpx_files()

    def add_version(self):
        """
        Adds the version number derived from the attempt folder name to the assembly data dictionary.

        Args:
            attempt_folder_name (str): The name of the attempt folder (e.g., '001').
            assembly_data (dict): The dictionary containing the parsed assembly information.
        """
        self.assembly_data['Version'] = self.attempt_folder_num   

    def add_base_file_name(self):
        """
        Adds the base file name to the assembly data dictionary.

        Args:
            base_name (str): The base name of the .jpx files.
            assembly_data (dict): The dictionary containing the parsed assembly information.
        """
        self.assembly_data['Base File Name'] = self.base_file_name
        
    def add_planes_and_tiles(self):
        """
        Adds the number of planes and tiles to the assembly data dictionary.
        """
        try:
            # Safely access the nested dictionary keys
            plane_number = self.assembly_info.get("xyz-Table", {}).get("Z", {}).get("Number steps")
            if plane_number is None:
                raise KeyError("Number steps not found in xyz-Table -> Z")
            
            # Count the number of .jpx files in the source directory
            tile_number = len([file for file in os.listdir(self.source_directory) if file.endswith('.jpx')])

            # Add to the assembly data dictionary
            self.assembly_data['NumberOfPlanes'] = plane_number
            self.assembly_data['NumberOfTiles'] = tile_number
            
        except KeyError as e:
            print(f"Error accessing assembly info: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def add_grid_values(self):
        """
        Adds the grid values to the assembly data dictionary.
        """
        try:
            grid_x = int(self.assembly_info.get("xyz-Table", {}).get("X", {}).get("Number steps"))
            self.assembly_data['GridX'] = grid_x
            self.columns = grid_x  # Set columns to GridX

            grid_y = int(self.assembly_info.get("xyz-Table", {}).get("Y", {}).get("Number steps"))
            self.assembly_data['GridY'] = grid_y
            self.rows = grid_y  # Set rows to GridY
        except (TypeError, ValueError, KeyError) as e:
            raise ValueError(f"Error adding grid values: {e}")

    def add_background_fill(self):
        """
        Adds the background fill value to the assembly data dictionary.
        """
        background_fill = self.assembly_info.get("xyz-Table", {}).get("Background fill")
        if background_fill:
            self.assembly_data['BackgroundFillWhite'] = background_fill
        else:
            self.assembly_data['BackgroundFillWhite'] = 0
        
    def add_blend_size(self, blending_amount=None):
        """
        Adds the blend size to the assembly data dictionary.
        """
        if blending_amount is not None:
            self.assembly_data['BlendSize'] = blending_amount
        else:
            blend_size = self.assembly_info.get("Blend", {}).get("Size")
            if blend_size:
                self.assembly_data['BlendSize'] = blend_size
            else:
                self.assembly_data['BlendSize'] = 0
        
    def add_trim_sizes(self):
        """
        Adds the trim sizes to the assembly data dictionary.
        """
        try:
            # Absolute values instead of percentages now
            overlap_x_str = self.assembly_info.get("xyz-Table", {}).get("Overlap", {}).get("X")
            overlap_y_str = self.assembly_info.get("xyz-Table", {}).get("Overlap", {}).get("Y")
            
            if " %" in overlap_x_str and " %" in overlap_y_str:
                overlap_x_percent = int(overlap_x_str.replace(" %", ""));
                overlap_y_percent = int(overlap_y_str.replace(" %", ""));
                trim_x_percent = overlap_x_percent / 2;
                trim_y_percent = overlap_y_percent / 2;
                
                self.overlap_percentage = overlap_x_percent;
                self.trim_percentage = trim_x_percent;
                
                # Calculate the absolute values from percentages
                imgsize_x = self.assembly_info.get("Image sizes", {}).get("Blaze X")
                imgsize_x = remove_pixel(imgsize_x)
                imgsize_y = self.assembly_info.get("Image sizes", {}).get("Blaze Y")
                imgsize_y = remove_pixel(imgsize_y)
                
                trim_x = round(imgsize_x * trim_x_percent / 100)
                trim_y = round(imgsize_y * trim_y_percent / 100)
                
                self.assembly_data['TrimLeft'] = trim_x
                self.assembly_data['TrimRight'] = trim_x
                self.assembly_data['TrimTop'] = trim_y
                self.assembly_data['TrimBottom'] = trim_y
            else:
                overlap_x = int(self.assembly_info.get("xyz-Table", {}).get("Overlap", {}).get("X"))
                overlap_y = int(self.assembly_info.get("xyz-Table", {}).get("Overlap", {}).get("Y"))
                trim_x = round(overlap_x / 2)
                trim_y = round(overlap_y / 2)
                
                # Calculate the percentages from absolute values
                imgsize_x = self.assembly_info.get("Image sizes", {}).get("Blaze X")
                imgsize_x = remove_pixel(imgsize_x)
                
                self.overlap_percentage = overlap_x / imgsize_x * 100
                self.trim_percentage = trim_x / imgsize_x * 100

                self.assembly_data['TrimLeft'] = trim_x
                self.assembly_data['TrimRight'] = trim_x
                self.assembly_data['TrimTop'] = trim_y
                self.assembly_data['TrimBottom'] = trim_y
        except (TypeError, ValueError, KeyError) as e:
            raise ValueError(f"Error adding trim sizes: {e}")

    def add_tile_resolution_and_size(self):
        """
        Adds the tile resolution and size to the assembly data dictionary.
        """
        try:
            tile_resolution_x = self.assembly_info.get("Image sizes", {}).get("Blaze X")
            tile_resolution_x = remove_pixel(tile_resolution_x)
            self.assembly_data["TileResolutionX"] = tile_resolution_x

            tile_resolution_y = self.assembly_info.get("Image sizes", {}).get("Blaze Y")
            tile_resolution_y = remove_pixel(tile_resolution_y)
            self.assembly_data["TileResolutionY"] = tile_resolution_y

            tile_actual_size_x = tile_resolution_x - (2 * self.assembly_data['TrimLeft'])
            self.assembly_data["TileActualSizeX"] = tile_actual_size_x
            self.x_spacing = tile_actual_size_x

            tile_actual_size_y = tile_resolution_y - (2 * self.assembly_data['TrimTop'])
            self.assembly_data["TileActualSizeY"] = tile_actual_size_y
            self.y_spacing = tile_actual_size_y
        except (TypeError, ValueError, KeyError) as e:
            raise ValueError(f"Error adding tile resolution and size: {e}")

    def add_contour_id(self):
        """
        Adds the contour ID to the assembly data dictionary.
        """
        contour_id = self.assembly_info.get("Contour", {}).get("ID")
        if contour_id:
            self.assembly_data['ContourID'] = contour_id
        else:
            self.assembly_data['ContourID'] = 1  # Default value if not found

    def add_compression(self, compression_amount=None):
        """
        Adds the compression value to the assembly data dictionary.
        """
        if compression_amount is not None:
            self.assembly_data['Compression'] = compression_amount
        else:
            compression = self.assembly_info.get("Compression")
            if compression:
                self.assembly_data['Compression'] = compression
            else:
                self.assembly_data['Compression'] = 10 # This assumes comprehsion is set to 10 by default due to the .jpx files compiled in MicroFile+ app.

    def add_mbf_file_format(self):
        """
        Adds the MBF file format to the assembly data dictionary.
        """
        mbf_file_format = self.assembly_info.get("MBF File Format")
        if mbf_file_format:
            self.assembly_data['MBF File Format'] = mbf_file_format
        else:
            self.assembly_data['MBF File Format'] = 1

    def add_background_channels(self):
        """
        Adds the Background Channels to the assembly data dictionary with six default channels set to -1.0.
        """
        for i in range(1, 7):  # Loop through channels 1 to 6
            channel_key = f"Background Ch{i}"
            channel_value = self.assembly_info.get("xyz-Table", {}).get(channel_key, -1.0)
            self.assembly_data[channel_key] = float(channel_value)

    def add_background_target_rgb(self):
        """
        Adds the Background Target RGB to the assembly data dictionary with a default value of 1761627393.
        """
        background_target_rgb = self.assembly_info.get("xyz-Table", {}).get("Background Target RGB")
        if background_target_rgb:
            self.assembly_data['Background Target RGB'] = background_target_rgb
        else:
            self.assembly_data['Background Target RGB'] = 0

    def add_original_positions(self):
        """
        Adds the original positions to the assembly data dictionary.
        """
        try:
            original_position_x = self.assembly_info.get("xyz-Table", {}).get("X", {}).get("Start pos")
            original_position_y = self.assembly_info.get("xyz-Table", {}).get("Y", {}).get("Start pos")
            original_position_z = self.assembly_info.get("xyz-Table", {}).get("Z", {}).get("Start pos")

            original_position_x = remove_micron(original_position_x)
            original_position_y = remove_micron(original_position_y)
            original_position_z = remove_micron(original_position_z)

            self.assembly_data['OriginalPositionX'] = original_position_x
            self.assembly_data['OriginalPositionY'] = original_position_y
            self.assembly_data['OriginalPositionZ'] = original_position_z
        except (TypeError, ValueError, KeyError) as e:
            raise ValueError(f"Error adding original positions: {e}")

    def add_acquire_raw_stacks(self):
        """
        Adds the Acquire Raw Stacks value to the assembly data dictionary with a default value of 0.
        """
        acquire_raw_stacks = self.assembly_info.get("Acquire Raw Stacks")
        if acquire_raw_stacks is not None:
            self.assembly_data['Acquire Raw Stacks'] = acquire_raw_stacks
        else:
            self.assembly_data['Acquire Raw Stacks'] = 0    

    def add_max_raw_planes_per_file(self):
        """
        Adds the Max Raw Planes Per File value to the assembly data dictionary with a default value of 0.
        """
        max_raw_planes = self.assembly_info.get("Max Raw Planes Per File")
        if max_raw_planes is not None:
            self.assembly_data['Max Raw Planes Per File'] = max_raw_planes
        else:
            self.assembly_data['Max Raw Planes Per File'] = 0  # Default value
        
    def add_enable_blending(self, enable_blending_input=None):
        """
        Adds the Enable Blending value to the assembly data dictionary with a default value of 1.
        """
        if enable_blending_input is not None:
            self.assembly_data['Enable Blending'] = enable_blending_input
        else:
            enable_blending = self.assembly_info.get("Enable Blending")
            if enable_blending is not None:
                self.assembly_data['Enable Blending'] = enable_blending
            else:
                self.assembly_data['Enable Blending'] = 0  # Default value
        
    def add_multi_chan_acquire(self, multi_chan_acquire_input=None):
        """
        Adds the MultiChanAcquire value to the assembly data dictionary with a default value of 0.
        """
        if multi_chan_acquire_input is not None:
            self.assembly_data['MultiChanAcquire'] = multi_chan_acquire_input
        else:
            multi_chan_acquire = self.assembly_info.get("MultiChanAcquire")
            if multi_chan_acquire is not None:
                self.assembly_data['MultiChanAcquire'] = multi_chan_acquire
            else:
                self.assembly_data['MultiChanAcquire'] = 0  # Default value     

    def add_brightfield(self):
        """
        Adds the Brightfield value to the assembly data dictionary with a default value of 0.
        """
        brightfield = self.assembly_info.get("Brightfield")
        if brightfield is not None:
            self.assembly_data['Brightfield'] = brightfield
        else:
            self.assembly_data['Brightfield'] = 0  # Default value
        
    def add_save_mbf_format(self, mbf_format_input=None):
        """
        Adds the SaveMBFFormat value to the assembly data dictionary with a default value of 1.
        """
        if mbf_format_input is not None:
            self.assembly_data['SaveMBFFormat'] = mbf_format_input
        else:   
            save_mbf_format = self.assembly_info.get("SaveMBFFormat")
            if save_mbf_format is not None:
                self.assembly_data['SaveMBFFormat'] = save_mbf_format
            else:
                self.assembly_data['SaveMBFFormat'] = 1  # Default value
        
    # These two functions below are set to 0 by default and generally set using the GUI in the compiler. However they are set here for completeness and to keep format of the assembly file consistent.

    def add_do_stitching(self):
        """
        Adds the DoStitching value to the assembly data dictionary with a default value of 0.
        """
        self.assembly_data['DoStitching'] = 0  # Default value
        
    def add_restrict_stitching_to_xy(self):
        """
        Adds the RestrictStitchingToXY value to the assembly data dictionary with a default value of 0.
        """
        self.assembly_data['RestrictStitchingToXY'] = 0  # Default value

    def process_base_info(self, compression_amount=None, enable_blending=None, blending_amount=None, multi_chan_acquire=None, save_mbf_format=None):
        """
        Processes the base information from the assembly info file and adds it to the assembly data dictionary.
        """
        self.add_version()
        self.add_base_file_name()
        self.add_planes_and_tiles()
        self.add_grid_values()
        self.add_background_fill()
        self.add_blend_size(blending_amount)
        self.add_trim_sizes()
        self.add_tile_resolution_and_size()
        self.add_contour_id()
        self.add_compression(compression_amount)
        self.add_mbf_file_format()
        self.add_background_target_rgb()
        self.add_background_channels()
        self.add_original_positions()
        self.add_acquire_raw_stacks()
        self.add_max_raw_planes_per_file()
        self.add_enable_blending(enable_blending)
        self.add_multi_chan_acquire(multi_chan_acquire)
        self.add_brightfield()
        self.add_save_mbf_format(save_mbf_format)
        self.add_do_stitching()
        self.add_restrict_stitching_to_xy()

    # Code for manually adding image filters. Generally better to use the filters for FFC and background subtraction in the core apps supplier.

    def add_background_channel_filters(self, filter_info=1, active=None, valid=None, enable=None, diameters=None, flatfield_active=0, flatfield_enable_single=0, flatfield_enable=None):
        """
        Adds the [Channel Filters] section to the assembly data dictionary.
        Allows customization of Background Subtraction Diameter for each channel.

        Args:
            filter_info (int): The value for "Has Filter Information" (0 or 1).
            active (dict): A dictionary where keys are channel indices (0-5) and values are active status (0 or 1).
                            If None, default active status of 0 is used for all channels.
            valid (dict): A dictionary where keys are channel indices (0-5) and values are valid status (0 or 1).
                            If None, default valid status of 0 is used for all channels.
            enable (dict): A dictionary where keys are channel indices (0-5) and values are enable status (0 or 1).
                            If None, default enable status of 0 is used for all channels.
            diameters (dict): A dictionary where keys are channel indices (0-5) and values are diameters.
                            If None, default diameter of "10.0000" is used for all channels.
            flatfield_active (int): The value for "Flatfield Active" (0 or 1).
            flatfield_enable_single (int): The value for "Flatfield Enable Single" (0 or 1).
            flatfield_enable (dict): A dictionary where keys are channel indices (0-5) and values are enable status (0 or 1).
                            If None, default enable status of 0 is used for all channels.
        """
        self.background_channel_filters = {}

        default_active = 0
        default_enable = 0
        default_valid = 0
        default_diameter = "10.0000"
    
        channel_filters = {
            "Has Filter Information": filter_info,
            "Background Subtract Active": default_active,
            "Background Subtraction Enable Single": default_enable,
            "Background Subtraction Diameter Single": default_diameter,
        }

        # Add channel-specific data for channels 0 to 5
        for i in range(6):
            channel_filters[f"Channel Valid {i}"] = valid.get(i, default_valid) if valid else default_valid
            channel_filters[f"Background Subtraction Enable {i}"] = enable.get(i, default_enable) if enable else default_enable
            channel_filters[f"Background Subtraction Diameter {i}"] = diameters.get(i, default_diameter) if diameters else default_diameter

        default_flatfield_enable = 0

        # Add flatfield-specific data for channels 0 to 5
        channel_filters["Flatfield Active"] = flatfield_active
        channel_filters["Flatfield Enable Single"] = flatfield_enable_single
        for i in range(6):
            channel_filters[f"Flatfield Enable {i}"] = flatfield_enable.get(i, default_flatfield_enable) if flatfield_enable else default_flatfield_enable

        # Store the channel filters in the assembly data dictionary
        self.background_channel_filters = channel_filters

    def process_channel_filters(self):
        """
        Processes the channel filters and adds them to the assembly data dictionary.
        """

        self.add_background_channel_filters()

    def generate_tile_coordinates(self):
        """
        Generates tile coordinates in a left-to-right pattern based on the given rows (GridY), columns (GridX), and spacing.

        Args:
            None: Uses self.rows (GridY), self.columns (GridX), self.x_spacing, and self.y_spacing.

        Returns:
            None: Updates self.tile_coordinates with the generated coordinates.
        """
        tile_coordinates = {}

        # Generate coordinates for each tile
        tile_index = 0
        for row in range(self.rows):  # Iterate over rows (GridY)
            for col in range(self.columns):  # Iterate over columns (GridX)
                # Calculate X and Y positions
                tile_coordinates[f"Tile{tile_index}X"] = col * self.x_spacing  # X depends on the column
                tile_coordinates[f"Tile{tile_index}Y"] = row * self.y_spacing  # Y depends on the row
                tile_index += 1

        self.tile_coordinates = tile_coordinates
    
    def process_tile_info(self):
        """
        Processes the tile information and adds it to the assembly data dictionary.
        """
        self.generate_tile_coordinates()

    def write_assembly_file(self):
        """
        Writes the assembly.txt file in the attempt folder based on the parsed assembly data and tile coordinates.

        Args:
            attempt_folder_path (str): The path to the attempt folder.
        """
        assembly_file_path = os.path.normpath(os.path.join(self.attempt_folder_path, 'AssemblyData.txt'))

        with open(assembly_file_path, 'w') as file:
            # Write general assembly data
            file.write("[Virtual Tissue Stack Acquire Data]\n")
            for key, value in self.assembly_data.items():
                file.write(f"{key} = {value}\n")

            # Write tile coordinate data
            file.write("\n[Tile Coordinate Data]\n")
            for key, value in self.tile_coordinates.items():
                file.write(f"{key} = {value}\n")

        print(f"Assembly file written to: {assembly_file_path}")

def extract_percentage(value_str):
    """
    Extracts the percentage value from a string.

    Args:
        value_str (str): The input string containing a percentage (e.g., '22 % ( 65.78 µm )').

    Returns:
        int: The extracted percentage value as an integer.
    """
    # Use a regular expression to find the percentage value
    match = re.search(r"(\d+)\s*%", value_str)
    if match:
        return int(match.group(1))  # Convert the matched value to an integer
    else:
        raise ValueError(f"Could not extract a percentage from '{value_str}'")
    
def remove_micron(value_str):
    """
    Removes the unit 'µm' from the string and extracts the numeric value.

    Args:
        value_str (str): The input string (e.g., '-16819.02 µm').

    Returns:
        float: The numeric value as a float.
    """
    match = re.search(r"-?\d+(\.\d+)?", value_str)
    if match:
        return float(match.group())
    else:
        raise ValueError(f"Could not extract a numeric value from '{value_str}'")
    
def remove_pixel(value_str):
    """
    Removes the word 'pixel' from the string and extracts the numeric value.

    Args:
        value_str (str): The input string (e.g., '184 pixel').

    Returns:
        int: The numeric value as an integer.
    """
    match = re.search(r"\d+", value_str)
    if match:
        return int(match.group())
    else:
        raise ValueError(f"Could not extract a numeric value from '{value_str}'")

def main():
    """
    Main function to run the AssemblyFileProcessor.
    """
    print("Process assembly file. Please ensure all source files are in .jpx format for fast processing. Then follow the instructions below:")
    source_directory = input("Enter the source directory: ").strip()
    target_directory = input("Enter the target directory: ").strip()
    assembly_info_file = input("Enter the path to the measurement info .txt file: ").strip()

    # Loop until a valid response is provided
    while True:
        manually_add_info = input("Do you want to manually add additional information for blending, multichannel acquire, compression and file format? (yes/no): ").strip().lower()
        if manually_add_info in ["yes", "y"]:

            # Enable Blending
            enable_blending_input = input("Enable Blending? (yes/no): ").strip().lower()
            if enable_blending_input in ["yes", "y"]:
                enable_blending = 1
                set_blending_input = input("Enter blending amount pixels: ").strip().lower()
                if set_blending_input.isdigit():
                    blending_amount = int(set_blending_input)
                else:
                    print("Invalid input for blending amount. Defaulting to 0.")
                    blending_amount = 0
            elif enable_blending_input in ["no", "n"]:
                enable_blending = 0
                blending_amount = 0
            else:
                print("Invalid input for Enable Blending. Defaulting to 0 (no).")
                enable_blending = 0
                blending_amount = 0

            # Multi-Channel Acquire
            multi_chan_acquire_input = input("Enable Multi-Channel Acquire? (yes/no): ").strip().lower()
            if multi_chan_acquire_input in ["yes", "y"]:
                multi_chan_acquire = 1
            elif multi_chan_acquire_input in ["no", "n"]:
                multi_chan_acquire = 0
            else:
                print("Invalid input for Multi-Channel Acquire. Defaulting to 0 (no).")
                multi_chan_acquire = 0

            compression_input = input("Enter compression value (0-100). Enter nothing to default to 10 (MBF standard): ").strip()
            if compression_input.isdigit() and 0 <= int(compression_input) <= 100:
                compression_amount = int(compression_input)
            else:
                print("Defaulting to 10.")
                compression_amount = 10

            # Save MBF Format
            save_mbf_format_input = input("Enable Save MBF Format? (yes/no): ").strip().lower()
            if save_mbf_format_input in ["yes", "y"]:
                save_mbf_format = 1
            elif save_mbf_format_input in ["no", "n"]:
                save_mbf_format = 0
            else:
                print("Invalid input for Save MBF Format. Defaulting to 1.")
                save_mbf_format = 1

            break
        elif manually_add_info in ["no", "n"]:
            # Default values
            enable_blending = 0
            blending_amount = 0
            multi_chan_acquire = 0
            compression_amount = 10
            save_mbf_format = 1
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    try:
        processor = AssemblyFileProcessor(source_directory, target_directory, assembly_info_file)
        processor.process_directory_structure(multi_chan_acquire=multi_chan_acquire, compression_amount=compression_amount)
        processor.process_base_info(enable_blending=enable_blending, blending_amount=blending_amount, multi_chan_acquire=multi_chan_acquire, compression_amount=compression_amount, save_mbf_format=save_mbf_format)
        processor.process_tile_info()
        processor.write_assembly_file()
        print("Files have been organized and assembly.txt has been created successfully. Please use preview mode in image compiler to set filters and corrections.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()