#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2011-2013 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.

import socket;

"""
Crazyflie console is used to receive characters printed using printf
from the firmware.
"""
from cflib.crtp.crtpstack import CRTPPort
from cflib.utils.callbacks import Caller

import struct
import socket

__author__ = 'Bitcraze AB'
__all__ = ['Console']

SOUND_IP = "127.0.0.1"
SOUND_PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

soundIncrement = 0

class Console:
    """
    Crazyflie console is used to receive characters printed using printf
    from the firmware.
    """

    receivedChar = Caller()

    def __init__(self, crazyflie):
        """
        Initialize the console and register it to receive data from the copter.
        """
        self.cf = crazyflie
        self.cf.add_port_callback(CRTPPort.CONSOLE, self.incoming)
        self.cf.add_port_callback(7, self.statusIncoming)
    def statusIncoming(self, packet):
        global soundIncrement
        print("got sound")
        sound = 0
        if packet.data[0] == 100:
            sound = 3
        elif packet.data[0] == 114:
            sound = 4
        if sound > 0:
            soundIncrement = soundIncrement+1
            sock.sendto(struct.pack("<LBB", soundIncrement, 3, sound), (SOUND_IP, SOUND_PORT))
            print("Got some status packet with valid sound")
        else:
            print("Got some status with invalid sound:" + str(packet.data[0]))
    def incoming(self, packet):
        """
        Callback for data received from the copter.
        """
        # This might be done prettier ;-)
        console_text = packet.data.decode('UTF-8')

        self.receivedChar.call(console_text)
