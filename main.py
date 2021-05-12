import os, pandas, numpy, scipy, openpyxl
from read_trc import read_trc
from read_filenames import read_filenames
from pathlength import pathlength
from threeptderiv import threeptderiv
from jerkcost import jerkcost

# Workspace and directory definitions
home = os.getcwd()
# dataloc = 'D:\Dropbox (University of Michigan)\Python'
dataloc = "C:/Users/nefea/Dropbox (University of Michigan)/Python"
os.chdir(dataloc)
CupData = pandas.read_excel('INSARCupData.xlsx', sheet_name='CupLocation')
part = 'VIADL_022'
mouthdist = 75
percentstartthresh = .05
percentstopthresh = .10
framerate = 120
frametime = 1000/framerate
filter_type = 'lowpass'
filter_order = 4
filter_cutoff = 6

# Create database using Pandas dataframe
db = pandas.DataFrame(columns=['ID', 'Group', 'Age', 'Trial', 'Hand',
                               'HandMaxVel', 'HandMeanVel', 'HandMaxAccel', 'HandMeanAccel','HandMaxJerk', 'HandMeanJerk', 'HandJerkCost', 'HandXPathLength', 'HandYPathLength', 'HandZPathLength', 'HandThreeDPathLength',
                               'ChestMaxVel', 'ChestMeanVel', 'ChestMaxAccel', 'ChestMeanAccel','ChestMaxJerk', 'ChestMeanJerk', 'ChestJerkCost', 'ChestXPathLength', 'ChestYPathLength', 'ChestZPathLength', 'ChestThreeDPathLength',
                               'HeadMaxVel', 'HeadMeanVel', 'HeadMaxAccel', 'HeadMeanAccel','HeadMaxJerk', 'HeadMeanJerk', 'HeadJerkCost', 'HeadXPathLength', 'HeadYPathLength', 'HeadZPathLength', 'HeadThreeDPathLength'])

# Read in demographic data per part
Group = 'TD'
Age = 11

# For loop by part

# Find TRC file names by part
folder = dataloc + '\\' + part + '\Tracked + Packaged\TRC'
os.chdir(folder)
files = read_filenames('UPPER.trc')

# For loop by number of trials within part

# Read in TRC data
TRC = read_trc(files[1], folder, home)
StartRow = 59
EndRow = len(TRC.index)

filename = files[0]

# Determine which hand was used by finding the hand/trial string in the filename
if '_r' in filename:
    Hand = 'Right'
    Trial = filename[filename.find('_r')+2]
    HandMarker = TRC[["RM2X", "RM2Y", "RM2Z"]].copy()
    HandMarker.columns = ["X", "Y", "Z"]
    HandMarker = HandMarker.astype(numpy.float)
    ChestMarker = TRC[["XYPHX", "XYPHY", "XYPHZ"]].copy()
    ChestMarker.columns = ["X", "Y", "Z"]
    ChestMarker = ChestMarker.astype(numpy.float)
    HeadMarker = TRC[["GR3X", "GR3Y", "GR3Z"]].copy()
    HeadMarker.columns = ["X", "Y", "Z"]
    HeadMarker = HeadMarker.astype(numpy.float)
elif '_l' in filename:
    Hand = 'Left'
    Trial = filename[filename.find('_l')+2]
    HandMarker = TRC[["LM2X", "LM2Y", "LM2Z"]].copy()
    HandMarker.columns = ["X", "Y", "Z"]
    HandMarker = HandMarker.astype(numpy.float)
    ChestMarker = TRC[["XYPHX", "XYPHY", "XYPHZ"]].copy()
    ChestMarker.columns = ["X", "Y", "Z"]
    ChestMarker = ChestMarker.astype(numpy.float)
    HeadMarker = TRC[["GL3X", "GL3Y", "GL3Z"]].copy()
    HeadMarker.columns = ["X", "Y", "Z"]
    HeadMarker = HeadMarker.astype(numpy.float)

# Three point Derivatives
# Hand
HandPosDiff=numpy.empty([1,0]) # empty numpy.array to collect data
markers = numpy.asarray(list(zip(HandMarker.X, HandMarker.Y, HandMarker.Z)))
for pt1, pt2 in zip(markers, markers[1:]):
    HandPosDiff = numpy.append(HandPosDiff, numpy.linalg.norm(pt2 - pt1))

Handvel = threeptderiv(StartRow, EndRow, HandPosDiff, frametime, filter_order, filter_cutoff, filter_type)
Handaccel = threeptderiv(StartRow, EndRow, Handvel, frametime, filter_order, filter_cutoff, filter_type)
Handjerk = threeptderiv(StartRow, EndRow, Handaccel, frametime, filter_order, filter_cutoff, filter_type)

# Chest
ChestPosDiff=numpy.empty([1,0]) # empty numpy.array to collect data
markers = numpy.asarray(list(zip(ChestMarker.X, ChestMarker.Y, ChestMarker.Z)))
for pt1, pt2 in zip(markers, markers[1:]):
    ChestPosDiff = numpy.append(ChestPosDiff, numpy.linalg.norm(pt2 - pt1))

Chestvel = threeptderiv(StartRow, EndRow, HandPosDiff, frametime, filter_order, filter_cutoff, filter_type)
Chestaccel = threeptderiv(StartRow, EndRow, Handvel, frametime, filter_order, filter_cutoff, filter_type)
Chestjerk = threeptderiv(StartRow, EndRow, Handaccel, frametime, filter_order, filter_cutoff, filter_type)

# Head
HeadPosDiff=numpy.empty([1,0]) # empty numpy.array to collect data
markers = numpy.asarray(list(zip(HeadMarker.X, HeadMarker.Y, HeadMarker.Z)))
for pt1, pt2 in zip(markers, markers[1:]):
    HeadPosDiff = numpy.append(HeadPosDiff, numpy.linalg.norm(pt2 - pt1))

Headvel = threeptderiv(StartRow, EndRow, HandPosDiff, frametime, filter_order, filter_cutoff, filter_type)
Headaccel = threeptderiv(StartRow, EndRow, Handvel, frametime, filter_order, filter_cutoff, filter_type)
Headjerk = threeptderiv(StartRow, EndRow, Handaccel, frametime, filter_order, filter_cutoff, filter_type)

# Find start and end of movement
# start of movement
over_thresh = abs(Handvel) > (Handvel.max()*percentstartthresh)
frames_over = numpy.asarray(numpy.where(over_thresh == 1))
for j in range(frames_over.shape[1]-12):
    print(frames_over[:, j+12]-frames_over[:, j])
    if frames_over[:, j+12]-frames_over[:, j] == 12:
        startmove = int(frames_over[:,j])
        break

# end of movement
under_thresh = abs(Handvel) < (Handvel.max()*percentstopthresh)
frames_under = numpy.asarray(numpy.where(over_thresh == 1))
move_stops = numpy.where(numpy.diff(frames_under)>1)[1]
mouth_stops = move_stops[abs(HeadMarker.Z[move_stops])-HandMarker.Z[move_stops]<mouthdist]
endmove = int(mouth_stops[0])

# Maximum and mean derivatives
# Hand
HandMaxVel = numpy.amax(Handvel[startmove:endmove])
HandMeanVel = numpy.mean(Handvel[startmove:endmove])
HandMaxAccel = numpy.amax(Handaccel[startmove:endmove])
HandMeanAccel = numpy.mean(Handaccel[startmove:endmove])
HandMaxJerk = numpy.amax(Handjerk[startmove:endmove])
HandMeanJerk = numpy.mean(Handjerk[startmove:endmove])

# Chest
ChestMaxVel = numpy.amax(Chestvel[startmove:endmove])
ChestMeanVel = numpy.mean(Chestvel[startmove:endmove])
ChestMaxAccel = numpy.amax(Chestaccel[startmove:endmove])
ChestMeanAccel = numpy.mean(Chestaccel[startmove:endmove])
ChestMaxJerk = numpy.amax(Chestjerk[startmove:endmove])
ChestMeanJerk = numpy.mean(Chestjerk[startmove:endmove])

# Head
HeadMaxVel = numpy.amax(Headvel[startmove:endmove])
HeadMeanVel = numpy.mean(Headvel[startmove:endmove])
HeadMaxAccel = numpy.amax(Headaccel[startmove:endmove])
HeadMeanAccel = numpy.mean(Headaccel[startmove:endmove])
HeadMaxJerk = numpy.amax(Headjerk[startmove:endmove])
HeadMeanJerk = numpy.mean(Headjerk[startmove:endmove])

# Jerk Cost
HandJerkCost = jerkcost(x=Handjerk, frametime=frametime, framerate=framerate, max_vel=HandMaxVel)
ChestJerkCost = jerkcost(x=Chestjerk, frametime=frametime, framerate=framerate, max_vel=ChestMaxVel)
HeadJerkCost = jerkcost(x=Headjerk, frametime=frametime, framerate=framerate, max_vel=HeadMaxVel)

# Path length
HandXPathLength, HandYPathLength, HandZPathLength, HandThreeDPathLength = pathlength(startmove, endmove, HandMarker.X, HandMarker.Y, HandMarker.Z)
ChestXPathLength, ChestYPathLength, ChestZPathLength, ChestThreeDPathLength = pathlength(startmove, endmove, ChestMarker.X, ChestMarker.Y, ChestMarker.Z)
HeadXPathLength, HeadYPathLength, HeadZPathLength, HeadThreeDPathLength = pathlength(startmove, endmove, HeadMarker.X, HeadMarker.Y, HeadMarker.Z)

# Append data to database
ith_parttrial = [part, Group, Age, Trial, Hand,
                HandMaxVel, HandMeanVel, HandMaxAccel, HandMeanAccel,HandMaxJerk, HandMeanJerk, HandJerkCost, HandXPathLength, HandYPathLength, HandZPathLength, HandThreeDPathLength,
                ChestMaxVel, ChestMeanVel, ChestMaxAccel, ChestMeanAccel, ChestMaxJerk, ChestMeanJerk, ChestJerkCost, ChestXPathLength, ChestYPathLength, ChestZPathLength, ChestThreeDPathLength,
                HeadMaxVel, HeadMeanVel, HeadMaxAccel, HeadMeanAccel, HeadMaxJerk, HeadMeanJerk, HeadJerkCost, HeadXPathLength, HeadYPathLength, HeadZPathLength, HeadThreeDPathLength]

db.loc[len(db)] = ith_parttrial

# Save database to CSV
db.to_csv("IMDRC2021_HandChestHead_05102021")


