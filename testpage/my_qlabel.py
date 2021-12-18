from PyQt5 import QtWidgets, QtCore, QtGui


class MyQLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.clicked.emit()
        QtWidgets.QLabel.mousePressEvent(self, ev)
