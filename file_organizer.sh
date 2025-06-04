#!/bin/bash
echo "Please enter the directory path to organize files:"
read source_dir

if [ ! -d "$source_dir" ]; then
        echo "Error: The directory does not exist or is not accessible."
        exit 1
fi

# Number of files transferred to each folder
declare -A file_count

for file in "$source_dir"/*; do
        if [ -f "$file" ]; then
                extension="${file##*.}"  # the end of the file

                # make dir by file extension
                mkdir -p "$source_dir/$extension"
                
                # Check if the file is already in the destination directory
                if [ "$file" != "$source_dir/$extension/$(basename "$file")" ]; then
                        # move the file to the appropriate extension folder
                        mv "$file" "$source_dir/$extension/"
                        
                        # Fix: use this syntax to update file_count array
                        file_count["$extension"]=$((file_count["$extension"] + 1))
                        
                        echo "Moved $file to $source_dir/$extension/"
                else
                        echo "Skipping $file as it is already in the destination folder."
                fi
        fi
done

# Print summary
echo -e "\nSummary of file organization:"
for extension in "${!file_count[@]}"; do
        echo "$extension: ${file_count[$extension]} files"
done

echo "file organization completed"
