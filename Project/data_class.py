import os
import shutil


def move_files_with_word(source_dir, target_dir, word):
    # Ensure the target directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Iterate through files in the source directory
    for filename in os.listdir(source_dir):
        # Check if the word is in the file name
        if word in filename and "png" in filename:
            src_file_path = os.path.join(source_dir, filename)
            tgt_file_path = os.path.join(target_dir, filename)
            # Move the file to the target directory
            shutil.move(src_file_path, tgt_file_path)
            print(f"Moved: {filename}")


# Usage
source_directory = 'D:/ML_Dataset/processed/training'
target_directory = 'D:/ML_Dataset/processed/training/unknown'
specific_word = 'unknown'  # Replace with the word you're checking for

move_files_with_word(source_directory, target_directory, specific_word)

# {'rod', 'worms', 'snow', 'unknown', 'pteropods', 'polychaeta'}