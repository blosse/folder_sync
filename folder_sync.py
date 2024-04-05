### Test task for internal development in QA team at Veeam ###

# Step 1: Get CLI args
# Step 2: Check that src and dst folders exist
#         handle errors if not
# Step 3: Walk src dir and compare with dst
#         Handle missing file/dir
#         Handle outdated file/dir
# Step 4: Walk dst dir and check for files that
#         should not exist
# Step 5: Make sure sync function is called on
#         correct interval

import os
import shutil
import argparse

def check_files(src_dir, dst_dir, files) :
        # Check if file exists in dst_dir
        for file in files :
            src_file = os.path.join(src_dir, file)
            dst_file = os.path.join(dst_dir, file)
            if not os.path.exists(dst_file) or os.stat(src_file).st_mtime > os.stat(src_file).st_mtime :
                print("Something needs to be synced!")

def sync_folders(src_folder, dst_folder) :
    #Check that both folders exist
    if not os.path.isdir(src_folder) :
        raise ValueError(f"Source folder {src_folder} not found")
    if not os.path.isdir(dst_folder) :
        os.makedirs(dst_folder)

    #Walk src dir
    for src_dir, dir_names, files in os.walk(src_folder) :
        #Check if dirs exist in dst_folder
        for dir in dir_names :
            dst_dir = os.path.join(dst_folder, dir)
            print(f"Checking for dir: '{dst_dir}'")

            if not os.path.isdir(dst_dir) :
                os.makedirs(dst_dir)
                print(f"Dir not found, created new dir: {dst_dir}")

        for file in files :
            src_file = os.path.join(src_dir, file)
            dst_file = src_file.replace(src_folder, dst_folder, 1)
            print(f"Checking for file '{src_file}'")

            if not os.path.exists(dst_file) or os.stat(src_file).st_mtime > os.stat(src_file).st_mtime :
                print(f"File: '{dst_file}' not found")
                file_path = shutil.copy2(src_file, dst_file)
                print(f"Created file: '{file_path}'")

            #check_files(src_dir, dst_dir, files)
           
# Run the thing
def main() :
    
    # Step 1: Receive CLI args
    parser = argparse.ArgumentParser(description='Synchronize folders.')
    parser.add_argument('src', type=str, help='Source folder to sync from')
    parser.add_argument('dst', type=str, help='Destination folder to sync to') 
    parser.add_argument('interval', type=int, help='Interval between syncs in seconds')

    args = parser.parse_args()

    sync_folders(args.src, args.dst)

if __name__ == "__main__" :
    main()
