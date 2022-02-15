import BaseCode
import os
import matplotlib.pyplot as plt
import GraphUtils
import GraphUtils as GU
import SignalUtils
import SignalUtils as SU
import numpy as np
import scipy.io.wavfile as wav

if __name__ == '__main__':

    workingDirectory = os.getcwd()
    dir = "WaveFiles"
    fileName = "note_guitare_LAd.wav"
    fullpath = f'{workingDirectory}\\{dir}\\{fileName}'
    #BaseCode.ComputeN()
    Fs,data = SU.ReadWavfile(fullpath)

    enveloppe = BaseCode.ComputeEnvelope(886,abs(data))
    enveloppe = enveloppe[0:160000]

    N = len(data)
    print(f"{N}, {Fs}")
    indexs,gain,phase = BaseCode.Exctract32Sinus(data)
    # calcul parametres sinus
    freq_32 = []
    phase_32 = []
    mag_32 = []

    for i in range(0, 32):
        freq_32.append((indexs[i]) / (N / Fs))
        phase_32.append(phase[(indexs[i])])
        mag_32.append(gain[(indexs[i])])
    print(f"Frequence {freq_32} \n phase {phase_32} \n gain {mag_32}")

    temps = np.arange(0, N/Fs, 1/Fs)

    LADiese =SU.CropForOutput(SU.AddEnveloppeTemporrel(enveloppe,SU.CreateSound(freq_32,mag_32,phase_32,1,temps)))
    SOL = SU.CropForOutput(SU.AddEnveloppeTemporrel(enveloppe,SU.CreateSound(freq_32,mag_32,phase_32,0.841,temps)))
    MiB = SU.CropForOutput(SU.AddEnveloppeTemporrel(enveloppe,SU.CreateSound(freq_32,mag_32,phase_32,0.667,temps)))
    Silence = SU.CropForOutput(np.zeros(N))
    Fa = SU.CropForOutput(SU.AddEnveloppeTemporrel(enveloppe,SU.CreateSound(freq_32,mag_32,phase_32,0.749,temps)))
    Re = SU.CropForOutput(SU.AddEnveloppeTemporrel(enveloppe,SU.CreateSound(freq_32,mag_32,phase_32,0.630,temps)))

    bethoven = []
    bethoven.extend(SOL)
    bethoven.extend(SOL)
    bethoven.extend(SOL)
    bethoven.extend(MiB)
    bethoven.extend(Silence)
    bethoven.extend(Fa)
    bethoven.extend(Fa)
    bethoven.extend(Fa)
    bethoven.extend(Re)
    GU.ShowGraphs([bethoven])
    signalSortie = np.array(bethoven)
    wav.write("bethoven.wav",Fs,signalSortie.astype(np.float32))



