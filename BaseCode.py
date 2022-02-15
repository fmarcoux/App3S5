import scipy

import GraphUtils as GU
import SignalUtils
import SignalUtils as SPE
import numpy as np

def ComputeN():
    print(SPE.computeNForFIRFilterOfTemporalEnvelope())

def ComputeEnvelope(K,data):
    K = 886
    h = SignalUtils.GetCoefficient(K)
    return np.convolve(data, h)


    #reponseImpulsionnel = SPE.GetCoefficient(886)
    #tailleVecteurFinale = len(reponseImpulsionnel) + len(data) - 1
    #dataPadde = SPE.PaddZero(abs(data), tailleVecteurFinale - len(data))
    #reponseImpulsionnelPadde = SPE.PaddZero(reponseImpulsionnel, tailleVecteurFinale - len(reponseImpulsionnel))
    #enveloppeTemporelle = np.convolve(reponseImpulsionnelPadde, dataPadde)
    #GU.ShowGraphs([enveloppeTemporelle, abs(data)], xlim=[0, 160000])
    #GU.ShowOnSameGraph([enveloppeTemporelle, abs(data)], xlim=[0, 160000])


def constructNote(sinus,enveloppeTemporel):
    longeur = len(enveloppeTemporel-1)
    max = np.max(enveloppeTemporel)
    dataNote = [0 for i in range(0,longeur)]
    for (Hz,Gain,Phase) in sinus:
        print(f"Computing sinus of : {Hz} Hz with gain : {Gain} and phase {Phase}")
        sin = [np.sin(Hz*2*np.pi*n + Phase) for n in range(0,longeur)]
        for i in range(0,longeur):
            dataNote[i] += sin[i]
    dataNote = [dataNote[k]*enveloppeTemporel[k]/32*max for k in range(0,longeur)]
    GU.ShowGraphs([dataNote])
    return dataNote


def Exctract32Sinus(data):
    dataFenetre = SPE.HanningWindow(data)
    GU.ShowGraphs([dataFenetre])
    response = np.fft.fft(dataFenetre)
    responseDb = 20*np.log10(np.abs(response))
    angle = np.angle(response)
    peaks = scipy.signal.find_peaks(responseDb, distance=1690)
    peaks32 = peaks[0][0:32]
    return peaks32,np.abs(response),angle







