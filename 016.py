#!/usr/bin/env python3

from packet import Packet

if '__main__' == __name__:
    done = False

    while not done:
        try:
            line = input()
            packet = Packet(line)
            print(packet.version_sum())
            print(packet.value)
        except:
            done = True
