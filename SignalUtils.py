import os
import scipy.signal as signal
from scipy.io import wavfile
import numpy as np


def CropForOutput(signal,long=False):
    "Crop un vecteur pour qu'il soit d'une longeur raisonnable à l'écoute"
    if long:
        return signal[7600:44000]
    else :
        return signal[7600:22000]

def AddEnveloppeTemporrel(enveloppe,son):
    return (son*enveloppe) /max(enveloppe)

def CreateSound(freq,gain,phase,facteurLa,t):
    "Crée un son en additionnant les sinus généré par les paramètres freq, gain et phase ainsi que le facteur La# "
    sound = np.zeros(len(t))
    for i in range(0,32):
        sound += gain[i]* np.sin(2 * np.pi * freq[i] * facteurLa* t + phase[i])
    sound = sound / max(gain)
    return sound

def ReadWavfile(fileName):
    "read a wave file specified in fullpath and return the sample rate(hz_ and the  data(ndarray)"
    workingDirectory = os.getcwd()
    dir = "WaveFiles"
    fullpath = f'{workingDirectory}\\{dir}\\{fileName}'
    if ".wav" not in fullpath:
        raise Exception("Specified file is not of a wav file")
    return wavfile.read(fullpath)


def HanningWindow(array):
    "Ajoute une window de type Hanning au signal en entre, retourne le signal transforme (ndarray)"
    hanning = np.hanning(len(array))
    for i in range(0,len(array)):
        array[i] = array[i]*hanning[i]
    return array


def PaddZero(initialData, nombredezero):
    "Padd les data dans initialData avec le nombre de zero specifie en parametre, retourne larray de data padde"
    return np.hstack([initialData,np.zeros(nombredezero)])


def computeNForFIRFilterOfTemporalEnvelope():
    "Calcul le nombre de paramètre de notre filtre pour avoir un gain de -3dB a pi/1000"
    K =1
    wbar = np.pi/1000
    targetGain = 0.707106 #-3dB
    gain=1
    is_in_margin = lambda gain:not(targetGain-0.0001 < gain<targetGain+0.0001)
    while is_in_margin(gain):
        gain = (1/K)*np.sin(wbar*K/2)/np.sin(wbar/2)
        print(f"K : {K}")
        print(f"Gain : {gain}")
        K += 1
    print(K)


def ComputeEnvelope(K,data):
    "Clacul le signal d'enveloppe temporelle"
    h= np.ones(K)*(1/K)
    return np.convolve(h,data)

def Exctract32Sinus(data):
    "Extrait les 32 sinus principales du signal d'entré"
    dataFenetre = HanningWindow(data)
    response = np.fft.fft(dataFenetre)
    peaks = signal.find_peaks(response,distance=1600)
    peaks32 = peaks[0][0:32]
    return peaks32,np.abs(response),np.angle(response)


def reponseImpFiltrePB(N, n, K):
    h = []
    # h = (1 / N) * (np.sin(np.pi * axen * K / N) / ( np.sin(np.pi * axen / N)))
    for i in range(0, len(n)):
        if n[i] == 0:
            h.append(K / N)
        else:
            h.append(np.sin(n[i] * np.pi * K / N) / (N * np.sin(np.pi * n[i] / N)))
    return h


def tranfoPBastoCBande(hpb, N, d):
    hcb = []
    for i in range(0, N):
        hcb.append(d[i] - (2 * hpb[i] * np.cos(0.14248 * i)))
    return hcb


def defineDirac(n):
    d = np.zeros(len(n))
    for i in range(0, len(n) - 1):
        if n[i] == 0:
            d[i] = 1
    return d


