import BaseCode
import os


if __name__ == '__main__':
    workingDirectory = os.getcwd()
    dir = "WaveFiles"
    fileName = "note_guitare_LAd.wav"
    fullpath = f'{workingDirectory}\\{dir}\\{fileName}'
    BaseCode.ExctractParameters(fullpath)


