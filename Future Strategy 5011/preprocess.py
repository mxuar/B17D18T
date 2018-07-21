#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 21:18:55 2018

@author: xumin
"""

# directory below on your own computer accordingly
import os
working_directory = '/Users/xumin/Desktop/5011 Advanced Statistics/SVM'
os.chdir(working_directory)
from svmtest import handle_bar

# Run the main function in your demo.py to get your model and training reday(if there is any)
os.system('python svmtest.py')

import h5py
import empyrical.utils
import pandas as pd
import numpy as np
from copy import deepcopy
format2_dir = 'Data/data_format2_20170717_20171211.h5'
f3='Data/1.h5'


btData = h5py.File(f3, mode='r')

import glob

f=h5py.File('/Users/xumin/Desktop/h5/1.h5', mode= "r")
    