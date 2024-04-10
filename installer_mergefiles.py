import os
import glob

def insert_modules():
    # Define the start and end markers
    start_marker = "#MODULE_INSTALLER_SPACE_START_00000000\n"
    end_marker = "#MODULE_INSTALLER_SPACE_END_00000001\n"

    # Define the blacklist
    fileblacklist = ["__init__.py", "auto_load.py", "animationpostupstools.py", "function_names.py", "installer_mergefiles.py","module_animationfanpostupstools.py","animationfanpostup_placeholder.py"]
    # Get the current directory
    current_directory = os.path.dirname(__file__)

    # Get all Python files in the current directory
    files = glob.glob(os.path.join(current_directory, "*.py"))

    # Filter out the blacklisted files
    files = [file for file in files if os.path.basename(file) not in fileblacklist]

    # Read the target file
    #with open("animationpostupstools.py", "r") as target_file:
    #lines = target_file.readlines()
        
    #read the main module file
    with open("module_animationfanpostupstools.py", "r") as target_file:
        lines_module = target_file.readlines()

    #overwrite all the content with the main module file
    with open("animationpostupstools.py", "w") as target_file:
        target_file.writelines(lines_module)
        
    # Read the target fil
    with open("animationpostupstools.py", "r") as target_file:
        lines = target_file.readlines()

    # Find the start and end markers
    start_index = lines.index(start_marker) + 1
    end_index = lines.index(end_marker)

    # Remove the old content between the markers
    del lines[start_index:end_index]

    # Insert the new content
    for file in files:
        with open(file, "r") as source_file:
            #insert header commment with the file name
            lines.insert(start_index, "#"+os.path.basename(file)+"\n")
            lines.insert(start_index, source_file.read())
            start_index += 1
            #inster footer comment
            lines.insert(start_index, "#"+os.path.basename(file)+"\n")

    # Write the modified content back to the target file
    with open("animationpostupstools.py", "w") as target_file:
        target_file.writelines(lines)