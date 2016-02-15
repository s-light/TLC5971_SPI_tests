#!/usr/bin/python
# coding=utf-8

"""
simple test for tlc5971

TLC5971 datasheet:
http://www.ti.com/lit/ds/symlink/tlc5971.pdf#page=23&zoom=180,0,720

spidev docu:
http://tightdev.net/SpiDev_Doc.pdf

"""

import posix
import struct
import ctypes

import time

try:
    import spidev
except ImportError:
    # no spidev here..
    print("no spidev. dry-run..")
    spidev_available = False
else:
    spidev_available = True


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
        # BC-Data (12 x 16Bits = 192Bits)
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

def bytes_to_hex(Bytes):
    return ''.join(["0x%02X " % x for x in Bytes]).strip()
# end def

def low(value):
    return value % 256
def high(value):
    return value // 256


# config area as single uint32_t:
# data_header = ctypes.c_uint32(0)
# data_header.value =
# data_header = 0b10010100010111111111111111111111
data_header = [
    0b10010100,
    0b01011111,
    0b11111111,
    0b11111111
]


################################################################
if __name__ == '__main__':

    spi = None

    # create spi object
    if spidev_available:
        print("create spi devices.")
        spi = spidev.SpiDev()

    # open spi port 0, device (CS) 0
    #
    print("open spi port.")
    # /dev/spidev32766.0
    # Connects to the specified SPI device, opening /dev/spidev-bus.device
    if spidev_available:
        spi.open(32766, 0)

    print("set speed to 600kHz (min speed)")
    if spidev_available:
        spi.max_speed_hz = 600000
        spi.bits_per_word = 8

    # ------------------------------------------
    print("create data")
    # my_data = [0x01, 0x02, 0x03, 0x04]

    # my_data = TLC5971_DATA()
    # print("my_data: ", my_data)

    # print("data_header", data_header)

    # data_GS = [
    #     10010,
    #     10020,
    #     10030,
    #     30010,
    #     10020,
    #     10030,
    #     10010,
    #     30020,
    #     10030,
    #     10010,
    #     10020,
    #     30030,
    # ]
    data_GS = [
        # 0
        3000,
        0,
        0,
        # 1
        0,
        5000,
        0,
        # 2
        0,
        0,
        9000,
        # 3
        3000,
        6000,
        0,
    ]

    # data_to_send = [my_data]
    data_to_send = []
    # data_to_send = data_header

    # add header data:
    for value in data_header:
        data_to_send.append(
            value
        )

    # add GS data:
    for value in data_GS:
        data_to_send.append(high(value))
        data_to_send.append(low(value))
        # data_to_send.append(
        #     ctypes.c_uint16(value)
        # )

    # add 1 byte for additional 8 clock cycles
    # data_to_send.append(0)

    # data_to_send = [0, 255, 0, 65535]

    # print("data_to_send:", data_to_send)
    # print("data_to_send:")
    # for element in data_to_send:
    #     print(element)
    # print("------------")

    # ------------------------------------------

    print("transfer one frame")
    # spi.xfer2([0xAA])
    if spidev_available:
        print("send...")
        # spi.xfer2(
        #     data_to_send,
        #     0,  # delay_usec
        #     # speed_hz
        #     # bits_per_word
        # )
        # spi.xfer2(data_header)
        spi.xfer2(data_to_send)

    print("finished.")
