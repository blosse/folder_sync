### Test task for internal development in QA team at Veeam ###

# This program syncs all files in a source folder to a destination
# folder on a given interval.

import os
import shutil
import argparse
import logging
from time import sleep

#Checks that source and destination folders exist
def folders_exist(src_folder, dst_folder) :
    if not os.path.isdir(src_folder) :
        logging.warning(f"Source folder {src_folder} not found")

    if not os.path.isdir(dst_folder) :
        try : 
            os.makedirs(dst_folder)
            logging.info(f"Destination folder not found, '{dst_folder}' generated")
        except Exception as e :
            logging.error(f"An error occurred: {str(e)}")

#Removes all files and folders from src that do not exist in dst
def clean_folders(src_folder, dst_folder) :
    for src_dir, dir_names, files in os.walk(src_folder) :
        
        #Check for directories 
        for dir in dir_names :
            src = os.path.join(src_dir, dir)
            dst_dir = src.replace(src_folder, dst_folder, 1)

            if not os.path.isdir(dst_dir) :
                logging.debug(f"Directory '{dst_dir}' not found, removing")
                try :
                    shutil.rmtree(src)
                    logging.info(f"Directory '{src}' removed")
                except Exception as e :
                    logging.error(f"An error occurred when removing '{src}': {str(e)}")

        #Check for files
        for file in files :
            src_file = os.path.join(src_dir, file)
            dst_file = src_file.replace(src_folder, dst_folder, 1)

            if not os.path.exists(dst_file) :
                logging.debug(f"File '{dst_file}' not found, removing")
                try :
                    os.remove(src_file)
                    logging.info(f"File '{src_file}' removed")
                except Exception as e :
                    logging.error(f"An error occurred when removing '{src_file}': {str(e)}")
                    
#Copy or update all files and folders that exist in src to dst
def sync_folders(src_folder, dst_folder) :
    for src_dir, dir_names, files in os.walk(src_folder) :

        #Check for directories 
        for dir in dir_names :
            src = os.path.join(src_dir, dir)
            dst_dir = src.replace(src_folder, dst_folder, 1)

            if not os.path.isdir(dst_dir) :
                try : 
                    os.makedirs(dst_dir)
                    logging.info(f"Directory '{dst_dir}' created")
                except Exception as e :
                    logging.error(f"An error occurred when creating '{dst_dir}': {str(e)}")

        #Check for files
        for file in files :
            src_file = os.path.join(src_dir, file)
            dst_file = src_file.replace(src_folder, dst_folder, 1)

            #If file does not exist
            if not os.path.exists(dst_file) :
                logging.debug(f"File '{dst_file}' not found")
                try :
                    file_path = shutil.copy2(src_file, dst_file)
                    logging.info(f"File '{file_path}' created")
                except Exception as e :
                    logging.error(f"An error occurred when creating '{file_path}': {str(e)}") 

            #If file is outdated
            elif (os.stat(src_file).st_mtime > os.stat(dst_file).st_mtime) :
                logging.debug(f"File '{dst_file}' is outdated")
                try :
                    file_path = shutil.copy2(src_file, dst_file)
                    logging.info(f"File '{file_path}' updated")
                except Exception as e :
                    logging.error(f"An error occurred when updating '{file_path}': {str(e)}")
           
# Run the thing
if __name__ == "__main__" :
    #Set up logging
    logging.basicConfig(format="%(asctime)s-%(levelname)s: %(message)s",
                        datefmt="%H:%M:%S",
                        level=logging.INFO,
                        handlers=[
                            logging.FileHandler("sync.log"),
                            logging.StreamHandler()])
    
    #Handle CLI args
    parser = argparse.ArgumentParser(description='Synchronize folders.')
    parser.add_argument('src', type=str, help='Source folder to sync from')
    parser.add_argument('dst', type=str, help='Destination folder to sync to') 
    parser.add_argument('interval', type=int, help='Interval between syncs in seconds')
    args = parser.parse_args()
    
    #Sync
    while True :
        #Make sure source and desitnation folders exist
        folders_exist(args.src, args.dst)
        #Remove files from dst that do not exist in src
        clean_folders(args.dst, args.src)
        #Sync src to dst
        sync_folders(args.src, args.dst)
        #Sleep until next interval
        sleep(args.interval)

