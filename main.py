import os, pandas, numpy, scipy
from read_trc import read_trc
from read_filenames import read_filenames
from pathlength import pathlength
from threeptderiv import threeptderiv


# Workspace and directory definitions
home = os.getcwd()
dataloc = 'D:\Dropbox (University of Michigan)\Python'
os.chdir(dataloc)
CupData = pandas.read_excel('INSARCupData.xlsx', sheet_name='CupLocation')
part = 'VIADL_022'
mouthdist = 75
percentstartthresh = .05
percentstopthresh = .10
frametime = 1000/120
filter_type = 'lowpass'
filter_order = 4
filter_cutoff = 6

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

# Three point Derivatives
markers = numpy.asarray(zip(Marker.X, Marker.Y, Marker.Z))
HandPosDiff = (numpy.linalg.norm(pt2-pt1)
           for pt1, pt2 in zip(markers, markers[1:]))

vel = threeptderiv(StartRow, EndRow, HandPosDiff, frametime, filter_order, filter_cutoff, filter_type)
accel = threeptderiv(StartRow, EndRow, accel, frametime, filter_order, filter_cutoff, filter_type)
jerk = threeptderiv(StartRow, EndRow, jerk, frametime, filter_order, filter_cutoff, filter_type)

# Find beginning and end of movement


# Maximum and mean derivatives
MaxVel = vel[startmove:endmove].max()
MeanVel = vel[startmove:endmove].mean()
MaxAcc = accel[startmove:endmove].max()
MeanAcc = accel[startmove:endmove].max()
MaxJerk = jerk[startmove:endmove].max()
MeanJerk = jerk[startmove:endmove].max()

# Jerk Cost

# Path length
XPathLength, YPathLength, ZPathLength, ThreeDPathLength = pathlength(StartRow, EndRow, Marker.X, Marker.Y, Marker.Z)


#Work percent contribution?





