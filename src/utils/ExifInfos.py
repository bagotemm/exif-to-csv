"""Exif Infos"""

from collections.abc import Iterable

from PIL import ExifTags, Image


def get_exif_infos(image_path: str, bytes_transcription=False):
    """Function returning exif_infos of picture"""
    exif_tag_gps_infos = "GPSInfo"
    exif_infos = {}
    if __is_valid_image_pillow(image_path):
        with Image.open(image_path) as img:
            if image_path.lower().endswith(".jpg"):
                exif = img._getexif()
            else:
                exif = img.getexif()
            if exif is None:
                return {}
            exif_infos = {
                ExifTags.TAGS[k]: (
                    (str(v) if bytes_transcription else "Bytes")
                    if isinstance(v, bytes)
                    else v
                )
                for (k, v) in exif.items()
                if k in ExifTags.TAGS
            }
            # GPS
            if exif_tag_gps_infos in exif_infos.keys():
                exif_gps_infos = exif_infos[exif_tag_gps_infos]
                for key in exif_gps_infos.keys():
                    decode = ExifTags.GPSTAGS.get(key, key)
                    if isinstance(decode, str):
                        gps_element = exif_gps_infos[key]
                        if isinstance(gps_element, Iterable):
                            value = list(gps_element)
                            if value:
                                exif_infos[decode] = ".".join(str(x) for x in value)
                del exif_infos[exif_tag_gps_infos]
        return exif_infos


def __is_valid_image_pillow(file_path: str):
    """Function checkung if file is valid image according to pillow lib"""
    try:
        with Image.open(file_path) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False
