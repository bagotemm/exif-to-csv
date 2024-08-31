"""Create csv file containing exif infos about the pictures found in dir"""

import argparse
import os
import sys
import traceback
from collections.abc import Iterable
from csv import DictWriter as CsvWriter
from pathlib import Path

from PIL import ExifTags, Image

DEFAULT_CSV_FILENAME = "EXIF_Data_Collection.csv"
FILEPATH_COL_NAME = "file_path"
EXIF_GPS_INFOS_TAG = "GPSInfo"

# Argument parsing
parser = argparse.ArgumentParser(description="Exif Infos To CSV")
parser.add_argument(
    "-c",
    "--csv_name",
    help="Output CSV Filename",
    required=False,
    default=DEFAULT_CSV_FILENAME,
)
parser.add_argument(
    "-d",
    "--directory",
    help="Directory to scan",
    required=False,
    default=os.getcwd(),
)
parser.add_argument(
    "--nosubdir",
    help="True if you don't want to scan sub sirdirectories",
    action="store_true",
)
argument = parser.parse_args()

# Set the directory path and CSV file name
img_path = Path.resolve(Path(argument.directory))
if not (Path.exists(img_path) and Path.is_dir(img_path)):
    print(str(img_path) + " is not a valid directory")
    sys.exit()
print("Dossier parcouru : " + str(img_path))
csv_path = Path(argument.csv_name)
# Initialize lists to hold the data
exif_data_cols = []
exif_data = []


# Functions
def get_exif_infos(image_path: str):
    """Function returning exif_infos of picture"""
    exif_infos = {}
    if is_valid_image_pillow(image_path):
        with Image.open(image_path) as img:
            if image_path.lower().endswith(".jpg"):
                exif = img._getexif()
            else:
                exif = img.getexif()
            if exif is None:
                return {}
            exif_infos = {
                ExifTags.TAGS[k]: "Bytes" if isinstance(v, bytes) else v
                for (k, v) in exif.items()
                if k in ExifTags.TAGS
            }
            # GPS
            if EXIF_GPS_INFOS_TAG in exif_infos.keys():
                exif_gps_infos = exif_infos[EXIF_GPS_INFOS_TAG]
                for key in exif_gps_infos.keys():
                    decode = ExifTags.GPSTAGS.get(key, key)
                    if isinstance(decode, str):
                        gps_element = exif_gps_infos[key]
                        if isinstance(gps_element, Iterable):
                            value = list(gps_element)
                            if value:
                                exif_infos[decode] = ".".join(str(x) for x in value)
                del exif_infos[EXIF_GPS_INFOS_TAG]
            for exif_attr_name in exif_infos.keys():
                if exif_attr_name not in exif_data_cols:
                    exif_data_cols.append(exif_attr_name)
        return exif_infos


def is_valid_image_pillow(file_path: str):
    """Function checkung if file is valid image according to pillow lib"""
    try:
        with Image.open(file_path) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False


def print_error(message_error: str):
    print(message_error)
    with open("error.txt", "a") as error_file:
        error_file.write(message_error)
        error_file.write(traceback.format_exc())


# Delete file if already existing
Path.unlink(csv_path, missing_ok=True)

# Walk through the directory structure
i = 1
for root, dirs, files in os.walk(img_path):
    files.sort()
    for file in files:
        full_path = os.path.join(root, file)
        print("[" + str(i) + "] Analysing " + full_path)
        if full_path.lower().endswith((".png", ".jpg", ".bmp")) is False:
            continue
        try:
            file_exif_infos = get_exif_infos(full_path)
            if file_exif_infos:
                exif_data.append({FILEPATH_COL_NAME: full_path} | file_exif_infos)
        except TypeError as te:
            print_error("TypeError : KO (" + full_path + ") : " + str(te))
        except ValueError as ve:
            print_error("ValueError : KO (" + full_path + ") : " + str(ve))
        except KeyboardInterrupt:
            exit()
        except BaseException as be:
            print_error("Exception : KO (" + full_path + ") : " + str(be))
        i = i + 1
    if argument.nosubdir:
        break


# Export to CSV
if exif_data:
    exif_data_cols.sort()
    exif_data_cols.insert(0, FILEPATH_COL_NAME)
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = CsvWriter(
            csvfile, fieldnames=exif_data_cols, delimiter=";", escapechar="\\"
        )
        writer.writeheader()
        for row in exif_data:
            writer.writerow(row)
    print("Fichier CSV : " + str(Path.resolve(csv_path)))
else:
    print("No picture found")
