#!/usr/bin/env python

import argparse
import aubio
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
from pydub import playback
import threading
from time import sleep, time
import pylab

def plotter(tabX, tabY, line):
    if line == []:
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        line, = ax.plot(tabX, tabY, '-o', alpha=0.8)
        plt.show()

    line.set_ydata(tabY)

    if np.min(tabY) <= line.axes.get_ylim()[0] or np.max(tabY) >= line.axes.get_ylim()[1]:
        plt.ylim([np.min(tabY) - np.std(tabY),np.max(tabY) + np.std(tabY)])

    plt.pause(0.01)
    return line

def webplotter():
    """pylab.plot(samples)
    pylab.grid()
    pylab.axis([0, len(samples), -0.5, 0.5])
    pylab.savefig("img.png", dpi=50)
    pylab.close('all')"""
    pass

def play(file):
    song = AudioSegment.from_wav(file)
    playback.play(song)

def main():
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="name of the file you want to analyze")
    parser.add_argument("-m", action="store_const", dest="m", const=True, help="display data with matplotlib")
    parser.add_argument("-p", action="store_const", dest="p", const=False, default=True,  help="don't play sound when showing data")
    args = parser.parse_args()
    #print(args)

    # open audio file to analyze
    s = aubio.source(args.file, hop_size = 1024)
    samplerate = s.samplerate
    hopSize = s.hop_size
    winSize = 4096

    # length of track in seconds, divide the nubmer of samples by sumber of sample for one second
    sourceLength = s.duration / s.samplerate
    #print(s.duration, s.samplerate, s.duration / s.samplerate)

    tolerance = 0.8

    pitchOutput = aubio.pitch("yin", winSize, hopSize, samplerate)
    pitchOutput.set_unit("midi")
    pitchOutput.set_tolerance(tolerance)

    plt.style.use("ggplot")

    tabX = np.linspace(0, 1, 1025)[0:-1]
    line = []

    if args.p is True:
        threading.Thread(target=lambda: play(args.file)).start()

    while True:
        samples, read = s()
        """n = []
        for i in range(0, 1024, 2):
            n.append(samples[i])"""
        #print(len(tabX), len(samples), samplerate)
        line = plotter(tabX, samples, line)
        if read < hopSize:
            break

if __name__ == "__main__":
    main()
