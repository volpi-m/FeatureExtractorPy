from pydub import AudioSegment
import sys


class Converter:

    def __init__(self, file):
        # Setup available conversion format, complete file name, name without extension
        #   and with extension
        self.AVAILABE_EXTENSION = ["mp3", "ogg"]
        self.file = file
        self.name = file[:file.rfind(".")]
        self.ext = self.file.split(".")[-1]

        # Check if the current file type is a supported
        #   otherwise raise exception if no converions could be done
        if self.ext not in self.AVAILABE_EXTENSION:
            raise Exception("Format file not availabe for conversion")

    def convert(self, ext):
        """
        Convert the file to the specified format
        """

        snd = AudioSegment.from_file(self.file, format=self.ext)
        newName = self.name + ext
        snd.export(newName, format=ext)
        return self.name + ext
