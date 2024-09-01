"""
Setup
"""

from setuptools import find_packages, setup

setup(
    name="exif_to_csv",
    version="1.0.0",
    description="Extract in CSV format exif datas from pictures",
    author="BAGOT Emmanuel",
    author_email="bagot.emmanuel@gmail.com",
    packages=find_packages(),
    install_requires=[
        "Pillow==10.4.0",
    ],
    python_requires=">=3.10.11",
    classifiers=[
        "License :: GNU GENERAL PUBLIC LICENSE",
        "Programming Language :: Python :: 3.10.11",
    ],
)
