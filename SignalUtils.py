import matplotlib.pyplot as plt
import scipy.signal
from scipy.io import wavfile
import numpy as np

import GraphUtils


def ReadWavfile(fullPath):
    "read a wave file specified in fullpath and return the data(ndarray) and the sample rate(hz)"
    if ".wav" not in fullPath:
        raise Exception("Specified file is not of a wav file")
    return wavfile.read(fullPath)

def ExctractTemporalEnvelope(data):
    "Exctract the temporal envelope of a discrete signal, returns the amplitude(ndarray) and the phase(ndarray)"
    #redressage du signal
    signalRedresse = abs(data)
    plt.plot(signalRedresse)
    plt.show()
    return

def FFT(data):
    "Compute the fft of the given signal and returns the magnitude and phase"
    ffts = np.fft.fft(data)
    return np.abs(ffts),np.angle(ffts)


def HanningWindow(array):
    "Ajoute une window de type Hanning au signal en entre, retourne le signal transforme (ndarray)"
    hanning = np.hanning(len(array))

    for i in range(0,len(array)):
        array[i] = array[i]*hanning[i]
    return array



def computeRIF(N,sampleFrequence,cutoffFrequence):
    """calcul la reponse impulsionnel pour un filtre passe bas selon les parametres
    (N = nombre de batonnet dans la reponse en frequence)
    sampleFrequence = la frequence a laquelle le signal a ete echantillone
    cutofffrequence = la frequence de cutoff voulu
    retourne la reponse impulsionnel (ndarray)
    """
    K = cutoffFrequence*N/sampleFrequence +1
    reponseImpulsionnelle = [K/N]
    for i in range(1,N):
        reponseImpulsionnelle.append(singlePointreponseImpulsionnelle(i,K,N))
    return np.array(reponseImpulsionnelle)

def singlePointreponseImpulsionnelle(n,K,N):
    return (np.sin(np.pi*n*K/N)/np.sin(np.pi*n/N))/N


def PaddZero(coefficients, nombredezero):
    zeros = np.array([0 for i in range(0,nombredezero)])
    return np.hstack([coefficients,zeros])


def computeNForFIRFilterOfTemporalEnvelope(nbCoefficientInitial,numberOfZeros):
    "Calcul le nombre de paramètre de notre filtre pour avoir un gain de -3dB a pi/1000"
    gain =0.00
    nbcoefficient =nbCoefficientInitial
    while( gain !=-3):
        coefficient = [(1/nbcoefficient) for i in range(0,nbcoefficient)]
        coefficient = PaddZero(coefficient,numberOfZeros)
        magnitude,phase =FFT(coefficient)
        magnitude = GraphUtils.setDbScale(magnitude,magnitude[0])
        indexpisur1000 = round(len(magnitude)/(2*1000))
        gain = magnitude[indexpisur1000]
        print("nombre de coefficients : ",nbcoefficient,"\nindexpisur1000",indexpisur1000,"valeur en Db a pi sur 1000", gain)

        if(gain<-3.0001):
            break
        nbcoefficient = nbcoefficient + 1
    return nbcoefficient,magnitude,phase
