"""
Create csv file containing exif infos about the pictures found in dir
"""

import argparse
import os
from csv import DictWriter as CsvWriter
from pathlib import Path
from typing import List

from utils import ExifInfos, helpers

DEFAULT_CSV_FILENAME = "EXIF_Data_Collection.csv"
FILEPATH_COL_NAME = "file_path"


def __argparse() -> argparse.Namespace:
    """Argument parsing"""
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
    parser.add_argument(
        "-y",
        help="Authorize overwriting of export file",
        action="store_true",
    )
    return parser.parse_args()


def __export_to_csv(exif_infos_all: List[dict], csv_path: str) -> None:
    """Export cols and data to CSV"""
    cols = []
    for exif_infos in exif_infos_all:
        print(exif_infos.keys())
        for col in exif_infos.keys():
            if col not in cols:
                cols.append(col)
    cols.remove(FILEPATH_COL_NAME)
    cols.sort()
    cols.insert(0, FILEPATH_COL_NAME)
    if exif_infos_all:
        with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = CsvWriter(csvfile, fieldnames=cols, delimiter=";", escapechar="\\")
            writer.writeheader()
            for row in exif_infos_all:
                writer.writerow(row)
        print("Fichier CSV : " + str(Path.resolve(csv_path)))
    else:
        print("No picture found")


def main():
    """Main method"""
    # Argument parsing
    arguments = __argparse()

    # Set the directory path and CSV file name
    img_path = Path.resolve(Path(arguments.directory))
    if not (Path.exists(img_path) and Path.is_dir(img_path)):
        print(str(img_path) + " is not a valid directory")
        return
    print("Dossier parcouru : " + str(img_path))
    csv_path = Path(arguments.csv_name)
    # Delete file
    if Path.exists(csv_path):
        if arguments.y:
            Path.unlink(csv_path)
        else:
            helpers.print_error(
                str(csv_path.absolute()) + " file already exists. Use -y to overwrite."
            )
            return

    # Initialize lists to hold the data
    exif_data = []

    # Walk through the directory structure
    i = 0
    for root, dirs, files in os.walk(img_path):
        files.sort()
        for file in files:
            i = i + 1
            full_path = os.path.join(root, file)
            print("[" + str(i) + "] Analysing " + full_path)
            if full_path.lower().endswith((".png", ".jpg", ".bmp")) is False:
                continue
            try:
                file_exif_infos = ExifInfos.get_exif_infos(full_path)
                if file_exif_infos:
                    exif_data.append({FILEPATH_COL_NAME: full_path} | file_exif_infos)
            except TypeError as te:
                helpers.print_error("TypeError : KO (" + full_path + ") : " + str(te))
            except ValueError as ve:
                helpers.print_error("ValueError : KO (" + full_path + ") : " + str(ve))
            except KeyboardInterrupt:
                exit()
            except BaseException as be:
                helpers.print_error("Exception : KO (" + full_path + ") : " + str(be))

        if arguments.nosubdir:
            break

    # Export CSV
    __export_to_csv(exif_data, csv_path)


# Using the special variable
# __name__
if __name__ == "__main__":
    main()
