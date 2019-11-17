#!/usr/bin/env python

import argparse
import aubio
import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment, playback
import threading
import time


currentTime = lambda: int(round(time.time() * 1000))


def plotter(tabX, tabY, line):
    if line == []:
        plt.ion()
        fig = plt.figure(figsize=(13, 6))
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


def main():
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="name of the file you want to analyze")
    parser.add_argument("-m", action="store_const", dest="m", const=True, help="display data with matplotlib")
    parser.add_argument("-p", action="store_const", dest="p", const=False, default=True,  help="don't play sound when showing data")
    args = parser.parse_args()
    #print(args)

    # Open audio file to get samplerate and duration of the track then close it
    s = aubio.source(args.file)
    samplerate = s.samplerate
    duration = s.duration
    s.close()

    # Compute length of track in seconds, divide the total nubmer of samples by sumber of sample
    # for one second
    print(s.duration, samplerate, duration / samplerate)

    # I want to update the plot 20 times per second, so hopSize is the number of sample aubio should send me
    hopSize = samplerate // 20

    # Reopen the file with a new hopSize according to its samplerate
    s = aubio.source(args.file, hop_size=hopSize)

    pitchOutput = aubio.pitch("default", 4096, hopSize, s.samplerate)
    pitchOutput.set_unit("midi")
    #pitchOutput.set_tolerance(0.8)

    plt.style.use("ggplot")

    tabX = np.linspace(0, 1, hopSize + 1)[0:-1]
    line = []

    # Play music of another thread because pydub is blocking, another method is probably better
    # but this is what I got
    if args.p is True:
        threading.Thread(target=lambda: play(args.file)).start()

    while True:
        samples, read = s()

        startTime = currentTime()
        line = plotter(tabX, samples, line)
        endTime = currentTime()

        diff = endTime - startTime
        sleepTime = (50 - diff) / 1000

        #print("'", sleepTime, "'")
        time.sleep(sleepTime if sleepTime > 0 else 0)

        if read < hopSize:
            break


if __name__ == "__main__":
    main()
