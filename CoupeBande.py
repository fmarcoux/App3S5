import numpy as np
import os
from scipy.io.wavfile import write
import GraphUtils
import SignalUtils
import SignalUtils as SPE
import matplotlib.pyplot as plt


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


def graphReponseFreq(x, y, type,xlim=[0,0]):
    plt.plot(x, y)
    plt.xlabel('Fréquence (Hz)')
    plt.ylabel('Gain filtre du ' + type + ' (dB)')
    plt.title('Réponse frequence ' + type)
    if xlim!= [0,0]:
        plt.xlim(xlim)
    plt.show()


def CoupeBande():

    fe, data = SPE.ReadWavfile("note_basson_plus_sinus_1000_Hz.wav")

    echantillon = len(data)
    N = 6000
    K = int(((2 * 40 * N/fe) + 1))
    axen = np.arange(-N / 2, N / 2)
    axem = np.arange(-echantillon / 2, echantillon / 2)

    axeFrequence = axem * (fe / echantillon)
    d = defineDirac(axen)

    hinfo = reponseImpFiltrePB(N, axen, K)
    Hinfo = np.fft.fftshift(np.fft.fft(hinfo, echantillon))
    graphReponseFreq(axeFrequence, 20 * np.log10(np.abs(Hinfo)), "passe-bas",[0,100])

    # h2 = d - 2*(1 / N * (np.sin(np.pi*axen*K / N) / ( np.sin(np.pi*axen / N)))) * np.cos(axen * 1000*np.pi*2 / fe)
    h2info = tranfoPBastoCBande(hinfo, N, d)

    H2 = np.fft.fftshift(np.fft.fft(h2info, echantillon))
    graphReponseFreq(axeFrequence, 20 * np.log10(np.abs(H2)), "coupe-bande",[0,2000])

    son = SignalUtils.HanningWindow(data)
    sonclair = np.convolve(h2info, son)
    for i in range(0,3):
        sonclair = np.convolve(h2info, sonclair)
    sonclair = sonclair /max(sonclair)
    write("AudioSynthese\\sonclair.wav", fe, np.array(sonclair).astype(np.float32))
