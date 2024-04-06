### Test task for internal development in QA team at Veeam ###

# This program syncs all files in a source folder to a destination
# on a given interval.

import os
import shutil
import argparse
import logging
from time import sleep

def folders_exist(src_folder, dst_folder) :
    #Check that both folders exist
    if not os.path.isdir(src_folder) :
        logging.warningf(f"Source folder {src_folder} not found")
        #raise ValueError(f"Source folder {src_folder} not found")
    if not os.path.isdir(dst_folder) :
        try : 
            os.makedirs(dst_folder)
            logging.info(f"Destination folder not found, '{dst_folder}' generated")
        except Exception as e :
            logging.error(f"An error occurred: {str(e)}")

def clean_folders(src_folder, dst_folder) :
    #print(f"Removing outdated files from '{src_folder}'.")

    for src_dir, dir_names, files in os.walk(src_folder) :
        
        for dir in dir_names :
            src = os.path.join(src_dir, dir)
            dst_dir = src.replace(src_folder, dst_folder, 1)
            #print(f"Checking for dir: '{dst_dir}'")

            if not os.path.isdir(dst_dir) :
                logging.debug(f"Directory: '{dst_dir}' not found, removing")
                #print(f"Directory: '{dst_dir}' not found, removing")
                try :
                    shutil.rmtree(src)
                    logging.info(f"Directory '{src}' successfully removed")
                except Exception as e :
                    logging.error(f"An error occurred when removing '{src}': {str(e)}")

        for file in files :
            src_file = os.path.join(src_dir, file)
            dst_file = src_file.replace(src_folder, dst_folder, 1)
            #print(f"Checking for file '{dst_file}'")

            if not os.path.exists(dst_file) :
                logging.debug(f"File: '{dst_file}' not found, removing")
                try :
                    os.remove(src_file)
                    logging.info(f"File '{src_file}' removed")
                except Exception as e :
                    logging.error(f"An error occurred when removing '{src_file}': {str(e)}")
                    
def sync_folders(src_folder, dst_folder) :
    #print(f"Syncing from '{src_folder}' to '{dst_folder}'.")    

    #Walk src directory and sync to dst
    for src_dir, dir_names, files in os.walk(src_folder) :
        #Check for directories in "current" directory
        for dir in dir_names :
            src = os.path.join(src_dir, dir)
            dst_dir = src.replace(src_folder, dst_folder, 1)

            if not os.path.isdir(dst_dir) :
                try : 
                    os.makedirs(dst_dir)
                    logging.info(f"Directory '{dst_dir}' created")
                except Exception as e :
                    logging.error(f"An error occurred when creating '{dst_dir}': {str(e)}")

        #Check for files in "current" directory
        for file in files :
            src_file = os.path.join(src_dir, file)
            dst_file = src_file.replace(src_folder, dst_folder, 1)

            if not os.path.exists(dst_file) :
                logging.info(f"File: '{dst_file}' not found")
                try :
                    file_path = shutil.copy2(src_file, dst_file)
                    logging.info(f" File: '{file_path}' created")
                except Exception as e :
                    logging.error(f"An error occurred when creating '{file_path}': {str(e)}") 

            elif (os.stat(src_file).st_mtime > os.stat(dst_file).st_mtime) :
                logging.debug(f"File: '{dst_file}' is outdated")
                try :
                    file_path = shutil.copy2(src_file, dst_file)
                    logging.info(f"File: '{file_path}' updated")
                except Exception as e :
                    logging.error(f"An error occurred when updating '{file_path}': {str(e)}")
           
def main() :

    logging.basicConfig(filename="sync.log", format="%(asctime)s-%(levelname)s: %(message)s", datefmt="%H:%M:%S", level=logging.INFO)
    
    #Handle CLI args
    parser = argparse.ArgumentParser(description='Synchronize folders.')
    parser.add_argument('src', type=str, help='Source folder to sync from')
    parser.add_argument('dst', type=str, help='Destination folder to sync to') 
    parser.add_argument('interval', type=int, help='Interval between syncs in seconds')

    args = parser.parse_args()
    
    while True :
        #Make sure source and desitnation folders exist
        folders_exist(args.src, args.dst)
        #Remove files from dst that do not exist in src
        clean_folders(args.dst, args.src)
        #Sync src to dst
        sync_folders(args.src, args.dst)
        #Sleep until next interval
        sleep(args.interval)

# Run the thing
if __name__ == "__main__" :
    main()

