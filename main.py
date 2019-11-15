#!/usr/bin/env python

import argparse
import aubio

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("file", help="Name of the file you want to analyze")
    args = parse.parse_args()

    s = aubio.source(args.file)
    samplerate = s.samplerate
    hopSize = s.hop_size
    winSize = 4096

    print(samplerate, hopSize, winSize)

    tolerance = 0.8
    pitches = []

    pitchOutput = aubio.pitch("yin", winSize, hopSize, samplerate)
    pitchOutput.set_unit("midi")
    pitchOutput.set_tolerance(tolerance)

    totalFrame = 0
    while True:
        samples, read = s()
        pitch = pitchOutput(samples)[0]
        print("{:f} {:f}".format(totalFrame / float(samplerate), pitch))
        pitches.append(pitch)
        totalFrame += read
        if read < hopSize:
            break

if __name__ == "__main__":
    main()
