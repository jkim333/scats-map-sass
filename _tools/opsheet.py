import re
import os
import zipfile
import shutil
from distutils.dir_util import copy_tree

folder_path = r'C:\Users\Jihyung\Downloads\Sheets 0-1999\0-1999'
output_directory = r'C:\Users\Jihyung\Downloads\Opsheets'

all_files_and_folders = os.listdir(folder_path)

filtered_files = []
filtered_folders = []

folder_pattern1 = re.compile('^\d\d\d\d$')
folder_pattern2 = re.compile('^\d\d\d\d_[a-zA-Z]+$')
tif_pattern = re.compile('^\d+\.tif$')
for i in all_files_and_folders:
    if os.path.isdir(os.path.join(folder_path, i)) and \
        (folder_pattern1.match(i) or folder_pattern2.match(i)):
        # folders that meet folder_pattern1 or folder_pattern2
        filtered_folders.append(i)
    elif not os.path.isdir(os.path.join(folder_path, i)) and \
        tif_pattern.match(i):
        # tif files
        filtered_files.append(i)

for file in filtered_files:
    site_id = str(int(file.split('.')[0]))

    tmp_folder = os.path.join(output_directory, site_id)
    os.mkdir(tmp_folder)

    # copy .tif files over
    shutil.copy(os.path.join(folder_path, file), os.path.join(tmp_folder, file))
    
    # zip the folder
    shutil.make_archive(os.path.join(output_directory, site_id), 'zip', tmp_folder)
    
    # delete folder
    shutil.rmtree(tmp_folder)

for folder in filtered_folders:
    site_id = str(int(folder.split('_')[0]))

    tmp_folder = os.path.join(output_directory, site_id)
    os.mkdir(tmp_folder)

    # copy folder over
    copy_tree(os.path.join(folder_path, folder), os.path.join(tmp_folder, folder))

    # copy file over
    file_name = f"{folder.split('_')[0]}.htm"
    shutil.copy(os.path.join(folder_path, file_name), os.path.join(tmp_folder, file_name))

    # zip the folder
    shutil.make_archive(os.path.join(output_directory, site_id), 'zip', tmp_folder)

    # delete folder
    shutil.rmtree(tmp_folder)
