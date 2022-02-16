import matplotlib.pyplot as plt
import numpy as np
"Fonctions pour afficher des graphiques"

def graphReponseFreq(x, y, type,xlim=[0,0]):
    plt.plot(x, y)
    plt.xlabel('Fréquence (Hz)')
    plt.ylabel('Gain filtre du ' + type + ' (dB)')
    plt.title('Réponse frequence ' + type)
    if xlim!= [0,0]:
        plt.xlim(xlim)
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

