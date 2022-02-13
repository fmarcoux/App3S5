import BaseCode
import os

import GraphUtils
import SignalUtils as SPE

if __name__ == '__main__':
    workingDirectory = os.getcwd()
    dir = "WaveFiles"
    fileName = "note_guitare_LAd.wav"
    fullpath = f'{workingDirectory}\\{dir}\\{fileName}'

    SPE.computeFrequencyResponse(5)

    #sampleRate, data = SPE.ReadWavfile(fullpath)
    #magn,angle = SPE.FFT(data)
    #GraphUtils.ShowGraphs([magn,angle],titles=["magnitude","angles"],freqNormalise=True)


    #reponseImpulsionnel = SPE.computeRIF(159,sampleRate,22.05)
    #GraphUtils.ShowGraphs([reponseImpulsionnel],type="stem",scales=["log"])

    #GraphUtils.ShowGraphs([data],freqNormalise=True,freqEchantillonage=sampleRate)
    #frequenceNormalisepisur1000 = sampleRate/2*1000
    #print("frequence de coupure pi sur 1000",frequenceNormalisepisur1000,"\n frequence dechantillonage",sampleRate)
    #SPE.computeRIF(10,)
    #BaseCode.ExctractEnvelope(data)
    #data = SPE.HanningWindow(data)
    #magn,angle= SPE.FFT(data)

