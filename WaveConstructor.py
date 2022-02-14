import wave
import numpy as np

def Construct(FileName,data):

    samplerate = 44100

    # Put the channels together with shape (2, 44100).
    data = np.array([data, data]).T

    # Convert to (little-endian) 16 bit integers.
    data = (data * (2 ** 15 - 1)).astype("<h")

    with wave.open(FileName, "w") as f:
        # 2 Channels.
        f.setnchannels(2)
        # 2 bytes per sample.
        f.setsampwidth(2)
        f.setframerate(samplerate)
        f.writeframes(data.tobytes())