import matplotlib.pyplot as plt

import SignalParameterExtractor
from SignalParameterExtractor import SignalParameterExtractor as SPE

def ExctractParameters(fullpath):
    spe = SignalParameterExtractor.SignalParameterExtractor
    sampleRate,data = spe.ReadWavfile(spe,fullpath)
    print(sampleRate)

    magnitude, phase = spe.ExctractTemporalEnvelope(spe,data)
    fig, (ax0, ax1) = plt.subplots(nrows=2)
    ax0.plot( data, label='signal')
    ax0.plot( magnitude, label='Enveloppe')
    #ax0.set_xlim(12000,15000)
    ax1.plot(phase)
    plt.show()
    return
