#!/usr/bin/env python

import argparse
import aubio
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment, playback
#from pyqtgraph.Qt import QtGui, QtCore
#import pyqtgraph as pg
import threading
import time

import converter


currentTime = lambda: int(round(time.time() * 1000))


def plotter(tabX, tabY, line):
    if line == []:
        plt.ion()
        fig = plt.figure(figsize=(13, 6), num=0)
        ax = fig.add_subplot(111)
        line, = ax.plot(tabX, tabY, '-o', alpha=0.8)
        plt.show()

    line.set_ydata(tabY)

    if np.min(tabY) <= line.axes.get_ylim()[0] or np.max(tabY) >= line.axes.get_ylim()[1]:
        plt.ylim([np.min(tabY) - np.std(tabY),np.max(tabY) + np.std(tabY)])

    plt.pause(0.005)
    return line


def play(file):
    time.sleep(0.1)
    song = AudioSegment.from_wav(file)
    playback.play(song)


def argumentParsing():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="name of the file you want to analyze")
    parser.add_argument("-m", action="store_const", dest="m", const=True, default=False, help="display data with matplotlib")
    parser.add_argument("-qt", action="store_const", dest="qt", const=True, default=False, help="display data with pyqtgraph")
    parser.add_argument("-p", action="store_const", dest="p", const=False, default=True,  help="don't play sound when showing data")
    return parser.parse_args()


def audioProcess(file):
    # Open audio file to get samplerate and duration of the track then close it
    s = aubio.source(file)
    samplerate = s.samplerate
    duration = s.duration
    s.close()

    # Compute length of track in seconds, divide the total nubmer of samples by sumber of sample
    # for one second
    print(s.duration, samplerate, duration / samplerate)

    # I want to update the plot 20 times per second, so hopSize is the number of sample aubio should send me
    hopSize = samplerate // 20

    # Reopen the file with a new hopSize according to its samplerate
    s = aubio.source(file, hop_size=hopSize)

    pitchOutput = aubio.pitch("default", 4096, hopSize, s.samplerate)
    pitchOutput.set_unit("midi")
    pitchOutput.set_tolerance(0.8)

    return hopSize, s


def main():
    # Argument parsing
    args = argumentParsing()
    #print(args)

    ext = args.file.split(".")[-1]
    if ext is not "wav":
        file = converter.convert(args.file, ext)

    hopSize, s = audioProcess(file)

    if args.m is True:
        plt.style.use("ggplot")
    """
    else:
        app = QtGui.QGuiApplication([])
        win = pg.GraphicsLayoutWidget(show = True, title="Audio feature extractor")
        win.resize(1000, 600)

        pg.setConfigOptions(antialias=True)

        plot = win.addPlot(title="Pitch")
        curve = plot.plot()
        data = np.random.normal(size=(10,1000))
        ptr = 0
        def update():
            global ptr
            curve.setData(data[ptr % 10])
            if ptr == 0:
                plot.enableAutoRange('xy', False)
            ptr += 1
        timer = QtCore.QTimer()
        timer.timeout.connect(update)
        timer.start(50)

        QtGui.QApplication.instance().exec_()
    """

    tabX = np.linspace(0, 1, hopSize + 1)[0:-1]
    line = []

    # Play music of another thread because pydub is blocking, another method is probably better
    # but this is what I got
    if args.p is True:
        t = threading.Thread(target=lambda: play(file))
        t.start()

    while True:
        # Get new samples from file
        samples, read = s()

        # Compute time it takes to plot one frame with matplotlib
        startTime = currentTime()
        line = plotter(tabX, samples, line)
        endTime = currentTime()

        # Sleep for a small amount of time to keep the program synchronized because
        #   each frame render 50ms of sample
        diff = endTime - startTime
        sleepTime = (50 - diff) / 1000

        #print("'", sleepTime, "'")
        time.sleep(sleepTime if sleepTime > 0 else 0)

        if read < hopSize or plt.fignum_exists(0) is False:
            break


if __name__ == "__main__":
    main()
