from matplotlib import pyplot as plt

import CoupeBande
import GraphUtils as GU
import SignalUtils as SU
import numpy as np
import scipy.io.wavfile as wav

if __name__ == '__main__':

    Fs, data = SU.ReadWavfile("note_guitare_LAd.wav")
    enveloppe = SU.ComputeEnvelope(886, abs(data))
    enveloppe = enveloppe[0:160000]
    GU.ShowGraphs([enveloppe,data],titles=["Enveloppe temporelle du signal de guitare","Signal de guitare"])

    N = len(data)
    axem = np.arange(-N / 2, N / 2)
    axeFrequence = axem * (Fs / N)
    print(f"{N}, {Fs}")
    indexs, gain, phase = SU.Exctract32Sinus(data)
    print(f"index :\n {indexs} \n Gain : \n {gain} \n phase : \n{phase}")

    freqs = []
    phases = []
    mags = []

    for i in range(0, 32):
        freqs.append((indexs[i]) / (N / Fs))
        phases.append(phase[(indexs[i])])
        mags.append(gain[(indexs[i])])

    temps = np.arange(0, N / Fs, 1 / Fs)

    LADiese = SU.AddEnveloppeTemporrel(enveloppe, SU.CreateSound(freqs, mags, phases, 1, temps))
    SinusoidInital = np.fft.fftshift(np.fft.fft(data))
    SinusoidSynthese = np.fft.fftshift(np.fft.fft(LADiese))

    fig,(ax0,ax2) = plt.subplots(nrows=2,ncols=1)
    ax0.plot(axeFrequence, 20*np.log10(np.abs((SinusoidInital))))
    ax0.set_xlabel('Fréquence (Hz)')
    ax0.set_ylabel('Amplitude (dB)')
    ax0.set_title('signal original')
    ax0.scatter(freqs, 20 * np.log10(mags),c="orange")

    ax2.plot(axeFrequence, 20 * np.log10(np.abs((SinusoidSynthese))))
    ax2.set_xlabel('Fréquence (Hz)')
    ax2.set_ylabel('Amplitude (dB)')
    ax2.set_title('signal reconstruit')

    plt.show()

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
    #GU.ShowGraphs([beethoven])
    wav.write("AudioSynthese\\Beethoven.wav", Fs, np.array(beethoven).astype(np.float32))

    CoupeBande.CoupeBande()
