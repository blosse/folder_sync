#!/usr/bin/env python3

### Test task for internal development in QA team at Veeam ###

#This program syncs all files in a source folder and its nested folders 
#to a destination folder on a given interval.

import os
import shutil
import argparse
import logging
from time import sleep

#Checks that source and destination folders exist
def folders_exist(src_folder: str, dst_folder: str) -> None:
    if not os.path.isdir(src_folder):
        logging.warning(f"Source folder {src_folder} not found")

    if not os.path.isdir(dst_folder):
        try: 
            os.makedirs(dst_folder)
            logging.info(f"Destination folder not found, '{dst_folder}' generated")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")

#Removes all files and folders from dst that do not exist in src
def clean_folders(src_folder: str, dst_folder: str) -> None:
    for root, folder_names, files in os.walk(dst_folder):
        
        #Check for directories 
        for folder in folder_names:
            dst = os.path.join(root, folder)
            dst_dir = dst.replace(dst_folder, src_folder, 1)

            if not os.path.isdir(dst_folder):
                logging.debug(f"Folder '{dst_folder}' not found, removing")
                try:
                    shutil.rmtree(dst)
                    logging.info(f"Folder '{dst}' removed")
                except Exception as e:
                    logging.error(f"An error occurred when removing '{dst}': {str(e)}")

        #Check for files
        for file in files:
            dst_file = os.path.join(root, file)
            src_file = dst_file.replace(dst_folder, src_folder, 1)

            if not os.path.exists(src_file):
                logging.debug(f"File '{src_file}' not found, removing")
                try:
                    os.remove(dst_file)
                    logging.info(f"File '{dst_file}' removed")
                except Exception as e:
                    logging.error(f"An error occurred when removing '{dst_file}': {str(e)}")
                    
#Copy or update all files and folders that exist in src to dst
def sync_folders(src_folder: str, dst_folder: str) -> None:
    for root, folder_names, files in os.walk(src_folder):

        #Check for directories 
        for folder in folder_names:
            src = os.path.join(root, folder)
            dst_dir = src.replace(src_folder, dst_folder, 1)

            if not os.path.isdir(dst_folder):
                try: 
                    os.makedirs(dst_folder)
                    logging.info(f"Directory '{dst_folder}' created")
                except Exception as e:
                    logging.error(f"An error occurred when creating '{dst_folder}': {str(e)}")

        #Check for files
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = src_file.replace(src_folder, dst_folder, 1)

            #If file does not exist
            if not os.path.exists(dst_file):
                logging.debug(f"File '{dst_file}' not found")
                try:
                    file_path = shutil.copy2(src_file, dst_file)
                    logging.info(f"File '{file_path}' created")
                except Exception as e:
                    logging.error(f"An error occurred when creating '{file_path}': {str(e)}") 

            #If file is outdated
            elif (os.stat(src_file).st_mtime > os.stat(dst_file).st_mtime):
                logging.debug(f"File '{dst_file}' is outdated")
                try:
                    file_path = shutil.copy2(src_file, dst_file)
                    logging.info(f"File '{file_path}' updated")
                except Exception as e:
                    logging.error(f"An error occurred when updating '{file_path}': {str(e)}")
           
# Run the thing
if __name__ == "__main__":
    #Handle CLI args
    parser = argparse.ArgumentParser(description='Synchronize folders')
    parser.add_argument('src', type=str, help='Source folder to sync from')
    parser.add_argument('dst', type=str, help='Destination folder to sync to') 
    parser.add_argument('log', type=str, help='Path to log file')
    parser.add_argument('interval', type=int, help='Interval between syncs in seconds')
    args = parser.parse_args()
    
    #Set up logging
    logging.basicConfig(format="%(asctime)s-%(levelname)s: %(message)s",
                        datefmt="%H:%M:%S",
                        level=logging.INFO,
                        handlers=[
                            logging.FileHandler(args.log),
                            logging.StreamHandler()])

    #Sync
    while True:
        #Make sure source and desitnation folders exist
        folders_exist(args.src, args.dst)
        #Remove files from dst that do not exist in src
        clean_folders(args.src, args.dst)
        #Sync src to dst
        sync_folders(args.src, args.dst)
        #Sleep until next interval
        sleep(args.interval)

