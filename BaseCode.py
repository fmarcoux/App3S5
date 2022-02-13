
import GraphUtils as GU
import SignalUtils as SPE
import numpy as np
import scipy

def ComputeN():
    SPE.computeNForFIRFilterOfTemporalEnvelope(nbCoefficientInitial=800,numberOfZeros= 100000)

def ComputeAndShowEnvelope(data):
    reponseImpulsionnel = SPE.computeRIF(971,2*np.pi,np.pi/1000)
    tailleVecteurFinale = len(reponseImpulsionnel) + len(data) - 1
    dataPadde = SPE.PaddZero(abs(data), tailleVecteurFinale - len(data))
    reponseImpulsionnelPadde = SPE.PaddZero(reponseImpulsionnel, tailleVecteurFinale - len(reponseImpulsionnel))
    enveloppeTemporelle = np.convolve(reponseImpulsionnelPadde, dataPadde)
    GU.ShowGraphs([enveloppeTemporelle, abs(data)], xlim=[0, 160000])
    GU.ShowOnSameGraph([enveloppeTemporelle, abs(data)], xlim=[0, 160000])

def ExctractSinus(data):
    dataFenetre = SPE.HanningWindow(data)
    gain,phase = SPE.FFT(dataFenetre)
    gainEnDb = GU.setDbScale(gain,gain[0])
    #GU.ShowGraphs([gainEnDb,phase],freqNormalise=True,xlim=[0,2])
    Exctract32sinus(gainEnDb)
    return


def Keep32(gainSup):
    sorted_by_second = sorted(gainSup, key=lambda tup: tup[1])
    L = len(sorted_by_second)
    return sorted_by_second[L-32:L]

def Exctract32sinus(magnitudeEnDb):
    gainSup = []

    #Puisqu'on a le complexe comjuge d'un cote te de lautre, on analyse seulement la moité des amplitude
    for n in range(0,round(len(magnitudeEnDb)/2)):
        if magnitudeEnDb[n] >0:
            gainSup.append((n,magnitudeEnDb[n]))
    sin32 = Keep32(gainSup)
    print("Nombre de sinus : ",len(sin32), "\n (Index,Gain) : ",sin32)
    return
