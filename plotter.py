from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np


class QtPlotter:

    def __init__(self):
        app = QtGui.QApplication([])

        self.win = pg.GraphicsWindow(title="Audio feature extractor")
        self.win.resize(1000, 600)

        pg.setConfigOptions(antialias=True)

        self.plot = self.win.addPlot(title="Pitch")
        self.curve = self.plot.plot(pen='y')
        self.data = np.random.normal(size=(10, 100))

        self.ptr = 0

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.__update)
        self.timer.start(50)

        pg.QtGui.QApplication.instance().exec_()


    def __update(self):
        self.curve.setData(self.data[self.ptr % 10])
        if self.ptr == 0:
            self.plot.enableAutoRange('xy', False)
        self.ptr += 1
        if self.ptr > 20:
            self.timer.stop()


class MplPlotter:

    def __init__(self):
        pass

p = QtPlotter()
