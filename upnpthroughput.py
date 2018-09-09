#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module Docstring
"""

import subprocess
import distutils.spawn
import re

__author__ = "Edward Lawford"
__version__ = "0.1.0"
__license__ = "MIT"

# Variables
upnpcCommand = distutils.spawn.find_executable("upnpc")

# Runtime
previousBytesIn = 0
previousBytesOut = 0

def main():
    """ Main entry point """

    while True:
        p = subprocess.Popen("%s -s" % (upnpcCommand), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout = []
        while True:
            currentBytesIn = 0
            currentBytesOut = 0

            line = p.stdout.readline()
            if line == '' and p.poll() != None:
                break
            
            # Look for the "Bytes:" line
            if line.find("Bytes:") == 0:
                # Extract the "Bytes In" and "Bytes Out" values
                # Example output:
                #   Bytes:   Sent: 736400464        Recv: 3839423632
                m = re.search('Sent: (\d+)', line)
                if m:
                    currentBytesOut = m.group(1)
                m = re.search('Recv: (\d+)', line)
                if m:
                    currentBytesIn  = m.group(1)
                print "Bytes In: %s  Out: %s" % (currentBytesIn, currentBytesOut)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()