from pydub import AudioSegment
import sys


AVAILABE_EXT = ["mp3", "ogg"]


def convert(file, ext):
    fileSplit = file.split(".")

    # Loop through all available extension
    for e in AVAILABE_EXT:
        if ext == e:
            # If a correct extension is found, convert the file to .wav
            snd = AudioSegment.from_file(file, format=fileSplit[-1])
            name = fileSplit[0] + ".wav"
            snd.export(name, format="wav")
        return fileSplit[0] + ".wav"

    # Raise exception if no converions could be done
    raise Exception("Format file not availabe for conversion")
