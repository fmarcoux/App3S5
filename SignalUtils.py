import os
import scipy.signal as signal
from scipy.io import wavfile
import numpy as np

def CropForOutput(signal,long=False):
    if long:
        return signal[7600:44000]
    else :
        return signal[7600:22000]

def AddEnveloppeTemporrel(enveloppe,son):
    return (son*enveloppe) /max(enveloppe)

def CreateSound(freq,gain,phase,facteurLa,t):
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

def computeDirak(N):
    d= [1]
    [d.append(0) for i in range(0,N-1)]
    return d

def passBadVersCoupeBande(h,d,w0,Fs):
    "w0 est la frequence de passe bande en Hz"
    wo = 2*np.pi*w0/Fs
    nh=[]
    for n in range(0,len(h)-1):
        nh.append(d[n]+ 2*h[n]*np.cos(n*wo))
    return nh

def computeRIF(NombreDeCoefficient,cutoffFrequence,sampleFrequence):
    """calcul la reponse impulsionnel pour un filtre passe bas selon les parametres
    (N = nombre de coefficients du filtre passe bas)
    sampleFrequence = la frequence a laquelle le signal a ete echantillone
    cutofffrequence = la frequence de cutoff voulu
    retourne la reponse impulsionnel (ndarray)
    """
    K = int((2*cutoffFrequence*NombreDeCoefficient)/sampleFrequence)+1
    reponseImpulsionnelle =[]
    for i in range(round(-NombreDeCoefficient/2),round(NombreDeCoefficient/2)):
        if i==0 :
            reponseImpulsionnelle.append(K/NombreDeCoefficient)
        else:
            reponseImpulsionnelle.append(singlePointreponseImpulsionnelle(i,K,NombreDeCoefficient))
    return np.array(reponseImpulsionnelle)


def singlePointreponseImpulsionnelle(n,K,N):
    u = np.sin((np.pi*n*K)/N)
    d = np.sin((np.pi*n)/N)
    return ((1/N)*u/d)


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

def ComputeN():
    print(computeNForFIRFilterOfTemporalEnvelope())

def ComputeEnvelope(K,data):
    h= computeRIF(K,np.pi/1000,2*np.pi)
    return np.convolve(data,h)

def Exctract32Sinus(data):
    dataFenetre = HanningWindow(data)
    response = np.fft.fft(dataFenetre)
    responseDb = 20*np.log10(np.abs(response))
    peaks = signal.find_peaks(responseDb,distance=1600)
    peaks32 = peaks[0][0:32]
    return peaks32,np.abs(response),np.angle(response)