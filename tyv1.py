#!/usr/bin/env python
"""
tyv1.py
Erin Raif, Dept. Phys. + Astro./Dept. Earth + Env. Sci., August 2019
Takes in data from multiple NETCDF files and plots a contour graph of pressure perturbations along y against time
at a selected height, as they form a good proxy for KH wave locatoins
"""

# Imports ==================================
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np


# Image Variables ==========================
datasets = (3,2,1,7,8) # tuple of run no.s in order
RHs = ['70%','80%','90%','95%', '99.5%'] # Relative Humidities of runs (for titles) 

fs = (10,14)	# figure size, inches (w,h)
my_dpi = 96	# DPI

height = 1510	# Height to take from (select appropriate)

levels = [-10,-5,-1,1,5,10] # Pressure levels for colour mapping (Pa)
cols = ['#a6611a','#dfc27d','#f5f5f5','#80cdc1','#018571'] # List of colours (5)

# Create figure
fig = plt.figure(figsize=fs,dpi=my_dpi)

# Loop over datasets
for i in range(len(datasets)):
	# Read in from dataset
	ncdf  = Dataset('ncdf/run' + str(datasets[i]) + '.nc')
	
	# Time, y and z arrays
	tm = ncdf['time'][:]
	yv = ncdf['y'][:]
	zarr = ncdf['z'][:]

	# Find and retrieve index of selected height
	zind = np.where(zarr==height)
	z = zind[0][0]

	# Get pressure values as 2D slice
	pr = ncdf['p'][:,0,:,z]

	# Create subplot in appropriate place
	if i == 4:
		axe = plt.subplot2grid((3,4), (2,1), colspan=2)
	else:
		# Nifty workaround for five plots if I say so myself
		axe = plt.subplot2grid((3,4), (i//2,(i%2)*2), colspan=2)

	# Axis labels and limits (note division for appropriate units)
	axe.set_xlim(0,np.max(tm)/3600)
	axe.set_xlabel('Time, hrs')
	axe.set_ylabel('Horizontal distance, km')
	axe.set_ylim(np.min(yv)/1000,np.max(yv)/1000)

	# Plot pressure contours (data must be transposed)
	pl = axe.contourf(tm/3600,yv/1000,pr.transpose(),levels,colors=cols)

	# Add title and colorbar
	plt.title('Relative Humidity: ' + RHs[i])
	plt.colorbar(pl,ax=axe,extend='both')

# Tight layout, save and close (no display)
fig.tight_layout()
plt.savefig('ty_composite_v2.png', bbox_inches='tight', dpi=my_dpi)
plt.close()
