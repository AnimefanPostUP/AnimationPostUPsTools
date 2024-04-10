import os
import glob

def insert_modules():
    print ("Running the module installer")
    # Define the start and end markers
    start_marker = "#MODULE_INSTALLER_SPACE_START_00000000" + os.linesep
    end_marker = "#MODULE_INSTALLER_SPACE_END_00000001" + os.linesep
    
    start_ignore = "#MODULE_INSTALLER_SPACE_START_IGNORE_0013000000" + os.linesep
    end_ignore = "#MODULE_INSTALLER_SPACE_END_IGNORE_0013000001" + os.linesep
    
    # Define the blacklist
    fileblacklist = ["__init__.py", "auto_load.py", "animationpostupstools.py", "function_names.py", "installer_mergefiles.py","module_animationfanpostupstools.py","animationfanpostup_placeholder.py"]
    # Get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))



    # Get all Python files in the current directory
    files = glob.glob(os.path.join(current_directory, "*.py"))

    # Filter out the blacklisted files
    files = [file for file in files if os.path.basename(file) not in fileblacklist]
    
    #sort them alphabetically including numbers
    files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

    #print the files with new lines for each file
    
    for file in files:
        print(file)

    # Read the target file
    module_file_path = os.path.join(current_directory, "module_animationfanpostupstools.py")
    
    print(f"Reading module file: {module_file_path}")
    
    
    with open(module_file_path, "r") as target_file:
        lines_module = target_file.readlines()
        
        #print with new lines
        for  line in lines_module:
            print(line)

    #overwrite all the content with the main module file
    target_file_path = os.path.join(current_directory, "animationpostupstools.py")
    print(f"Writing to target file: {target_file_path}")
    with open(target_file_path, "w") as target_file:
        target_file.writelines(lines_module)

    # Read the target file
    with open(target_file_path, "r") as target_file:
        lines = target_file.readlines()

    # Find the start and end markers
    print ("Finding the start and end markers")
    for index, line in enumerate(lines):
        #trim and compare the line
        line = line.strip()
        if line == start_marker.strip():
            start_index = index
        elif line == end_marker.strip():
            end_index = index
            break
    # Remove the old content between the markers
    del lines[start_index:end_index]
    

    start_ignore_index = -1
    end_ignore_index = -1    
        
        
    #list to store function names   
    function_names = []
    functions_module = []
    functionlinenumber = []
        
    # Insert the new content
    for file in files:
        with open(file, "r") as source_file:
            # Read the entire file content first
            file_content = source_file.read()

            # Split the content into lines for processing
            lines_in_file = file_content.split('\n')

            # Read line by line and store all the function names
            for line, line_number in zip(lines_in_file, range(len(lines_in_file))):
                if "def " in line:
                    function_name = line.split("def ")[1].split("(")[0]
                    function_names.append(line)
                    #get files name only
                    filename    = os.path.basename(file)
                    functions_module.append(filename)
                    functionlinenumber.append(line_number)
                    print(f"Function name: {function_name} in file: {file} at line: {line_number}")

            lines.insert(start_index, "\n")
            # Add a very large comment text 3 lines 
            lines.insert(start_index+1, "#"*100+"\n")
            # Title of the file
            lines.insert(start_index+2, "#"+os.path.basename(file)+"\n")
            lines.insert(start_index+3, "#"*100+"\n")

            lines.insert(start_index+4, "\n")

            # Insert the content of the file
            lines.insert(start_index+5, file_content)
            # Insert footer comment

            # Add extra line behind the module
            lines.insert(start_index+6, "\n")
            start_index += 7

        for index, line in enumerate(lines):
            line = line.strip()
            if line == start_ignore.strip():
                start_ignore_index = index
            elif line == end_ignore.strip():
                end_ignore_index = index
                break
        
    
                    
    if start_ignore_index != -1 and end_ignore_index != -1:
        #print the to delete content
        print ("Ignoring the content:")
        print ( line for line in lines[start_ignore_index:end_ignore_index])
        
        #Delete line by line
        for i in range(start_ignore_index, end_ignore_index+1):
            del lines[start_ignore_index]
            
        #add a comment to the line
       # lines.insert(start_ignore_index, "#CONTENT HERE WAS DELETED BY INSTALLER\n")
        print ("Ignoring the content between the ignore markers !")
        print (start_ignore_index)
        print (end_ignore_index)
    
    
    # Write the new content to the target file
    print(f"Writing to target file: {target_file_path}")
    with open(target_file_path, "w") as target_file:

        target_file.writelines(lines)
            
            
    # Clean the content of the ignore section between the markers that were detected earlier
    start_ignore_index = -1
    end_ignore_index = -1

    # Read the module file
    with open(module_file_path, "r") as module_file:
        lines_module = module_file.readlines()
        
        # Find the start and end markers
        for index, line in enumerate(lines_module):
            line = line.strip()
            if line == start_ignore.strip():
                start_ignore_index = index
            elif line == end_ignore.strip():
                end_ignore_index = index
                break
            
        # Remove the old content between the markers but not the markers themselves
        del lines_module[start_ignore_index+1:end_ignore_index]
        
        if start_ignore_index != -1 and end_ignore_index != -1:
            #print the to delete content
            print ("Ignoring the content:")
            print ('\n'.join(lines_module[start_ignore_index:end_ignore_index]))
            
        #write the dummy function names into the ignore section
        print(f"Writing to module_animationfanpostupstools file: {module_file_path}")
        with open(module_file_path, "w") as module_file:
            # write into the ignore section between the markers
            linestring = ""
            #replace \n from the name
            function_names = [name.replace("\n", "") for name in function_names]
            
            
            
            for i, name in enumerate(function_names):
                linestring = linestring+""+f"{name}  return \t'file: " + functions_module[i] + "    line: "+ str(functionlinenumber[i]) +"'\n"

            linestring=linestring+"\n"
            lines_module.insert(start_ignore_index +1, linestring)
            module_file.writelines(lines_module)
                                        
                                        
            
            
       
            
#run the function
insert_modules()