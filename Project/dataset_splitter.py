import os
import re
import shutil
# Define the patterns
patterns = [
    r"fs\d+_(\w+)_roi",  # Example: "fs446_bipinnariaroi2.3125587302.tif.png"
    r"training(\w+)_roi",  # Example: "training_pluteus_roi0.3479887900.tif.png"
]
# Define source and target paths
source_path = r"C:\ML_Dataset\original"
target_path = r"C:\ML_Dataset\split_full"
# Ensure the target directory exists
os.makedirs(target_path, exist_ok=True)

def get_class_name(filename):
    # Extract class name from the filename using the patterns
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            return match.group(1)
    return None

def organize_images():
    # Organize images into folders based on their class names
    # Iterate over all files in the source directory
    walk = os.walk(source_path)
    for root, dirs, files in walk:
        for file in files:
            # Extract the class name from the file name
            class_name = get_class_name(file)
            if class_name:
                # Create a folder for the class if it doesn't exist
                class_folder = os.path.join(target_path, class_name)
                os.makedirs(class_folder, exist_ok=True)

                # Move the file to the corresponding folder
                source_file = os.path.join(root, file)
                target_file = os.path.join(class_folder, file)
                shutil.move(source_file, target_file)

                print(f"Moved: {source_file} -> {target_file}")
            else:
                print(f"Skipped: {file} (No matching class)")

if __name__ == '__main__':
    organize_images()