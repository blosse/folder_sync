A script which performs one-way synchronization between two folders. The script will maintain an exact replica of a source folder at a given destination location.

The script expects four arguments: path to a source folder, path to a destination folder, path to a log file and a time internval in seconds.
The script will sync the source folder to a destination folder on the given interval. All file creations, deletions and modifications at the destination folder is logged to the log-file and console.
