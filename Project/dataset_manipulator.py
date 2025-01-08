"""
These functions are used to create sub datasets from the original.
It then creates new subsets within the "subsets" directory of the root.
The folder structure before running anything should look like this:
- root
    - original
        - images
        - ...
It then adds the following structure:
- root
    - split_full
        - training
            - actinotrocha
            - amphipods
            - ...
        - test
            - actinotrocha
            - amphipods
            - ...
    - subsets
        - equal_dist_1000 (only training images)
            - actinotrocha
            - amphipods
            - ...
        - div_by_50
            - actinotrocha
            - amphipods
            - ...
        - etc..

"""

import os
import re
import shutil

# TODO: Change this to your dataset parent directory
dataset_parent = "D:/ML_Dataset"

# Relative path definitions
source_path = f"{dataset_parent}/original"
subset_root = f"{dataset_parent}/subsets"
split_dataset = f"{dataset_parent}/split_full"
training_path = f"{dataset_parent}/split_full/training"

# Regex patterns for extracting class names from the file names
patterns = [
    r"fs\d+_(\w+)_roi",  # Example: "fs446_bipinnariaroi2.3125587302.tif.png"
    r"training(\w+)_roi",  # Example: "training_pluteus_roi0.3479887900.tif.png"
]


def copy_with_rename(src, dst):
    """
    Copies the file from src to dst, renaming it if the file already exists.
    """
    base, extension = os.path.splitext(dst)
    counter = 1
    new_dst = dst
    while os.path.exists(new_dst):
        new_dst = f"{base}_{counter}{extension}"
        counter += 1
    shutil.copy(src, new_dst)




def get_class_name(filename):
    """
    Extracts the class name from the filename using the patterns.
    """
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            return match.group(1)
    return None


def organize_images():
    """
    Splits the dataset into training and test sets. And further splits them into classes based on image names.
    """
    split_training = os.path.join(split_dataset, "training")
    split_test = os.path.join(split_dataset, "test")

    os.makedirs(split_training, exist_ok=True)
    os.makedirs(split_test, exist_ok=True)
    walk = os.walk(source_path)
    for root, dirs, files in walk:
        for file in files:
            # Extract the class name from the file name
            class_name = get_class_name(file)
            if not class_name:
                print(f"Skipped: {file} (No matching class)")
                continue
            elif class_name[0] == "_":
                class_folder = os.path.join(split_training, class_name[1:])
            else:
                class_folder = os.path.join(split_test, class_name)
            os.makedirs(class_folder, exist_ok=True)

            # copy the file to the corresponding folder
            source_file = os.path.join(root, file)
            target_file = os.path.join(class_folder, file)
            shutil.copy(source_file, target_file)



def equalize_dataset(samples_per_class):
    """
    Increases the amount of samples of each class to a fixed number.
    If the class is underrepresented, the samples are repeated such that there are about the same amount of copies of each image.
    If the class is overrepresented, the first x samples are selected.
    """
    output_path = f"{subset_root}/equal_dist_{samples_per_class}"
    split_training = os.path.join(split_dataset, "training")

    for folder in os.listdir(split_training):
        files = os.listdir(f'{split_training}/{folder}')
        count = len(files)
        os.makedirs(f"{output_path}/{folder}", exist_ok=True)
        # select the first x samples, if more than x
        # else, copy all and repeat until x sample
        for i in range(samples_per_class):
            file = files[i % count]
            copy_with_rename(f'{training_path}/{folder}/{file}', f"{output_path}/{folder}/{file}")


def divide_dataset(division_factor):
    """
    Reduces the amount of samples of each class by a factor.
    With a large factor, this may result in some classes having very few or no samples due to the imbalance of the dataset.
    """
    output_path = f"{subset_root}/div_by_{division_factor}"

    for folder in os.listdir(training_path):
        count = len(os.listdir(f'{training_path}/{folder}'))
        # copy the first count / 1000 files
        os.makedirs(f"{output_path}/{folder}", exist_ok=True)
        for i, filename in enumerate(os.listdir(f'{training_path}/{folder}')):
            if i >= count // division_factor:
                break
            src_file_path = os.path.join(f'{training_path}/{folder}', filename)
            tgt_file_path = os.path.join(f"{output_path}/{folder}", filename)
            shutil.copy(src_file_path, tgt_file_path)
            print(f"Moved: {filename}")


def main():
    """
    Use the functions to organize the dataset into subsets
    Make sure you have run organize_images() before creating any other subsets.
    WARNING: Due to copying about 220,000 files, worth of over 8GB, organize_images() may takes some time.
    Depending on the parameters you choose, the other functions may take a while as well.
    """
    equalize_dataset(100)


if __name__ == '__main__':
    main()