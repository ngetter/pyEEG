# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 13:26:04 2016

@author: cognitive
"""

import numpy as np
from numpy.random import exponential as rexp

import matplotlib.pyplot as plt


exp = rexp(1.0,500)

x = np.linspace(0, 50, 500)

f2 = plt.hist(exp, histtype='stepfilled')