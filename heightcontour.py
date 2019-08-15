#!/usr/bin/env python

"""
contourv2.py
Erin Raif, Dept. of Phys. and Astro./Earth and Env. Sci.
University of Manchester, August 2019

Takes NETCDF data from dynamical-cloud-model and creates contour plot of cloud
mixing ratio at a specified time (NB can do other 'q' variables)
"""

# TODO? =========================================
"""
Potential improvements but not necessary:
Global axes limits and labels and colorbars (if it looks better)
"""


# Imports ======================================
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import os.path as pth
from netCDF4 import Dataset 

matplotlib.use('Agg') # display not needed (if run over server)
# This may produce console error message - does not affect program

# NETCDF Variables ==============================
# NB QC HAS BEEN EDITED TO READ G/KG AS IT IS MULTIPLIED
# BY 1000 in the image creatoin process - it is actually kg/kg!!!
varlist = [['qv','Vapor mixing ratio, kg/kg'],
           ['an_1', 'No. aerosol particles in mode 1'],
           ['as_1', 'Surface area of aerosol particles in mode 1'],
           ['am_1', 'Mass of aerosol particles in mode 1'],
           ['an_2', 'No. aerosol particles in mode 2'],
           ['as_2', 'Surface area of aerosol particles in mode 2'],
           ['am_2', 'Mass of aerosol particles in mode 2'],
           ['an_m_t', 'Total no. aerosol particles in mixed mode'],
           ['an_m_1', 'No. aerosol particles from mode 1 in mixed mode'],
           ['as_m_1', 'Surface area of aerosol particles from mode 1 in mixed mode'],
           ['am_m_1', 'Mass of aerosol particles from mode 1 in mixed mode'],
           ['an_m_2', 'No. aerosol particles from mode 2 in mixed mode'],
           ['as_m_2', 'Surface area of aerosol particles from mode 2 in mixed mode'],
           ['am_m_2', 'Mass of aerosol particles from mode 2 in mixed mode'],
           ['nc', 'No. cloud droplets'],
           ['qc', 'Cloud mixing ratio, g/kg'], # SEE NOTE ABOVE THIS TABLE
           ['cn_1', 'No. cloud particles in mode 1'],
           ['cs_1', 'Surface area of cloud particles in mode 1'],
           ['cm_1', 'Mass of cloud particles in mode 1'],
           ['cn_2', 'No. cloud particles in mode 2'],
           ['cs_2', 'Surface area of cloud particles in mode 2'],
           ['cm_2', 'Mass of cloud particles in mode 2'],
           ['nr', 'No. rain particles'],
           ['qr', 'Rain mixing ratio, kg/kg'],
           ['rn_1', 'No. rain particles in mode 1'],
           ['rs_1', 'Surface area of rain particles in mode 1'],
           ['rm_1', 'Mass of rain particles in mode 1'],
           ['rn_2', 'No. rain particles in mode 2'],
           ['rs_2', 'Surface area of rain particles in mode 2'],
           ['rm_2', 'Mass of rain particles in mode 2']]
           


# Image Parameters =============================

runslist = (1,9,10)  # Runs to be used
hgs = ['1700m', '1650m', '1600m'] # Relative Humidities of runs (for titles)
varno = 15  # No. of variable investigated (qc)
time = 1800 # Time of snapshot

my_dpi = 96             # Image DPI
siz = (10,2.5*len(runslist))		# Image Size (inches as tuple, required)

zpoints = [25,150]	# Points of z array to use
axlims = [-10,10,0.5,3] # Axis limits in km to use metres change in image creation

levels = [0,0.5,1.0,1.5,2.0,2.5,3.0] # Levels for colors (6 levels = 7 boundaries)
cols = ['#f2f0f7','#dadaeb','#bcbddc','#9e9ac8','#756bb1','#54278f'] # Colors (HEX)




# Image Creation ================================

# Create figure
fig = plt.figure(figsize=siz,dpi=my_dpi)

# NB due to gedit being weird, indentation of for loop
# may not be kosher when run in jupyter, etc, but seems to be fine

# Loop over each dataset
for i in range(len(runslist)):

    # Load dataset from NCDF file as specified in runslist
    ncdf = Dataset('ncdf/' + 'run' + str(runslist[i]) + '.nc')

    # Extract y and z variables as slices
    y = ncdf['y'][:]
    z = ncdf['z'][zpoints[0]:zpoints[1]]

    # Extract time variable as slice and find index of required time
    tarr = ncdf['time'][:]
    tind = np.where(tarr==time)
    t = tind[0][0]

    # Take 2D slice in y and z of specified variable (qc)
    var = ncdf['q'][t,0,:,zpoints[0]:zpoints[1],varno]
   
    # Add contour subplot
    ax1 = fig.add_subplot((len(runslist)*100)+11+i)

    # Add axis limits and labels (??TODO: improve by globalising??)
    ax1.set_xlim(axlims[0],axlims[1])
    ax1.set_ylim(axlims[2],axlims[3])
    ax1.set_xlabel('Horizontal distance/km')
    ax1.set_ylabel('Altitude/km')

    # Make contour plot NOTE MULTIPLIED BY 1000 AS QC.
    # Transpose required dimensionally
    plot1 = ax1.contourf(y/1000,z/1000,var.transpose()*1000,levels,colors=cols)

    # Title individual plot and add colorbar
    plt.title('Height of shear layer: ' + hgs[i])
    plt.colorbar(plot1, ax=ax1, extend='both') # (??TODO: globalise??)

    
# Set tight_layout, save and close figure (does not display)
fig.tight_layout()
plt.savefig('hg_test_'+str(time)+'.png', bbox_inches='tight', dpi=my_dpi)
plt.close()
