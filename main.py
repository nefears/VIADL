import os, pandas, read_trc, read_filenames

# Workspace and directory definitions
home = 'D:\Dropbox (University of Michigan)\Python\VIADL'
dataloc = 'F:\Projects\VIADL\Data\Cortex'
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

filename = 'stringstring_string_r1_stringstring'

# Determine which hand was used by finding the hand/trial string in the filename
if '_r' in filename:
    Hand = 'Right'
    Trial = filename[filename.find('_r')+2]
    Marker = TRC[["RM2X", "RM2Y", "RM2Z"]].copy()
elif '_l' in filename:
    Hand = 'Left'
    Trial = filename[filename.find('_l')+2]
    Marker = TRC[["LM2X", "LM2Y", "LM2Z"]].copy()

# Find Cup Distance


# Path length


# Three point Derivative


# Jerk Cost





