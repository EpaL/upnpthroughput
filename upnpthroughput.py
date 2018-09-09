#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module Docstring
upnpthroughput diplays the current throughput (upload and download) of your UPnP-enabled Internet router.
Note: upnpc must be installed prior to using. Visit https://brew.sh for instructions on how to install Homebrew, then 'brew install upnpc' to install upnpc.
"""

import subprocess
import distutils.spawn
import re
import time

__author__ = "Edward Lawford"
__version__ = "0.1.0"
__license__ = "MIT"

# Variables
upnpcCommand = ""
# upnpcCommand = distutils.spawn.find_executable("upnpc")

# Runtime

def main():
    """ Main entry point """

    previousBytesIn = 0
    previousBytesOut = 0
    lastTimestamp = 0

    if not upnpcCommand:
        print "Unable to locate upnpc. Did you install it? Make sure Homebrew is installed, then try 'brew install upnpc'."
        exit(5)

    if (validateIGD() == False):
        print "Valid Internet Gateway Device (IGD) not found. Check UPnP is enabled on your Internet router."
        exit(5)

    while True:
        
        # Poll the router's in and out bytes.
        p = subprocess.Popen("%s -s" % (upnpcCommand), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
                    currentBytesOut = int(m.group(1))
                m = re.search('Recv: (\d+)', line)
                if m:
                    currentBytesIn  = int(m.group(1))
                if lastTimestamp != 0 :
                    # Calculate and display the throughput rate in bytes/sec.
                    interval = time.time() - lastTimestamp   
                    inBytesSecFormatted = "{:,.0f}".format((currentBytesIn - previousBytesIn) / interval)
                    outBytesSecFormatted = "{:,.0f}".format((currentBytesOut - previousBytesOut) / interval)
                    print "In: %s bytes/sec Out: %s bytes/sec" % (inBytesSecFormatted, outBytesSecFormatted)
                lastTimestamp = time.time()
                
                previousBytesIn = currentBytesIn
                previousBytesOut = currentBytesOut

def validateIGD():

    validIgdFound = False

    p = subprocess.Popen("%s -s" % (upnpcCommand), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:

        line = p.stdout.readline()
        if line == '' and p.poll() != None:
            break

        if line.find("Found valid IGD") == 0:
            validIgdFound = True
            print line
    
    return validIgdFound

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()