import os


def rename_directories(path):
    for old_dir_name in os.listdir(path):
        if old_dir_name.startswith('_') and os.path.isdir(os.path.join(path, old_dir_name)):
            new_dir_name = old_dir_name[1:]  # remove the initial underscore
            old_dir_path = os.path.join(path, old_dir_name)
            new_dir_path = os.path.join(path, new_dir_name)

            os.rename(old_dir_path, new_dir_path)  # rename the directory
            print(f"The directory {old_dir_name} has been renamed to {new_dir_name}")


if __name__ == '__main__':
    dir_path = "C:/ML_Dataset/split_full/training"  # substitute with your actual directory path
    rename_directories(dir_path)