import matplotlib.pyplot as plt
import numpy as np


def convert_to_decibel(arr,ref):
    ref = ref
    if arr != 0:
        return 20 * np.log10(abs(arr) / ref)

def setDbScale(data,ref):
    return [convert_to_decibel(n,ref) for n in data]



def ShowOnSameGraph(listofData,titles=[],xlim=[0,0],ylim=[0,0],freqNormalise = False,Hz =False):
    for i in range(0,len(listofData)):
        N = len(listofData[i])
        x= np.arange(0,N)
        if(freqNormalise):
            x = [m * 2*np.pi/N for m in x]
        if(Hz):
            x = [(m*44100)/N for m in x]
        plt.plot(x,listofData[i])
        if xlim != [0, 0]:
            plt.xlim(xlim)
        elif ylim != [0, 0]:
            plt.ylim(ylim)
    if len(titles) > 0:
        plt.title.set_text(titles[0])
    plt.show()

def ShowGraphs(listofData,titles=[],xlim=[0,0],ylim=[0,0],type="plot",freqNormalise = False,log=False,Hz=False):
    "Show the graphs in a subplot, xlim and y lim can be specified, the default plot type is plot, the FreqNormalise parameter modify the x axis to show the graph from 0 to 2pi"
    fig,graphs = plt.subplots(nrows=len(listofData),ncols=1,squeeze=False)
    for i in range(0,len(listofData)):
        N = len(listofData[i])
        x= np.arange(0,N)
        if(freqNormalise==True and Hz==False):
            x = [m * 2 * np.pi/ N for m in x]
        elif(freqNormalise==False and Hz==True):
            x = [ round(m*44100/N) for m in x]
        if type=="plot":
            graphs[i,0].plot(x,listofData[i])
        elif type == "stem":
            graphs[i,0].stem(x,listofData[i])
        if xlim != [0, 0]:
            graphs[i,0].set_xlim(xlim)
        elif ylim != [0, 0]:
            graphs[i,0].set_ylim(ylim)
        if log:
            graphs[i, 0].set_yscale("log")
        if len(titles) > i:
            graphs[i,0].title.set_text(titles[i])

    plt.show()

