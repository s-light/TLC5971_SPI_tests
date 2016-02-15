#!/usr/bin/python
# coding=utf-8

"""
simple test for tlc5971

TLC5971 datasheet:
http://www.ti.com/lit/ds/symlink/tlc5971.pdf#page=23&zoom=180,0,720

spidev docu:
http://tightdev.net/SpiDev_Doc.pdf

"""

import spidev
import posix
import struct
import ctypes

import time


class TLC5971_DATA(ctypes.Structure):

    """
    TLC5971 data structure.

        Bit  Overview:
        BIT NUMBER  BIT NAME
        15-0	    GSR0
        31-16	    GSG0
        47-32	    GSB0
        63-48	    GSR1
        79-64	    GSG1
        95-80	    GSB1
        111-96	    GSR2
        127-112	    GSG2
        143-128	    GSB2
        159-144	    GSR3
        175-160	    GSG3
        191-176	    GSB3
        198-192	    BCR
        205-199	    BCG
        212-206	    BCB
        213	        BLANK
        214	        DSPRPT
        215	        TMGRST
        216	        EXTGCK
        217	        OUTTMG
    """

    _fields_ = [
        # Write Command (6Bits)
        ("WRCMD", ctypes.c_uint32, 6), # default: 25h
        # Function Control Data (5 x 1Bit = 5Bits)
        ("OUTTMG", ctypes.c_uint32, 1), # default: 0
        ("EXTGCK", ctypes.c_uint32, 1), # default: 0
        ("TMGRST", ctypes.c_uint32, 1), # default: 0
        ("DSPRPT", ctypes.c_uint32, 1), # default: 1
        ("BLANK", ctypes.c_uint32, 1),  # default: 0
        # BC-Data (3 x 7Bits = 21Bits)
        ("BCB", ctypes.c_uint32, 7),  # default: 7Fh = full
        ("BCG", ctypes.c_uint32, 7),  # default: 7Fh = full
        ("BCR", ctypes.c_uint32, 7),  # default: 7Fh = full
        # BC-Data (12 x 8Bits = 21Bits)
        ("GSB3", ctypes.c_uint32, 16),
        ("GSG3", ctypes.c_uint32, 16),
        ("GSR3", ctypes.c_uint32, 16),
        ("GSB2", ctypes.c_uint32, 16),
        ("GSG2", ctypes.c_uint32, 16),
        ("GSR2", ctypes.c_uint32, 16),
        ("GSB1", ctypes.c_uint32, 16),
        ("GSG1", ctypes.c_uint32, 16),
        ("GSR1", ctypes.c_uint32, 16),
        ("GSB0", ctypes.c_uint32, 16),
        ("GSG0", ctypes.c_uint32, 16),
        ("GSR0", ctypes.c_uint32, 16),
    ]



################################################################
if __name__ == '__main__':

    # prepare Data
    # prepareData()

    # create spi object
    spi = spidev.SpiDev()

    # open spi port 0, device (CS) 0
    # /dev/spidev32766.0
    print("open spi port.")
    spi.open(0, 0)

    print("transfer one frame")
    spi.xfer2([0xAA])
