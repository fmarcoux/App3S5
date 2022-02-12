import scipy.signal
from scipy.io import wavfile
import numpy as np

@classmethod
class SignalParameterExtractor:

    def ReadWavfile(self,fullPath):
        "read a wave file specified in fullpath and return the data(ndarray) and the sample rate(hz)"
        if ".wav" not in fullPath:
            raise Exception("Specified file is not of a wav file")
        samplerate, data = wavfile.read('./output/audio.wav')
        return samplerate, np.array(data)

    def ExctractTemporalEnvelope(self,data):
        "Exctract the temporal envelope of a discrete signal, returns the amplitude(ndarray) and the phase(ndarra)"
        envelope = scipy.signal.hilbert(data)
        return np.abs(envelope),np.unwrap(np.angle(envelope))
