import matplotlib.pyplot as plt
import numpy as np


def convert_to_decibel(arr,ref):
    ref = ref
    if arr != 0:
        return 20 * np.log10(abs(arr) / ref)
    else:
        return -60

def setDbScale(data,ref):
    return [convert_to_decibel(n,ref) for n in data]


def ShowGraphs(listofData,titles=[],xlim=[0,0],ylim=[0,0],type="plot",freqNormalise = False,scales=[]):
    "Show the graphs in a subplot, xlim and y lim can be specified, the default plot type is plot"
    fig,graphs = plt.subplots(nrows=len(listofData),ncols=1,squeeze=False)
    for i in range(0,len(listofData)):
        N = len(listofData[i])
        x= np.arange(0,N)
        if(freqNormalise):
            x = [m * 2*np.pi/N for m in x]
        if type=="plot":
            graphs[i,0].plot(x,listofData[i])
        elif type == "stem":
            graphs[i,0].stem(x,listofData[i])
        if xlim != [0, 0]:
            graphs[i,0].set_xlim(xlim)
        elif ylim != [0, 0]:
            graphs[i,0].set_ylim(ylim)
        if len(titles) > i:
            graphs[i,0].title.set_text(titles[i])

    plt.show()

