import os, pandas, numpy, sys
from scipy import signal
import matplotlib.pyplot as plt
from read_trc import read_trc
from read_filenames import read_filenames
from pathlength import pathlength
from jerkcost import jerkcost

# Workspace and directory definitions
home = os.getcwd()
# dataloc = 'D:/Dropbox (University of Michigan)/Python'
dataloc = 'F:/Projects/VIADL/Data/Cortex'
# dataloc = "C:/Users/nefea/Dropbox (University of Michigan)/Python"
os.chdir(dataloc)
DemoData = pandas.read_excel('INSARDemoData.xlsx')
CupData = pandas.read_excel('INSARCupData.xlsx', sheet_name='CupLocation')
mouthdist = 75
handcupdist=50
percentstartthresh = .10
percentstopthresh = .10
framerate = 120
filter_type = 'lowpass'
filter_order = 4
filter_cutoff = 10/(framerate/2)

outputfilename = "Combined_IMDRC2021_HandChestHead_05262021_105075_10Hzfiltered_test2.csv"

# Create database using Pandas dataframe
db = pandas.DataFrame(columns=['ID', 'Group', 'Age', 'Trial', 'Hand', 'ReactionTime', 'MovementDur', 'CupMoveDur', 'MouthMoveDur',
                                'HandCupMoveMaxVel', 'HandCupMoveMeanVel', 'CupMoveTimetoMaxPeak', 'HandMouthMoveMaxVel', 'HandMouthMoveMeanVel', 'MouthMoveTimetoMaxPeak',
                               'HandMaxVel', 'HandMeanVel', 'HandMaxAccel', 'HandMeanAccel','HandMaxJerk', 'HandMeanJerk', 'HandJerkCost', 'HandXPathLength', 'HandYPathLength', 'HandZPathLength', 'HandThreeDPathLength',
                               'ChestMaxVel', 'ChestMeanVel', 'ChestMaxAccel', 'ChestMeanAccel','ChestMaxJerk', 'ChestMeanJerk', 'ChestJerkCost', 'ChestXPathLength', 'ChestYPathLength', 'ChestZPathLength', 'ChestThreeDPathLength',
                               'HeadMaxVel', 'HeadMeanVel', 'HeadMaxAccel', 'HeadMeanAccel','HeadMaxJerk', 'HeadMeanJerk', 'HeadJerkCost', 'HeadXPathLength', 'HeadYPathLength', 'HeadZPathLength', 'HeadThreeDPathLength'])
db.to_csv(outputfilename, mode='w', index=False)

# Loop through all parts in DemoData
for part in sorted(DemoData.ID):
    # Save for each part
    Group = DemoData.loc[numpy.where(DemoData.ID == part)[0], 'Group'].item()
    Age = DemoData.loc[numpy.where(DemoData.ID == part)[0], 'Age'].item()
    CupLocs = CupData[CupData.ID == part]

    # Find TRC file names by part
    folder = dataloc + '/' + part + '/Tracked + Packaged/TRC'
    os.chdir(folder)
    files = sorted(read_filenames(['cup', 'UPPER.trc']))

    # For loop by number of trials within part
    for filenum in range(0, len(files)):
        if 'Trial' in locals():
            del [Trial, Hand, CupLoc, HandMarker, ChestMarker, HeadMarker]
        try:
            if 'startmove' in locals():
                del [startmove, endmove, ReactionTime, MovementDur, CupMoveDur, MouthMoveDur,
                   HandCupMoveMaxVel, HandCupMoveMeanVel, CupMoveTimetoMaxPeak, HandMouthMoveMaxVel, HandMouthMoveMeanVel, MouthMoveTimetoMaxPeak, HandMaxVel, HandMeanVel, HandMaxAccel, HandMeanAccel,HandMaxJerk, HandMeanJerk, HandJerkCost, HandXPathLength, HandYPathLength, HandZPathLength, HandThreeDPathLength,
                   ChestMaxVel, ChestMeanVel, ChestMaxAccel, ChestMeanAccel, ChestMaxJerk, ChestMeanJerk, ChestJerkCost, ChestXPathLength, ChestYPathLength, ChestZPathLength, ChestThreeDPathLength,
                   HeadMaxVel, HeadMeanVel, HeadMaxAccel, HeadMeanAccel, HeadMaxJerk, HeadMeanJerk, HeadJerkCost, HeadXPathLength, HeadYPathLength, HeadZPathLength, HeadThreeDPathLength]
        except Exception:
            print("Unexpected error during deleting: ", sys.exc_info()[0])
        # Read in TRC data
        filename = files[filenum]
        TRC = read_trc(filename, folder, home)
        StartRow = 0
        EndRow = len(TRC.index)

        frametime = numpy.mean(numpy.diff(TRC.Time))

        # Read in cup data per part per trial
        CupLoc = CupLocs[CupLocs.Trial == filenum+1]
        CupMarker = pandas.DataFrame([[CupLoc.CupBMX.item(), CupLoc.CupBMY.item(), CupLoc.CupBMZ.item()]], columns=['X','Y','Z'])


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

        print("Starting " + part + " " + Hand + " Hand, Trial " + str(Trial))
        try:
            # Derivatives
            # Create butterworth filter
            b, a = signal.butter(filter_order, filter_cutoff, filter_type)

            # Hand
            HandPosDiff = numpy.empty([1, 0])  # empty numpy.array to collect data
            markers = numpy.asarray(list(zip(HandMarker.X, HandMarker.Y, HandMarker.Z)))
            for pt1, pt2 in zip(markers, markers[1:]):
                HandPosDiff = numpy.append(HandPosDiff, numpy.linalg.norm(pt2 - pt1, 2))

            Handvel = signal.filtfilt(b, a, (HandPosDiff / frametime))
            Handaccel = signal.filtfilt(b, a, (numpy.diff(Handvel) / frametime))
            Handjerk = signal.filtfilt(b, a, (numpy.diff(Handaccel) / frametime))

            # Chest
            ChestPosDiff = numpy.empty([1, 0])  # empty numpy.array to collect data
            markers = numpy.asarray(list(zip(ChestMarker.X, ChestMarker.Y, ChestMarker.Z)))
            for pt1, pt2 in zip(markers, markers[1:]):
                ChestPosDiff = numpy.append(ChestPosDiff, numpy.linalg.norm(pt2 - pt1, 2))

            Chestvel = signal.filtfilt(b, a, (ChestPosDiff / frametime))
            Chestaccel = signal.filtfilt(b, a, (numpy.diff(Chestvel) / frametime))
            Chestjerk = signal.filtfilt(b, a, (numpy.diff(Chestaccel) / frametime))

            # Head
            HeadPosDiff = numpy.empty([1, 0])  # empty numpy.array to collect data
            markers = numpy.asarray(list(zip(HeadMarker.X, HeadMarker.Y, HeadMarker.Z)))
            for pt1, pt2 in zip(markers, markers[1:]):
                HeadPosDiff = numpy.append(HeadPosDiff, numpy.linalg.norm(pt2 - pt1, 2))

            Headvel = signal.filtfilt(b, a, (HeadPosDiff / frametime))
            Headaccel = signal.filtfilt(b, a, (numpy.diff(Headvel) / frametime))
            Headjerk = signal.filtfilt(b, a, (numpy.diff(Headaccel) / frametime))

            # Find start and end of movement
            # start of movement
            over_thresh = abs(Handvel[61:len(Handvel)+1]) > (Handvel.max()*percentstartthresh)
            frames_over = numpy.asarray(numpy.where(over_thresh == 1))+61
            for j in range(frames_over.shape[1]-12):
                if frames_over[:, j+12]-frames_over[:, j] == 12:
                    startmove = int(frames_over[:, j])
                    break

            # end of movement
            under_thresh = abs(Handvel[startmove:len(Handvel)+1]) < (Handvel.max()*percentstopthresh)
            frames_under = numpy.asarray(numpy.where(under_thresh == 1))+startmove
            move_stops = frames_under[:, numpy.where(numpy.diff(frames_under) > 1)[1]+1]
            mouth_stops = numpy.empty([1, 0])
            for i in range(len(move_stops[0])):
                if abs(HeadMarker.Z[move_stops[0][i]]-HandMarker.Z[move_stops[0][i]]) < mouthdist:
                    mouth_stops = numpy.append(mouth_stops, move_stops[0][i])
            endmove = int(mouth_stops[0])

            # Segmenting the movement
            for i in range(len(Handvel[startmove:endmove]) + 1):
                if (HandMarker.Z[startmove + i] - CupMarker.Z[0] < handcupdist) and (Handvel[startmove + i] < Handvel.max() * percentstopthresh):
                    CupReach = startmove + i
                    break

            # Distance between hand and cup
            CupDistX = abs(CupMarker.X[0] - HandMarker.X[startmove])
            CupDistY = abs(CupMarker.Y[0] - HandMarker.Y[startmove])
            CupDistZ = abs(CupMarker.Z[0] - HandMarker.Z[startmove])
            CupDist3D = abs(numpy.linalg.norm(numpy.asarray(CupMarker.iloc[[0]]) - numpy.asarray(HandMarker.iloc[[startmove]]), 2))

            # Reaction Time and Movement Time
            ReactionTime = TRC.Time[startmove]-TRC.Time[61]
            MovementDur = TRC.Time[endmove]-TRC.Time[startmove]
            MouthMoveDur = TRC.Time[CupReach] - TRC.Time[startmove]
            CupMoveDur = TRC.Time[endmove] - TRC.Time[CupReach]

            # Maximum and mean derivatives
            # Hand
            HandMaxVel = numpy.amax(Handvel[startmove:endmove])
            HandMeanVel = numpy.mean(Handvel[startmove:endmove])
            HandMaxAccel = numpy.amax(Handaccel[startmove:endmove])
            HandMeanAccel = numpy.mean(Handaccel[startmove:endmove])
            HandMaxJerk = numpy.amax(Handjerk[startmove:endmove])
            HandMeanJerk = numpy.mean(Handjerk[startmove:endmove])

            # Reaching to the Cup
            HandCupMoveMaxVel = numpy.amax(Handvel[startmove:CupReach])
            HandCupMoveMeanVel = numpy.mean(Handvel[startmove:CupReach])
            HandCupMoveMaxAccel = numpy.amax(Handaccel[startmove:CupReach])
            HandCupMoveMeanAccel = numpy.mean(Handaccel[startmove:CupReach])
            HandCupMoveMaxJerk = numpy.amax(Handjerk[startmove:CupReach])
            HandCupMoveMeanJerk = numpy.mean(Handjerk[startmove:CupReach])

            CupMoveTimetoMaxPeak = TRC.Time[startmove + numpy.where(Handvel[startmove:CupReach] == HandCupMoveMaxVel)[0][0]] - TRC.Time[startmove]

            # Bringing Cup to the Mouth
            HandMouthMoveMaxVel = numpy.amax(Handvel[CupReach:endmove])
            HandMouthMoveMeanVel = numpy.mean(Handvel[CupReach:endmove])
            HandMouthMoveMaxAccel = numpy.amax(Handaccel[CupReach:endmove])
            HandMouthMoveMeanAccel = numpy.mean(Handaccel[CupReach:endmove])
            HandMouthMoveMaxJerk = numpy.amax(Handjerk[CupReach:endmove])
            HandMouthMoveMeanJerk = numpy.mean(Handjerk[CupReach:endmove])

            MouthMoveTimetoMaxPeak = TRC.Time[CupReach + numpy.where(Handvel[CupReach:endmove] == HandMouthMoveMaxVel)[0][0]] - TRC.Time[CupReach]

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

            HandXPathLength = HandXPathLength/CupDistX
            HandYPathLength = HandYPathLength/CupDistY
            HandZPathLength = HandZPathLength/CupDistZ
            HandThreeDPathLength = HandThreeDPathLength/CupDist3D

            ChestXPathLength = ChestXPathLength/CupDistX
            ChestYPathLength = ChestYPathLength/CupDistY
            ChestZPathLength = ChestZPathLength/CupDistZ
            ChestThreeDPathLength = ChestThreeDPathLength/CupDist3D

            HeadXPathLength = HeadXPathLength/CupDistX
            HeadYPathLength = HeadYPathLength/CupDistY
            HeadZPathLength = HeadZPathLength/CupDistZ
            HeadThreeDPathLength = HeadThreeDPathLength/CupDist3D

            # Append data to database
            ith_parttrial = [part, Group, Age, Trial, Hand, ReactionTime, MovementDur, CupMoveDur, MouthMoveDur,
                            HandCupMoveMaxVel, HandCupMoveMeanVel, CupMoveTimetoMaxPeak, HandMouthMoveMaxVel, HandMouthMoveMeanVel, MouthMoveTimetoMaxPeak,
                            HandMaxVel, HandMeanVel, HandMaxAccel, HandMeanAccel,HandMaxJerk, HandMeanJerk, HandJerkCost, HandXPathLength, HandYPathLength, HandZPathLength, HandThreeDPathLength,
                            ChestMaxVel, ChestMeanVel, ChestMaxAccel, ChestMeanAccel, ChestMaxJerk, ChestMeanJerk, ChestJerkCost, ChestXPathLength, ChestYPathLength, ChestZPathLength, ChestThreeDPathLength,
                            HeadMaxVel, HeadMeanVel, HeadMaxAccel, HeadMeanAccel, HeadMaxJerk, HeadMeanJerk, HeadJerkCost, HeadXPathLength, HeadYPathLength, HeadZPathLength, HeadThreeDPathLength]

            db.loc[len(db)] = ith_parttrial

            # # Plot figure to check data
            # fig, (Xposplot, Yposplot, Zposplot, velplot, accelplot, jerkplot) = plt.subplots(6, 1)
            # fig.suptitle(part + '- ' + Hand + ' Hand, Trial ' + Trial)
            # Time = TRC.Time[0:endmove]
            # plt.xticks(numpy.arange(min(Time), max(Time) + 1, .5))
            # Xposplot.plot(Time[0:endmove], (HandMarker.X[0:endmove]) - HandMarker.X[startmove])
            # Xposplot.set_ylabel('X Position')
            # Xposplot.axvline(x=.5, color='blue')
            # Xposplot.axvline(x=Time[startmove], color='green')
            # Xposplot.axvline(x=Time[CupReach], color='orange')
            # Xposplot.axvline(x=Time[endmove], color='red')
            #
            # Yposplot.plot(Time[0:endmove], HandMarker.Y[0:endmove] - HandMarker.Y[startmove])
            # Yposplot.set_ylabel('Y Position')
            # Yposplot.axvline(x=.5, color='blue')
            # Yposplot.axvline(x=Time[startmove], color='green')
            # Yposplot.axvline(x=Time[CupReach], color='orange')
            # Yposplot.axvline(x=Time[endmove], color='red')
            #
            # Zposplot.plot(Time[0:endmove], (HandMarker.Z[0:endmove] - HandMarker.Z[startmove]) * -1)
            # Zposplot.set_ylabel('Z Position')
            # Zposplot.axvline(x=.5, color='blue')
            # Zposplot.axvline(x=Time[startmove], color='green')
            # Zposplot.axvline(x=Time[CupReach], color='orange')
            # Zposplot.axvline(x=Time[endmove], color='red')
            #
            # velplot.plot(Time[0:endmove], Handvel[0:endmove])
            # velplot.set_ylabel('Velocity')
            # velplot.axvline(x=.5, color='blue')
            # velplot.axvline(x=Time[startmove], color='green')
            # velplot.axvline(x=Time[CupReach], color='orange')
            # velplot.axvline(x=Time[endmove], color='red')
            #
            # accelplot.plot(Time[0:endmove], Handaccel[0:endmove])
            # accelplot.set_ylabel('Acceleration')
            # accelplot.axvline(x=.5, color='blue')
            # accelplot.axvline(x=Time[startmove], color='green')
            # accelplot.axvline(x=Time[CupReach], color='orange')
            # accelplot.axvline(x=Time[endmove], color='red')
            #
            # jerkplot.plot(Time[0:endmove], Handjerk[0:endmove])
            # jerkplot.set_ylabel('Jerk')
            # jerkplot.set_xlabel('Time (ms)')
            # jerkplot.axvline(x=.5, color='blue')
            # jerkplot.axvline(x=Time[startmove], color='green')
            # jerkplot.axvline(x=Time[CupReach], color='orange')
            # jerkplot.axvline(x=Time[endmove], color='red')

            print("Completed " + part + " " + Hand + " Hand, Trial " + str(Trial))
        except Exception:
            print(part + " " + Hand + " Hand, Trial " + str(Trial) + " failed!", "\n",
                  "Unexpected error: ", sys.exc_info()[0])
            continue



# Save database to CSV
os.chdir(dataloc)
db.to_csv(outputfilename, mode='a', header=False, index=False)

