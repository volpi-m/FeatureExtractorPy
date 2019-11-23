from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np


class QtPlotter:

    def __init__(self, sound, hopSize):
        self.sound = sound
        self.hopSize = hopSize

        QtGui.QApplication([])

        self.win = pg.GraphicsWindow(title="Audio feature extractor")
        self.win.resize(1000, 600)

        pg.setConfigOptions(antialias=True)

        self.plot = self.win.addPlot(title="Pitch")
        self.curve = self.plot.plot(pen='y')
        self.plot.setYRange(-2, 2)
        self.data = np.random.normal(size=(10, 100))

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.__update)
        self.timer.start(50)

        pg.QtGui.QApplication.instance().exec_()


    def __update(self):
        samples, read = self.sound()

        self.curve.setData(samples)

        if read < self.hopSize:
            self.timer.stop()
            self.win.close()

