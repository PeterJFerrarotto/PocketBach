# getRhythm returns an array of note durations for 1 full measure (rather than 1 note at a time)

import random

def getRhythm(finalMTX, measure, measures, voice=0, maxVoices=3, timeSig=[4,4], choraleOrFugue=0, subject=[]):
    rhythmArr = []
    newArr = []
    if measure == measures:  # if on the last measure, return a whole note
        return '1'
    elif measure == 1:  # if on the first measure
        if choraleOrFugue == 0:  # if a chorale
            num1 = random.random()
            # pick a random (common) rhythm
            # TO DO: fill this section
            pass

        else:  # if a fugue
            # TO DO: fill this section
            pass  # use subject

    else:
        num1 = random.random()
        if choraleOrFugue == 0:  # if a chorale
            if measure in [9,10,11,12]:  # measures 9-12
                # get index of current measure-8
                k = 0
                while finalMTX[maxVoices-1][k][11] != measure-8:
                    k+=1
                if num1 < 0.6:  # 60% chance to copy the same rhythms from measures 1-4
                    while finalMTX[maxVoices-1][k][11] == measure-8:  # while on the same measure
                        rhythmArr.append(finalMTX[maxVoices-1][k][1])
                        k+=1
                elif num1 < 0.9:  # 30% chance to pick a similar rhythm from measures 1-4
                    while finalMTX[maxVoices-1][k][11] == measure-8:
                        newArr.append(finalMTX[maxVoices-1][k][1])
                    rhythmArr = similarRhythm(newArr)
                else:  # just randomize
                    rhythmArr = randRhythm(timeSig, finalMTX[maxVoices-1][measure][3])  # pass interval
            else:  # just randomize
                rhythmArr = randRhythm(timeSig, finalMTX[maxVoices-1][measure][3])  # pass interval

    return rhythmArr


def randRhythm(timeSig = [4,4], interval = 0, common = 0):
    choices = []
    num1 = random.random()
    if timeSig == [4,4]:
        if common == 1:
            choices = [['1'], ['2', '2'], ['2', '4', '4'], ['4', '4', '2'], ['4', '4', '4', '4']]
        else:
            if num1 < 0.3:  # 30% chance to pick a common/simple rhythm regardless of interval
                choices = [['1'], ['2','2'], ['2','4','4'], ['4','4','2'], ['4','4','4','4']]
            elif num1 < 0.5: # 20% chance to simply pick a random choice regardless of interval
                choices = [['1'],
                           ['2~','4','4'], ['2~','4','8','8'], ['2~','8','8','4'], ['2~','8','8','8','8'],
                           ['2','2'], ['2','4','4'], ['2','4','8','8'], ['2','8','8','4'], ['2','8','8','8','8'],
                           ['4~','8','8','2'], ['4~','8','8','4~','8','8'], ['4~','8','8','4','4'],
                           ['4~','8','8','4','8','8'], ['4~','8','8','8','8','4'], ['4~','8','8','8','8','8','8'],
                           ['4','4~','4','4'], ['4','4~','4','8','8'], ['4','4~','8','8','4'],
                           ['4','4~','8','8','8','8'], ['4','4','2'], ['4','4','4~','8','8'], ['4','4','4','4'],
                           ['4','4','4','8','8'], ['4','4','8','8','4'], ['4','4','8','8','8','8'], ['4','8','8','2'],
                           ['4','8','8','4~','8','8'], ['4','8','8','4','4'], ['4','8','8','4','8','8'],
                           ['4','8','8','8','8','4'], ['4','8','8','8','8','8','8'],
                           ['8','8','4~','4','4'], ['8','8','4~','4','8','8'], ['8','8','4~','8','8','4'],
                           ['8','8','4~','8','8','8','8'], ['8','8','4','4~','8','8'], ['8','8','4','4','4'],  # on this line
                           ['8','8','4','4','8','8'], ['8','8','4','8','8','4'], ['8','8','4','8','8','8','8'],
                           ['8','8','8','8','4~','8','8'], ['8','8','8','8','4','4'],
                           ['8','8','8','8','4','8','8'], ['8','8','8','8','8','8','4'], ['8','8','8','8','8','8','8','8']]
            else:  # 50% chance to consider interval (NOTE: technically less than 50% because interval may be > 4 or < -4. see "else:" below)
                if interval == 0:
                    choices = [['2~','4','4'], ['2~','8','8','8','8'],
                               ['2','2'], ['2','4','8','8'], ['2','8','8','4'],
                               ['4~','8','8','4~','8','8'], ['4~','8','8','4','4'], ['4~','8','8','8','8','8','8'],
                               ['4','4~','4','8','8'], ['4','4~','8','8','4'], ['4','4','4~','8','8'], ['4','4','4','4'],
                               ['4','4','8','8','8','8'], ['4','8','8','2'], ['4','8','8','4','8','8'], ['4','8','8','8','8','4'],
                               ['8','8','4~','4','4'],
                               ]  # TO DO: finish this list
                elif interval == 1 or interval == -1:
                    choices = [['1'],
                               ['2~','4','8','8'], ['2~','8','8','4'], ['2','4','4'], ['2','8','8','8','8'],
                               ['4~','8','8','2'], ['4~','8','8','4','8','8'], ['4~','8','8','8','8','4'],
                               ['4','4~','4','4'], ['4','4~','8','8','8','8'], ['4','4','2'], ['4','4','4','8','8'],
                               ['4','4','8','8','4'], ['4','8','8','4~','8','8'], ['4','8','8','4','4'], ['4','8','8','8','8','8','8'],
                               ['8','8','4~','4','8','8'], ['8','8','4~','8','8','4'],
                               ]   # TO DO: finish this list
                elif interval == 2 or interval == -2:
                    pass   # TO DO: finish this, same as interval == 0. keep separate though for future
                elif interval == 3 or interval == -3:
                    pass   # TO DO: finish this, same as interval == 1/-1 except for ['1']
                elif interval == 4 or interval == -4:
                    pass   # TO DO: finish this, same as interval == 2/-2 except for ['2~','4','4'], ['2','2']
                else:  # otherwise just use a random choice
                    choices = [['1'],
                               ['2~','4','4'], ['2~','4','8','8'], ['2~','8','8','4'], ['2~','8','8','8','8'],
                               ['2','2'], ['2','4','4'], ['2','4','8','8'], ['2','8','8','4'], ['2','8','8','8','8'],
                               ['4~','8','8','2'], ['4~','8','8','4~','8','8'], ['4~','8','8','4','4'],
                               ['4~','8','8','4','8','8'], ['4~','8','8','8','8','4'], ['4~','8','8','8','8','8','8'],
                               ['4','4~','4','4'], ['4','4~','4','8','8'], ['4','4~','8','8','4'],
                               ['4','4~','8','8','8','8'], ['4','4','2'], ['4','4','4~','8','8'], ['4','4','4','4'],
                               ['4','4','4','8','8'], ['4','4','8','8','4'], ['4','4','8','8','8','8'], ['4','8','8','2'],
                               ['4','8','8','4~','8','8'], ['4','8','8','4','4'], ['4','8','8','4','8','8'],
                               ['4','8','8','8','8','4'], ['4','8','8','8','8','8','8'],
                               ['8','8','4~','4','4'], ['8','8','4~','4','8','8'], ['8','8','4~','8','8','4'],
                               ['8','8','4~','8','8','8','8'], ['8','8','4','4~','8','8'], ['8','8','4','4','4'],
                               ['8','8','4','4','8','8'], ['8','8','4','8','8','4'], ['8','8','4','8','8','8','8'],
                               ['8','8','8','8','4~','8','8'], ['8','8','8','8','4','4'],
                               ['8','8','8','8','4','8','8'], ['8','8','8','8','8','8','4'], ['8','8','8','8','8','8','8','8']]


    index = random.randint(0,len(choices)-1)  # note: randint(a, b) b is inclusive
    return choices[index]


def similarRhythm(oldRhythm):

    # based on old rhythm, look up an array of similar rhythms
    # NOTE: must put spaces after commas in keys!!! I tested this.
    choices = {
        "['1']": [['1'],['2','2'],['2~','4','4']],
        "['2', '2']": [['2','2'],['2~','4','4'],['2','4','4']]
        # TO DO: add more keys and similar rhythms
    }.get(str(oldRhythm),[oldRhythm,])  # NOTE: we have to default to [oldRhythm,] instead of just oldRhythm
                                        #   or indexing below will cause an error

    # pick a random similar rhythm from the list
    return choices[random.randint(0,len(choices)-1)]

