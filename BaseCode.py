import matplotlib.pyplot as plt

import SignalUtils as SPE


def ExctractEnvelope(data):
    magnitude, phase = SPE.ExctractTemporalEnvelope(data)
    return

