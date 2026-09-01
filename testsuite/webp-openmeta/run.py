#!/usr/bin/env python

# Copyright Contributors to the OpenImageIO project.
# SPDX-License-Identifier: Apache-2.0
# https://github.com/AcademySoftwareFoundation/OpenImageIO

redirect = " >> out.txt 2>&1 "

command += oiiotool("--create 1x1 3 -d uint8 -o base.webp")
command += run_app(pythonbin + " src/make-openmeta-webp.py", silent=True)
command += oiiotool(
    'openmeta-metadata.webp '
    '--echo "Make={TOP.Make}" '
    '--echo "Orientation={TOP.Orientation}" '
    '--echo "XMP rating={TOP.\'XMP:Rating\'}" '
    '--echo "ColorSpace={TOP.\'oiio:ColorSpace\'}"'
)
