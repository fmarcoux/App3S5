
import GraphUtils as GU
import SignalUtils as SU
import numpy as np
import scipy.io.wavfile as wav

if __name__ == '__main__':

    Fs, data = SU.ReadWavfile("note_guitare_LAd.wav")
    N = len(data)

    enveloppe = SU.ComputeEnvelope(886, abs(data))
    enveloppe = enveloppe[0:160000]
    indexs, gain, phase = SU.Exctract32Sinus(data)

    freqs = []
    phases = []
    mags = []

    for i in range(0, 32):
        freqs.append((indexs[i]) / (N / Fs))
        phases.append(phase[(indexs[i])])
        mags.append(gain[(indexs[i])])

    temps = np.arange(0, N / Fs, 1 / Fs)

    LADiese = SU.AddEnveloppeTemporrel(enveloppe, SU.CreateSound(freqs, mags, phases, 1, temps))
    SOL = SU.AddEnveloppeTemporrel(enveloppe, SU.CreateSound(freqs, mags, phases, 0.841, temps))
    MiB = SU.AddEnveloppeTemporrel(enveloppe, SU.CreateSound(freqs, mags, phases, 0.667, temps))
    Silence = np.zeros(N)
    Fa = SU.AddEnveloppeTemporrel(enveloppe, SU.CreateSound(freqs, mags, phases, 0.749, temps))
    Re = SU.AddEnveloppeTemporrel(enveloppe, SU.CreateSound(freqs, mags, phases, 0.630, temps))

    wav.write("AudioSynthese\\LADiese.wav", Fs, LADiese.astype(np.float32))
    wav.write("AudioSynthese\\SOL.wav", Fs, SOL.astype(np.float32))
    wav.write("AudioSynthese\\MiBemol.wav", Fs, MiB.astype(np.float32))
    wav.write("AudioSynthese\\FA.wav", Fs, Fa.astype(np.float32))
    wav.write("AudioSynthese\\Re.wav", Fs, Re.astype(np.float32))

    beethoven = []
    beethoven.extend(SU.CropForOutput(SOL))
    beethoven.extend(SU.CropForOutput(SOL))
    beethoven.extend(SU.CropForOutput(SOL))
    beethoven.extend(SU.CropForOutput(MiB,True))
    beethoven.extend(SU.CropForOutput(Silence,True))
    beethoven.extend(SU.CropForOutput(Fa))
    beethoven.extend(SU.CropForOutput(Fa))
    beethoven.extend(SU.CropForOutput(Fa))
    beethoven.extend(SU.CropForOutput(Re))
    wav.write("AudioSynthese\\Beethoven.wav", Fs, np.array(beethoven).astype(np.float32))

    fe, data = SU.ReadWavfile("note_basson_plus_sinus_1000_Hz.wav")
    echantillon = len(data)
    N = 6000
    K = int(((2 * 40 * N / fe) + 1))
    axen = np.arange(-N / 2, N / 2)
    axem = np.arange(-echantillon / 2, echantillon / 2)

    axeFrequence = axem * (fe / echantillon)
    d = SU.defineDirac(axen)

    hinfo = SU.reponseImpFiltrePB(N, axen, K)
    Hinfo = np.fft.fftshift(np.fft.fft(hinfo, echantillon))

    # h2 = d - 2*(1 / N * (np.sin(np.pi*axen*K / N) / ( np.sin(np.pi*axen / N)))) * np.cos(axen * 1000*np.pi*2 / fe)
    h2info = SU.tranfoPBastoCBande(hinfo, N, d)

    H2 = np.fft.fftshift(np.fft.fft(h2info, echantillon))

    son = SU.HanningWindow(data)
    sonclair = np.convolve(h2info, son)
    for i in range(0, 3):
        sonclair = np.convolve(h2info, sonclair)
    sonclair = sonclair / max(sonclair)

    wav.write("AudioSynthese\\sonclair.wav", fe, np.array(sonclair).astype(np.float32))
