#!/usr/bin/env python

# Copyright Contributors to the OpenImageIO project.
# SPDX-License-Identifier: Apache-2.0
# https://github.com/AcademySoftwareFoundation/OpenImageIO

import struct


BASE = "base.webp"
OUTPUT = "openmeta-metadata.webp"
EXIF_FLAG = 0x08
XMP_FLAG = 0x04


def read_chunks(data):
    if len(data) < 12 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise RuntimeError("base image is not a RIFF WebP file")

    chunks = []
    offset = 12
    while offset < len(data):
        if offset + 8 > len(data):
            raise RuntimeError("truncated WebP chunk header")
        fourcc = data[offset : offset + 4]
        size = struct.unpack_from("<I", data, offset + 4)[0]
        begin = offset + 8
        end = begin + size
        if end > len(data):
            raise RuntimeError("truncated WebP chunk payload")
        chunks.append((fourcc, data[begin:end]))
        offset = end + (size & 1)
    return chunks


def write_chunk(fourcc, payload):
    chunk = fourcc + struct.pack("<I", len(payload)) + payload
    if len(payload) & 1:
        chunk += b"\x00"
    return chunk


def make_tiff():
    make = b"OpenMetaCamera\x00"
    ifd_size = 2 + 2 * 12 + 4
    make_offset = 8 + ifd_size
    tiff = bytearray(b"II")
    tiff += struct.pack("<H", 42)
    tiff += struct.pack("<I", 8)
    tiff += struct.pack("<H", 2)
    tiff += struct.pack("<HHII", 0x010F, 2, len(make), make_offset)
    tiff += struct.pack("<HHI", 0x0112, 3, 1)
    tiff += struct.pack("<H", 6) + b"\x00\x00"
    tiff += struct.pack("<I", 0)
    tiff += make
    return bytes(tiff)


def make_xmp():
    return (
        b"<x:xmpmeta xmlns:x='adobe:ns:meta/'>"
        b"<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>"
        b"<rdf:Description xmlns:xmp='http://ns.adobe.com/xap/1.0/' "
        b"xmp:CreatorTool='OpenMeta WebP pilot' xmp:Rating='4'/>"
        b"</rdf:RDF></x:xmpmeta>"
    )


with open(BASE, "rb") as input_file:
    base_chunks = read_chunks(input_file.read())

vp8x = bytes((EXIF_FLAG | XMP_FLAG, 0, 0, 0, 0, 0, 0, 0, 0, 0))
chunks = write_chunk(b"VP8X", vp8x)
for chunk_type, payload in base_chunks:
    if chunk_type not in (b"VP8X", b"EXIF", b"XMP "):
        chunks += write_chunk(chunk_type, payload)
chunks += write_chunk(b"EXIF", make_tiff())
chunks += write_chunk(b"XMP ", make_xmp())

body = b"WEBP" + chunks
with open(OUTPUT, "wb") as output_file:
    output_file.write(b"RIFF" + struct.pack("<I", len(body)) + body)
