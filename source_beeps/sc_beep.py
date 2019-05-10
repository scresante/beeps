import os
import re
from sys import getsizeof

BEEPDIR='/home/shawn/Code/circuitpython/beeps'
os.chdir(BEEPDIR)
validshells = [_ for _ in os.listdir() if _.find('0') != 0 and _.find('.sh') > 0]

class beep():
    ''' this is a helper class to parse beep sh scripts
    the scripts must be preprocessed by hand:
    this class does not do things like emulate shell 
    variable replacement. 
    not to be run from a CPX, but used to create .beep files'''

    # this dict is really for debugging
    beeplibrary = {}
    def __init__(self):
        pass
    def parse_oneline(self,beepline):
        '''TODO: IMPLEMENT -d DELAY | -D DELAY see `man beep`.'''
        beepline = beepline.split('-n')
        tone_list = []

        def getrepeat(x):
            try: r = int(re.search(r'-r ?(\S+)', x).group(1))
            except: r = 1
            return r
        def getdelay(x):
            try: d = int(re.search(r'-[Dd] ?(\S+)', x).group(1))
            except: d = 0
            return d
        
        def getlen(x, deflen=250):
            try: l = int(re.search(r'-l ?(\S+)', x).group(1))
            except: l = deflen
            return l
        getfreq = lambda x: int(float(re.search(r'-f ?(\S+)', x).group(1)))

        for abeep in beepline:
            freq,duration = getfreq(abeep), getlen(abeep)
            delay = getdelay(abeep)
            repeat = getrepeat(abeep)
            for _ in range(repeat):
                tone_list.append((freq, duration, delay))

        return tone_list

    def beepreader(self, fname):
        beepdata = []
        ''' reads a clean* beep script '''
        with open(fname, "r") as f:
            lines = f.readlines()
        for line in lines:
            if line.find('beep') == 0:
                beepdata += self.parse_oneline(line)
        return beepdata

q = beep()

for shellfile in validshells:
    # print(f'reading {shellfile}', end=' ')
    q.beeplibrary[shellfile] = q.beepreader(shellfile)
    newf = shellfile.replace('.sh','.beep')
    with open(newf, 'w') as f:
        f.write(str(q.beepreader(shellfile)))
