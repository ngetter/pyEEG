# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 14:16:38 2016

@author: cognitive
"""

"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

## Set te window of display e.g WND=100 is 100 samples per chaet
NWD = 1000
## Should the DC be substructed from the signal
DC = True
## divide the signal by gain
GAIN = 4
## buffer to read on each inlet pull
BUFF = 30

# First resolve an EEG stream on the lab network
print("looking for an EEG stream...")
streams = resolve_stream('type', 'EEG')
print "strram name", streams[0].name()
print "channels" , streams[0].channel_count()


# create a new inlet to read from the stream
inlet = StreamInlet(streams[0])

#signal_tmp = np.zeros(1)
x=np.zeros(NWD)
baseline_mean = 0 
baseline_std = 0

f, ax = plt.subplots()
def dc(signal, i):
    """ 
    Calculates the DC of a signal in the specified window 
    - **parameters**, **types**, **return** and **return types**::
    
    Args:
        signal (array): 
            the signal matrix.
        
        i (int): 
            the frame number, used for dc remove based only on the beginning of
            the recordings.
        
    Returns:
        type (array): 
            the signal matrix normalized
    """
    global baseline_mean, baseline_std
    if i < 100:
        baseline_mean = np.mean(signal, axis=1, keepdims=True)
        baseline_std = np.std(signal, axis=1, keepdims=True)
        dc()
    return ((signal - baseline_mean) / baseline_std)/GAIN

def init():  
    global signal_tmp, start, x
    
    # get next sample from lsl and convert it to numpy array
    sample, start = inlet.pull_sample()
    sample = np.array(sample)
    #initiate y axis to n channels of zeros
    signal_tmp = np.zeros((len(sample), NWD))
    #initiate x axis to negativ time stamps
    #the first sample than will be marked zero on the x axis    
    x = np.linspace(-(NWD/100), 0, NWD )
    for y, sig in enumerate(signal_tmp):    
        ax.plot(x, y + sig, c='blue')
    plt.show()
    
def animate(i):
    global signal_tmp, x
    tmpy = []
    tmpx = []
    for ii in range(0,BUFF):
        sample, timestamp = inlet.pull_sample()
        tmpy.append(sample)
        tmpx.append(timestamp)
        
    signal_tmp = np.roll(signal_tmp,-BUFF,1)
    signal_tmp[:,-BUFF:] = np.array(tmpy).T
    
    if DC:
        plot_sig = dc( signal_tmp, i)
    else:
        plot_sig = signal_tmp / GAIN
    
    x = np.roll(x,-BUFF)
    x[-BUFF:] = np.array(tmpx) - start

    ax.clear()
    for y, sig in enumerate(plot_sig):
        ax.plot(x, y + sig, c='gray')
        ax.set_ylim([-2, 9])
        ax.set_xlim([x[0], x[NWD-1]])
        
ani = animation.FuncAnimation(f, animate, init_func = init, interval=1)
plt.show()

