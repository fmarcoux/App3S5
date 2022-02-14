
import GraphUtils as GU
import SignalUtils as SPE
import numpy as np
import scipy

def ComputeN():
    print(SPE.computeNForFIRFilterOfTemporalEnvelope())

def ComputeAndShowEnvelope(data):
    reponseImpulsionnel = SPE.GetCoefficient(886)
    tailleVecteurFinale = len(reponseImpulsionnel) + len(data) - 1
    dataPadde = SPE.PaddZero(abs(data), tailleVecteurFinale - len(data))
    reponseImpulsionnelPadde = SPE.PaddZero(reponseImpulsionnel, tailleVecteurFinale - len(reponseImpulsionnel))
    enveloppeTemporelle = np.convolve(reponseImpulsionnelPadde, dataPadde)
    #GU.ShowGraphs([enveloppeTemporelle, abs(data)], xlim=[0, 160000])
    #GU.ShowOnSameGraph([enveloppeTemporelle, abs(data)], xlim=[0, 160000])
    return enveloppeTemporelle

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


def ExctractSinus(data,samplerate,enveloppe):
    dataFenetre = SPE.HanningWindow(data)
    #GU.ShowGraphs([dataFenetre])
    gain,phase = SPE.FFT(dataFenetre)
    #GU.ShowGraphs([gain,phase],log=True)
    sinus = Exctract32sinus(gain,phase,samplerate)
    constructNote(sinus,enveloppe)
    return


def Keep32(gainSup):
    sorted_by_second = sorted(gainSup, key=lambda tup: tup[1])
    L = len(sorted_by_second)
    return sorted_by_second[L-32:L]

def Exctract32sinus(magnitude,phase,samplerate):
    gainSup = []
    #Puisqu'on a le complexe comjuge d'un cote te de lautre, on analyse seulement la moité des amplitude
    for n in range(0,round(len(magnitude)/2)):
        if magnitude[n] >0:
            gainSup.append((n*samplerate/len(magnitude),magnitude[n],phase[n]))
    sin32 = Keep32(gainSup)

    print("Nombre de sinus : ",len(sin32), "\n (Hz,Gain,phase) : ",sin32)
    return sin32


