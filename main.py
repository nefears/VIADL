import os, pandas, numpy
from read_trc import read_trc
from read_filenames import read_filenames
from pathlength import pathlength


# Workspace and directory definitions
home=os.getcwd()
dataloc = 'D:\Dropbox (University of Michigan)\Python'
os.chdir(dataloc)
CupData = pandas.read_excel('INSARCupData.xlsx', sheet_name='CupLocation')
part = 'VIADL_022'
mouthdist = 75
percentstartthresh = .05
percentstopthresh = .10
# Find TRC file names
folder = dataloc + '\\' + part + '\Tracked + Packaged\TRC'
os.chdir(folder)
files = read_filenames('UPPER.trc')

# Read in TRC data
TRC = read_trc(files[1], folder, home)
StartRow = 59
EndRow = len(TRC.index)

filename = files[0]

# Determine which hand was used by finding the hand/trial string in the filename
if '_r' in filename:
    Hand = 'Right'
    Trial = filename[filename.find('_r')+2]
    Marker = TRC[["RM2X", "RM2Y", "RM2Z"]].copy()
    Marker.columns = ["X", "Y", "Z"]
elif '_l' in filename:
    Hand = 'Left'
    Trial = filename[filename.find('_l')+2]
    Marker = TRC[["LM2X", "LM2Y", "LM2Z"]].copy()
    Marker.columns = ["X", "Y", "Z"]
    Marker = Marker.astype(numpy.float)

# Find Cup Distance

# Path length
XPathLength, YPathLength, ZPathLength, ThreeDPathLength = pathlength(StartRow, EndRow, Marker.X, Marker.Y, Marker.Z)

# Three point Derivative
#define velocity, acceleration from forward and backward points

# Jerk Cost





