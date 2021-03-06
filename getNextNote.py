"""getNextNote() chooses the next note based on the previous note and current chord, returns an int (not a string)"""

import random
import numToPitch as ntp
import pitchToNum as ptn
import defineChord as dc

def getNextNote(key, major, noteMTX, finalMTX, index, measures, voice, maxVoices):
    # extract relevant data from matrices
    prevNote = int(finalMTX[voice][index - 1][0])   # previous note, TO DO: change this to a dictionary
    currentRoot = noteMTX[index][4]             # current chord root
    nextChord = 1                               # next chord root, currently unused
    if index < measures - 1:
        nextChord = noteMTX[index + 1][4]
    seventh = noteMTX[index][5]                 # seventh chord?
    tonality = noteMTX[index][6]                # tonal root?
    inversion = noteMTX[index][7]               # inversion

    # TO DO: need to add nextChord considerations!!
    #   especially for 7th chords because of 3rd inversion linear descents,
    #   but also for picking 2nd inversions, which should be rare if it isn't linear motion

    # for reference:
    # 12 note data types: pitch, duration, direction, interval, chord root,
    #   7th chord, tonality, inversion, prev chord root, distance, beat, measure

    # generate random number - PocketBach's soul...
    num1 = random.random()
    #print(num1)

    # track chord tones
    chordVec = dc.defineChord(key, major, currentRoot, seventh, tonality, inversion)
    #print(chordVec)


    ################################################################
    # bass
    ################################################################
    # RULES:
    # 7th chords with only 3 voices cannot be in 2nd inversion (5th in bass)
    # bass line has high chance to pick root, even if there's a jump
    # NOTE: use actual data to derive percentages based on each composer's preferences
    # TO DO: need to consider repeated pitches
    if voice == 0:
        #print(chordVec)

        # return 5th for I-6/4 chords in bass
        if currentRoot == 1 and inversion == 2:
            nextNote = currentRoot + 4
            if nextNote > 7:
                nextNote -= 7
            return nextNote

        # if on the 2nd to last measure return a 5
        if index == measures - 2:
            return 5

        # 7th chords with only 3 voices cannot be in 2nd inversion (5th in bass)
        if noteMTX[index][5] == 1 and maxVoices == 3:
            if inversion == 0:
                del chordVec[2]
            elif inversion == 1:
                del chordVec[1]
            elif inversion == 2:
                del chordVec[0]
            else:
                del chordVec[3]

        if num1 < 0.2:    # 20% chance to repeat bass note (technically less than 20%,
                            # because we check to see if prevNote is a chord tone)
            #print('staying the same')
            if ntp.numToPitch(key, prevNote) in chordVec:  # repeat prevNote if you can
                nextNote = prevNote
            else:  # otherwise just go with root
                nextNote = currentRoot
        elif num1 < 0.4:   # 20% chance to move up linearly (technically less than 20%,
                            # because we check to see if prevNote + 1 is a chord tone)
            #print('moving up')
            if prevNote == 7:  # if prevNote is 7, can't use prevNote + 1
                if ntp.numToPitch(key, 1) in chordVec:
                    nextNote = 1
                else:  # otherwise just go with root
                    nextNote = currentRoot
            else:  # if prevNote isn't 7, can use prevNote + 1
                if ntp.numToPitch(key, prevNote + 1) in chordVec:
                    nextNote = prevNote + 1
                else:  # otherwise just go with root
                    nextNote = currentRoot
        elif num1 < 0.6:   # 20% chance to move down linearly (technically less than 20%,
                # because we check to see if prevNote - 1 is a chord tone)
            #print('moving down')
            if prevNote == 1:  # if prevNote is 1, can't use prevNote - 1
                if ntp.numToPitch(key, 7) in chordVec:
                    nextNote = 7
                else:  # otherwise just go with root
                    nextNote = currentRoot
            else:  # if prevNote isn't 1, can use prevNote - 1
                if ntp.numToPitch(key, prevNote - 1) in chordVec:
                    nextNote = prevNote - 1
                else:  # otherwise just go with root
                    nextNote = currentRoot
        else:  # 40% chance to simply pick root
            nextNote = currentRoot

    ################################################################
    # soprano
    ################################################################
    # RULES:
    # can't be 3rd+3rd
    # can't be 5th+5th
    # 7th chords with 3 voices cannot have a 5th
    # 7th chords with 3 voices cannot be root+root
    # 7th chords with 3 voices cannot be 3rd+3rd
    # TO DO: no parallel 5ths or octaves
    # NOTE: use actual data to derive percentages based on each composer's preferences
    elif voice == 2:
        # enforce rules above by changing chordVec!!!
        # check for 7th chords first

        # first of all... if on the last measure, just return tonic
        if noteMTX[index][11] == measures:
            return 1

        if finalMTX[0][index][5] == 0:  # if not a 7th chord
            # can't be 3rd+3rd
            if inversion == 1:  # if inversion = 1
                del chordVec[0]
            # can't be 5th+5th
            elif inversion == 2:  # if inversion = 2
                del chordVec[0]
        else:  # if a 7th chord
            # 7th chords with 3 voices cannot have a 5th
            if maxVoices == 3:
                # 7th chords with 3 voices cannot be root+root
                if inversion == 0:  # if inversion = 0
                    chordVec = [chordVec[1], chordVec[3]]
                # 7th chords with 3 voices cannot be 3rd+3rd
                elif inversion == 1:  # if inversion = 1
                    chordVec = [chordVec[2], chordVec[3]]
                # elif inversion == 2:  # NOTE: this should never happen with only 3 voices...
                else:  # inversion == 3:  # if inversion = 3
                    # can only be root or 3rd
                    chordVec = [chordVec[1], chordVec[2]]
            else:
                # TO DO: 4-voice rules
                pass

        # all percentages are multiplied by 2.5/7 = 0.36 because there's only about a 2.5/7 chance
        #   for the prevNote or prevNote +1/-1 to be a chord tone
        # TO DO: right now it checks for upward motion first, so percentages of upward/downward
        #   motion aren't equal... need to equalize
        if num1 < 0.83:         # 83% * 0.36 = 30% chance to move up or down
            if prevNote == 7:   # if prevNote is 7, can't use prevNote + 1
                if ntp.numToPitch(key, 1) in chordVec:
                    return 1
            else:  # if prevNote isn't 7, can use prevNote + 1
                if ntp.numToPitch(key, prevNote + 1) in chordVec:
                    return prevNote + 1
            if prevNote == 1:  # if prevNote is 1, can't use prevNote - 1
                if ntp.numToPitch(key, 7) in chordVec:
                    return 7
            else:  # if prevNote isn't 1, can use prevNote - 1
                if ntp.numToPitch(key, prevNote - 1) in chordVec:
                    return prevNote - 1
        else:      # 100% * 0.36 = 36% * 0.7 (30% less chance to make it through first if) = 25% chance to repeat note
            if ntp.numToPitch(key, prevNote) in chordVec:
                return prevNote

        # there's a high chance the note will fall through the if-elifs above,
        #   so don't put this line into "else:"
        return ptn.pitchToNum(key, chordVec[random.randint(0, len(chordVec) - 1)])

    ################################################################
    # alto/tenor
    ################################################################
    # RULES:
    # if root+root, must be 3rd
    # if root+3rd, can be root or 5th
    # if root+5th, must be 3rd
    # if 3rd+root, can be root or 5th
    # can't be 3rd+3rd
    # if 3rd+5th, must be root
    # if 5th+root, must be 3rd
    # if 5th+3rd, must be root
    # can't be 5th+5th
    # can't be 7th+7th
    # 7th chords with 3 voices cannot have a 5th
    # 7th chords with 3 voices cannot be root+root
    # 7th chords with 3 voices cannot be 3rd+3rd
    # 7th chords with 3 voices with root+3rd, must be 7th
    # 7th chords with 3 voices with root+7th, must be 3rd
    # 7th chords with 3 voices with 3rd+root, must be 7th
    # 7th chords with 3 voices with 3rd+7th, must be 7th
    # 7th chords with 3 voices with 7th+root, must be 3rd
    # 7th chords with 3 voices with 7th+3rd, must be root
    # TO DO: no parallel 5ths or octaves
    # NOTE: use actual data to derive percentages based on each composer's preferences
    # TO DO: need to check for note chosen in voice 0 and 1...
    else:
        # enforce rules above by changing chordVec!!!
        # check for 7th chords first
        if finalMTX[0][index][5] == 0:  # if not a 7th chord
            if inversion == 0:  # if inversion = 0
                # if root+root, must be 3rd
                if str(int(finalMTX[2][index][0])) == ptn.pitchToNum(key, chordVec[0]):
                    return int(ptn.pitchToNum(key, chordVec[1]))  # NOTE: return
                # if root+3rd, can be root or 5th
                elif str(int(finalMTX[2][index][0])) == ptn.pitchToNum(key, chordVec[1]):
                    del chordVec[1]
                # if root+5th, must be 3rd
                else:
                    return int(ptn.pitchToNum(key, chordVec[1]))  # NOTE: return
            elif inversion == 1:  # if inversion = 1
                # if 3rd+root, can be root or 5th
                if str(int(finalMTX[2][index][0])) == ptn.pitchToNum(key, chordVec[2]):
                    del chordVec[0]
                # elif # can't be 3rd+3rd
                else:  # if 3rd+5th, must be root
                    return int(ptn.pitchToNum(key, chordVec[2]))  # NOTE: return
            elif inversion == 2:  # if inversion = 2
                # if 5th+root, must be 3rd
                if str(int(finalMTX[2][index][0])) == ptn.pitchToNum(key, chordVec[1]):
                    return int(ptn.pitchToNum(key, chordVec[2]))  # NOTE: return
                # elif # can't be 5th+5th
                else:  # if 5th+3rd, must be root
                    return int(ptn.pitchToNum(key, chordVec[1]))  # NOTE: return
        else:  # if a 7th chord
            # 7th chords with 3 voices cannot have a 5th
            if maxVoices == 3:
                if inversion == 0:  # if inversion = 0
                    # 7th chords with 3 voices cannot be root+root
                    # 7th chords with 3 voices with root+3rd, must be 7th
                    if str(int(finalMTX[2][index][0])) == ptn.pitchToNum(key, chordVec[1]):
                        return int(ptn.pitchToNum(key, chordVec[3]))  # NOTE: return
                    # elif # 7th chords with 3 voices cannot have a 5th
                    # 7th chords with 3 voices with root+7th, must be 3rd
                    else:
                        return int(ptn.pitchToNum(key, chordVec[1]))  # NOTE: return

                elif inversion == 1:  # if inversion = 1
                    # 7th chords with 3 voices with 3rd+root, must be 7th
                    if str(int(finalMTX[2][index][0])) == ptn.pitchToNum(key, chordVec[3]):
                        return int(ptn.pitchToNum(key, chordVec[2]))  # NOTE: return
                    # 7th chords with 3 voices cannot be 3rd+3rd
                    # 7th chords with 3 voices cannot have a 5th
                    # 7th chords with 3 voices with 3rd+7th, must be root
                    else:
                        return int(ptn.pitchToNum(key, chordVec[3]))  # NOTE: return
                # 7th chords with 3 voices cannot have a 5th, so no 2nd inversion
                else:  # if inversion = 3
                    # 7th chords with 3 voices with 7th+root, must be 3rd
                    if str(int(finalMTX[2][index][0])) == ptn.pitchToNum(key, chordVec[1]):
                        return int(ptn.pitchToNum(key, chordVec[2]))  # NOTE: return
                    # 7th chords with 3 voices with 7th+3rd, must be root
                    else:
                        return int(ptn.pitchToNum(key, chordVec[1]))  # NOTE: return
                    # 7th chords with 3 voices cannot have a 5th
                    # can't be 7th+7th

            # not relevant at the moment so skipping them...
            else:
                # TO DO: many possible combinations and rules for 4 voices below...
                pass

        if num1 < 0.4:  # 40% chance to repeat note (technically less)
                        # because we check to see if prevNote is a chord tone)
            if ntp.numToPitch(key, prevNote) in chordVec:
                nextNote = prevNote
            else:
                nextNote = ptn.pitchToNum(key, chordVec[random.randint(0, len(chordVec) - 1)])
        elif num1 < 0.7:    # 30% chance to move up linearly (technically less than 30%,
                            # because we check to see if prevNote + 1 is a chord tone)
            if prevNote == 7:  # if prevNote is 7, can't use prevNote + 1
                if ntp.numToPitch(key, 1) in chordVec:
                    nextNote = 1
                else:
                    nextNote = ptn.pitchToNum(key, chordVec[random.randint(0, len(chordVec) - 1)])
            else:  # if prevNote isn't 7, can use prevNote + 1
                if ntp.numToPitch(key, prevNote + 1) in chordVec:
                    nextNote = prevNote + 1
                else:
                    nextNote = ptn.pitchToNum(key, chordVec[random.randint(0, len(chordVec) - 1)])
        else:   # 30% chance to move down linearly (technically less than 30%,
                # because we check to see if prevNote - 1 is a chord tone)
            if prevNote == 1:  # if prevNote is 1, can't use prevNote - 1
                if ntp.numToPitch(key, 7) in chordVec:
                    nextNote = 7
                else:
                    nextNote = ptn.pitchToNum(key, chordVec[random.randint(0, len(chordVec) - 1)])
            else:  # if prevNote isn't 1, can use prevNote - 1
                if ntp.numToPitch(key, prevNote - 1) in chordVec:
                    nextNote = prevNote - 1
                else:
                    nextNote = ptn.pitchToNum(key, chordVec[random.randint(0, len(chordVec) - 1)])

    #print(chordVec)
    return nextNote


 # in the chorale we want just 1 note, but in the fugue we want an array to match rhythmArr
def getNextNoteArr(rhythmArr, destinationChord, intervalPatternsUsed):
    arrayOfNotes = []
    notesNeeded = 0
    nextNote = ''
    for i in rhythmArr:
        if i != '2~' and i != '4~':
            notesNeeded += 1

    # need either destinationChord or destinationPitch
    # assuming destinationChord for now
    for n in range(notesNeeded):
        # figure out the destinationPitch (getNextNote()? chord harmonization is less important)
        # get interval between currentPitch and destinationPitch
        # determine beat based on rhythmArr to know if you want harmonic/non-harmonic tones
        # first look for intervalPatternsUsed to see if you can re-use them
        # next, look for common patterns, like linear motion, appoggiaturas, cambiatas, anticipations
        # TO DO: decide if you want advanced non-chord tones like suspensions, this isn't a priority
        # if no patterns, just move semi-linearly toward the destinationPitch

        # TO DO: assign nextNote

        arrayOfNotes.append(nextNote)

    return arrayOfNotes

