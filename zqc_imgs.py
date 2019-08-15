#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:29:24 2019

Erin Raif, SEES @ Manchester, August 2019
Part 1: Reads chosen 2D array from NCDF (in this, z and average qc over t and y) into CSVs
Part 2: Plots the results reading from created CSVs
Does not activate the first part if fullrun is set to False to save time.
"""

# Imports ===========================================
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# Functions =========================================
def writetoTXT(name,z_list,nc_list,var):
    # writes data to two-column space delimited text file
    filename = name + '_'+var+ '.txt'    
    csvWrite = open(filename, 'w')
    csvWrite.write('z '+var+'\n')
    
    for i in range(len(z_list)):
        csvWrite.write(str(z_list[i])+' '+str(nc_list[i])+'\n')
    
    print('Data successfully written to ' + filename)
    csvWrite.close()
    
    return 0

    
def readTXT(filename):
    # reads from two-column space delimited text file
    data = np.loadtxt(filename,skiprows=1)
    data = data.tolist()
    
    print('Data from ' + filename + ' read successfully.\n')
    
    return data
    
def full(name,var):
    # full write and read program
    dataname = 'ncdf/' + name + '.nc'
    
    ncdf = Dataset(dataname)
    
    z = ncdf['z'][:]
    if var == 'qc':
	    qc = np.mean(np.mean(ncdf['q'][:,0,:,:,15],axis=0),axis=0)*1000
	    writetoTXT(name,z,qc,var)
    elif var == 'nc':
	nc = np.mean(np.mean(ncdf['q'][:,0,:,:,14],axis=0),axis=0)
	writetoTXT(name,z,nc,var)
      
    
    data = readTXT(name + '_' + var + '.txt')
    
    return data    


# Program ==================================================

# Input variables
var = 'nc' # nc and qc only unless you want to break it!
noruns = 10 # Number of runs in total to make .txt files from - NOT no. to plot
runslist = (3,2,1,7,8) # List of runs to plot
RHs = ['70%','80%','90%','95%', '99.5%'] # Relative Humidities of runs (for titles)

ylims = [0.5,4.5] # y-limits

# Runtype variable
fullrun = False # True if .txt files need to be created still

# Blank numpy array for data
alldata = []
    
# Data retrieval ===========================================
if fullrun == True:
    
    for i in range(noruns):
	# Cycle through all runs
        name = 'run' + str(i+1)
        
        data = full(name,var)
        
        alldata.append(data)

    alldata = np.array(alldata)
    
    print(alldata.shape)
    
else:
    # Plotting (and reading) only
    for i in range(noruns):
        name = 'run' + str(i+1)
        
        data = readTXT(name + '_' + var + '.txt')
        
        alldata.append(data)        
        
    alldata = np.array(alldata)

# Plotting ==============================================

ad = alldata # shorten for ease

# Create figure, object-oriented
fig = plt.figure()
ax = fig.add_subplot(111)

# Set y-label and limits
ax.set_ylabel('Height, km')
ax.set_ylim(ylims[0],ylims[1])

# Set appropriate x-label and limits
if var == 'qc':
	# Mixing ratio
	ax.set_xlabel('Mixing ratio of cloud, g/kg')
	ax.set_xlim(1e-11,1)
else:
	# Concentration
	ax.set_xlabel('Number of cloud particles per cm^-3')
	ax.set_xlim(1e-2,1e10)
	
for i in range(len(runslist)):
	# Plot each line
	plt.semilogx(ad[i,:,1],ad[i,:,0]/1000,label = 'RH: ' + RHs[i])

# Add legend, grid, make tight layout, save, and show.
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig('ncz_semilog_a.png')
plt.show()
