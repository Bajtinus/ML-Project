import os
import shutil


file_names = set()

for filename in os.listdir('D:/ML_Dataset/processed/training'):
    if "png" not in filename:
        continue
    name = filename.split('_')[1]
    file_names.add(name)

print(file_names)

