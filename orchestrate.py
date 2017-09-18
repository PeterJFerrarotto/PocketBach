# orchestrate() fleshes out all voices for a given chord matrix

import numpy as np
import random
import getNextNote as gnn
import defineChord as dc
import pitchToNum as ptn

def orchestrate(key, major, noteMTX, chordsPerMeasure, beatsPerMeasure, measures, maxVoices):
    # 3 dimensional matrix finalMTX contains the fully orchestrated chorale
    # x = time (16 chords)
    # y = note (12 note and chord data)
    #   12 note data types: pitch, duration, direction, interval, chord root,
    #       7th chord, tonality, inversion, prev chord root, pickup, beat, measure
    # z = voice (3 voices)
    #   0 = bass, 1 = alto/tenor, 2 = soprano

    # OLD CRAP I TRIED - keeping for legacy
    #finalMTX = [[['r', 'r', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] * 16] * 3  # THIS DOESN'T WORK, USE NUMPY
    #finalMTX.fill(0)                # fill it with 0s, this will make everything an int though...
    #finalMTX.shape = (16, 12, 3)    # define dimensions

    # NOTE: THE NEW WAY OF DOING THIS USES STRUCTS TO ALLOW MULTIPLE TYPES INTO THE MATRIX.
    #       this 'removes' the note data dimension, though it can still be accessed with finalMTX[voice][measure][note data]
    # TO DO: swap the dimensions from [measure][note data][voice] to [voice][measure][note data]
    finalMTX = np.array([('r', 'r', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)],
                        dtype=[('pitch','S5'),('duration','S5'),('direction','i4'),
                        ('interval', 'i4'), ('chordRoot', 'i4'), ('seventhChord', 'i4'),
                        ('tonality', 'i4'), ('inversion', 'i4'), ('prevRoot', 'i4'),
                        ('pickup', 'i4'), ('beat', 'i4'), ('measure', 'i4')])
    for i in range(4):  # only 4 because finalMTX doubles in size each time, so 2^4 = 16
        finalMTX = np.concatenate((finalMTX, finalMTX),0)
    finalMTX = np.expand_dims(finalMTX, 0)  # add the 3rd dimension as new 1st dimension
    copyMTX = finalMTX  # copy for tacking on later
    finalMTX = np.concatenate((finalMTX, finalMTX),0)  # create more voices
                                                       # NOTE: i tried making it the 3rd but it won't work...
    finalMTX = np.concatenate((finalMTX, copyMTX),0)   # tack on one more 16x12 grid to make it 3x16x12
                                                       # NOTE: can't use (finalMTX, finalMTX) or it will double to 4x16x12
    # debugging
    # print(finalMTX.shape)
    # finalMTX[2][15][11] = 42
    # print(finalMTX)
    # print("Testing:", finalMTX[2][15][11])

    ################################################################
    # initialize the first chord
    ################################################################
    # bass
    finalMTX[0][0][0] = '1'
    finalMTX[0][0][1] = str(chordsPerMeasure)    # TO DO: fix this for non-4/4
    finalMTX[0][0][4] = 1
    finalMTX[0][0][10] = 1
    finalMTX[0][0][11] = 1
    # alto/tenor
    chordNotes = [1, 3, 5]  # create array for random to choose from below
    finalMTX[1][0][0] = str(chordNotes[random.randint(1, 3)-1])  # pick 1, 3, or 5
    finalMTX[1][0][1] = str(chordsPerMeasure)    # TO DO: fix this for non-4/4
    finalMTX[1][0][4] = 1
    finalMTX[1][0][10] = 1
    finalMTX[1][0][11] = 1
    # soprano
    if finalMTX[1][0][0] == '1':      # if 2 roots, must pick 3rd
        finalMTX[2][0][0] = '3'
    elif finalMTX[1][0][0] == '3':    # if root and 3rd, can pick 1 or 5
        chordNotes = [1, 5]
        finalMTX[2][0][0] = str(chordNotes[random.randint(1, 2)-1])
    else:                           # if root and 5th, must pick 3rd
        finalMTX[2][0][0] = '3'
    finalMTX[2][0][1] = str(chordsPerMeasure)    # TO DO: fix this for non-4/4
    finalMTX[2][0][4] = 1
    finalMTX[2][0][10] = 1
    finalMTX[2][0][11] = 1

    ################################################################
    # orchestrate the remaining chords
    ################################################################
    # NOTE: check for parallel 5ths, parallel octaves, tri-tones - redo a chord that fails check

    for i in range(1, measures):

        # TO DO: add while loop around each voice for validation until acceptable note is chosen
        #   if no acceptable note available, decrement i and rewrite previous choices

        # bass
        finalMTX[0][i][0] = str(gnn.getNextNote(key, major, noteMTX, finalMTX, i, measures, 0, maxVoices))
        # fill out inversion column for the other voices to follow rules
        chordArr = dc.defineChord(key, major, noteMTX[i][4], noteMTX[i][5], noteMTX[i][6])
        if finalMTX[0][i][0] == ptn.pitchToNum(chordArr[0]):
            finalMTX[0][i][7] = 0
        elif finalMTX[0][i][0] == ptn.pitchToNum(chordArr[1]):
            finalMTX[0][i][7] = 1
        elif finalMTX[0][i][0] == ptn.pitchToNum(chordArr[2]):
            finalMTX[0][i][7] = 2
        else:
            finalMTX[0][i][7] = 3  # 7th chords have 3rd inversion

        # soprano
        finalMTX[2][i][0] = str(gnn.getNextNote(key, major, noteMTX, finalMTX, i, measures, 2, maxVoices))  # soprano

        # alto/tenor:
        finalMTX[1][i][0] = str(gnn.getNextNote(key, major, noteMTX, finalMTX, i, measures, 1, maxVoices))  # alto/tenor

        # set all columns for i-th row of finalMTX using noteMTX
        #   12 note data types: pitch, duration, direction, interval, chord root,
        #       7th chord, tonality, inversion, prev chord root, pickup, beat, measure
        for voice in range(3):
            finalMTX[voice][i][1] = chordsPerMeasure    # duration

            # voice 0 interval
            if finalMTX[voice][i][0] == '1' or finalMTX[voice][i][0] == '2':    # interval, must check for 'wrapping'
                if finalMTX[voice][i-1][0] == '6' or finalMTX[voice][i-1][0] == '7':
                    temp = int(finalMTX[voice][i][0]) - int(finalMTX[voice][i-1][0])
                    if temp < 0:
                        temp += 7
                    finalMTX[0][i][3] = temp
                else:
                    finalMTX[voice][i][3] = finalMTX[voice][i][0] - finalMTX[voice][i-1][0]
            elif finalMTX[voice][i][0] == '6' or finalMTX[voice][i][0] == '7':
                if finalMTX[voice][i-1][0] == '1' or finalMTX[voice][i-1][0] == '2':
                    temp = int(finalMTX[voice][i][0]) - int(finalMTX[voice][i-1][0])
                    if temp > 0:
                        temp -= 7
                    finalMTX[voice][i][3] = temp
                else:
                    finalMTX[voice][i][3] = int(finalMTX[voice][i][0]) - int(finalMTX[voice][i-1][0])
            else:
                finalMTX[voice][i][3] = int(finalMTX[voice][i][0]) - int(finalMTX[voice][i-1][0])

            if finalMTX[voice][i][3] == 0:                              # direction
                finalMTX[voice][i][2] = 0
            elif finalMTX[voice][i][3] > 0:
                finalMTX[voice][i][2] = 1
            else:
                finalMTX[voice][i][2] = -1

            finalMTX[voice][i][4] = noteMTX[i][4]                       # chord root
            finalMTX[voice][i][5] = noteMTX[i][5]                       # 7th chord
            finalMTX[voice][i][6] = noteMTX[i][6]                       # tonality

            chordArr = dc.defineChord(key, major, noteMTX[i][4], noteMTX[i][5], noteMTX[i][6])  # inversion
            if finalMTX[voice][i][0] == ptn.pitchToNum(chordArr[0]):
                finalMTX[voice][i][7] = 0
            elif finalMTX[voice][i][0] == ptn.pitchToNum(chordArr[1]):
                finalMTX[voice][i][7] = 1
            elif finalMTX[voice][i][0] == ptn.pitchToNum(chordArr[2]):
                finalMTX[voice][i][7] = 2
            else:
                finalMTX[voice][i][7] = 3  # 7th chords have 3rd inversion

            finalMTX[voice][i][8] = noteMTX[i-1][4]                     # prev chord root
            finalMTX[voice][i][9] = 0                                   # pickup, none in bass
            finalMTX[voice][i][10] = noteMTX[i][10]                     # beat
            finalMTX[voice][i][11] = noteMTX[i][11]                     # measure


    #print(finalMTX)
    return finalMTX
