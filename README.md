# Exif Infos To CSV

This script create a csv file containing exif infos about the pictures found in the current directory. You can change the directory by adding a directory path as argument.

## Usage
### Command
```bash
python exif-to-csv.py [-c/--csv_name <CSV_FILENAME>] [-d/--directory <DIRECTORY_PATH>] 
```
### Arguments
#### CSV_FILENAME
If the <CSV_FILENAME> is not specified, the file wille be EXIF_Data_Collection.csv<br>
If the <CSV_FILENAME> already exist, he will be deleted and rewritten.<br>
#### DIRECTORY_PATH
If the <DIRECTORY_PATH> is not specified, the script will be applied to the current directory. 


## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0)