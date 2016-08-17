# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 14:15:38 2016

@author: cognitive
"""

"""Example program to demonstrate how to send a multi-channel time series to
LSL."""

import random
import time
import numpy.random as sprnd
from pylsl import StreamInfo, StreamOutlet

# first create a new stream info (here we set the name to BioSemi,
# the content-type to EEG, 8 channels, 100 Hz, and float-valued data) The
# last value would be the serial number of the device or some other more or
# less locally unique identifier for the stream as far as available (you
# could also omit it but interrupted connections wouldn't auto-recover).
info = StreamInfo('BioSemi', 'EEG', 8, 100, 'float32', 'myuid34234')

# next make an outlet
outlet = StreamOutlet(info)

print("now sending data...")
t = time.clock()
while True:
    # make a new random 8-channel sample; this is converted into a
    # pylsl.vectorf (the data type that is expected by push_sample)
    mysample = [sprnd.normal(0, 0.5), random.random(), random.random(),
                random.random(), random.random(), random.random(),
                random.random(), random.random()]
    # now send it and wait for a bit
    outlet.push_sample(mysample)
    if time.clock() - t > 1:
            time.sleep(0.01)
            mysample = [2,2,2,2,2,2,2,2]
            print('gling')
            t = time.clock()
            outlet.push_sample(mysample)
    time.sleep(0.01)
