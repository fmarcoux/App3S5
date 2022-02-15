
from scipy.io import wavfile
import numpy as np

def CropForOutput(signal,long):
    return signal[7600:22000]

def AddEnveloppeTemporrel(enveloppe,son):
    return (son*enveloppe) /max(enveloppe)

def CreateSound(freq,gain,phase,facteurLa,t):
    sound = np.zeros(len(t))
    for i in range(0,32):
        sound += gain[i]* np.sin(2 * np.pi * freq[i] * facteurLa* t + phase[i])
    sound = sound / max(gain)

    return sound

def ReadWavfile(fullPath):
    "read a wave file specified in fullpath and return the sample rate(hz_ and the  data(ndarray)"
    if ".wav" not in fullPath:
        raise Exception("Specified file is not of a wav file")
    return wavfile.read(fullPath)


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

def computeRIF(N,cutoffFrequence):
    """calcul la reponse impulsionnel pour un filtre passe bas selon les parametres
    (N = nombre de coefficients du filtre passe bas)
    sampleFrequence = la frequence a laquelle le signal a ete echantillone
    cutofffrequence = la frequence de cutoff voulu
    retourne la reponse impulsionnel (ndarray)
    """
    K = int(1+ cutoffFrequence*N/np.pi)
    reponseImpulsionnelle = [K/N]
    for i in range(1,N):
        reponseImpulsionnelle.append(singlePointreponseImpulsionnelle(i,K,N))
    return np.array(reponseImpulsionnelle)

def singlePointreponseImpulsionnelle(n,K,N):
    return (np.sin(np.pi*n*K/N))/ (np.sin(np.pi*n/N))/N


def PaddZero(initialData, nombredezero):
    "Padd les data dans initialData avec le nombre de zero specifie en parametre, retourne larray de data padde"
    zeros = np.array([0 for i in range(0,nombredezero)])
    return np.hstack([initialData,zeros])


def computeNForFIRFilterOfTemporalEnvelope():
    "Calcul le nombre de paramètre de notre filtre pour avoir un gain de -3dB a pi/1000"
    K =1
    wbar = np.pi/1000
    targetGain = -3
    gain=1
    is_in_margin = lambda gain:not(targetGain-0.001 < gain<targetGain+0.001)
    while is_in_margin(gain):
        gain = (1/K)*np.sin(wbar*K/2)/np.sin(wbar/2)
        print(f"K : {K}")
        print(f"Gain : {gain}")
        K += 1

def GetCoefficient(N):
    return [(1/N) for i in range(0,N)]