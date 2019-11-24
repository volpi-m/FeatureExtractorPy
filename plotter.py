from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np


class QtPlotter:

    def __init__(self, sound, hopSize):
        self.sound = sound
        self.hopSize = hopSize

        QtGui.QApplication([])

        # Setup window
        self.win = pg.GraphicsWindow(title="Audio feature extractor")
        self.win.resize(1000, 600)
        pg.setConfigOptions(antialias=True)

        # Setup plot and add a new curve
        self.plot = self.win.addPlot(title="Pitch")
        self.curve = self.plot.plot(pen='y')
        self.plot.setYRange(-1, 1)
        self.data = np.random.normal(size=(10, 100))

        # Setup timer, call __update every 50ms to plot new samples
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.__update)
        self.timer.start(50)

        # Run Qt window
        pg.QtGui.QApplication.instance().exec_()


    def __update(self):
        samples, read = self.sound()

        self.curve.setData(samples)

        if read < self.hopSize:
            self.timer.stop()
            self.win.close()

