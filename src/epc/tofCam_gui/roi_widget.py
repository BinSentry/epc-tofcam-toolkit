from PyQt5 import QtWidgets  
from PyQt5.QtWidgets import QSpinBox, QLabel

class ROIWidget(QtWidgets.QWidget):
    def __init__(self, server):
        super(ROIWidget, self).__init__()
        self.server = server
        self.initROI()

    def initROI(self):

        self.xMin = 0
        self.yMin = 0
        self.xMax = 319
        self.yMax = 239
        self.x1Input = QSpinBox(self)
        self.y1Input = QSpinBox(self)
        self.x2Input = QSpinBox(self)
        self.y2Input = QSpinBox(self)

        self.x1Input.setMinimum(self.xMin)
        self.x1Input.setMaximum(self.xMax)
        self.y1Input.setMinimum(self.yMin)
        self.y1Input.setMaximum(119)
        self.x2Input.setMinimum(self.xMin)
        self.x2Input.setMaximum(self.xMax)
        self.y2Input.setMinimum(120)
        self.y2Input.setMaximum(self.yMax)

        # default values
        self.x1Input.setValue(self.xMin)
        self.y1Input.setValue(self.yMin)
        self.x2Input.setValue(self.xMax)
        self.y2Input.setValue(self.yMax)

        # add labels
        self.x1Label = QLabel('X1:', self)
        self.y1Label = QLabel('Y1:', self)
        self.x2Label = QLabel('X2:', self)
        self.y2Label = QLabel('Y2:', self)

        # group box for roi
        self.roiGroupBox = QtWidgets.QGroupBox('ROI')
        roiLayout = QtWidgets.QVBoxLayout()
        positionLayout = QtWidgets.QGridLayout()
        positionLayout.addWidget(self.x1Label, 0, 0)
        positionLayout.addWidget(self.x1Input, 0, 1)
        positionLayout.addWidget(self.y1Label, 0, 2)
        positionLayout.addWidget(self.y1Input, 0, 3)
        positionLayout.addWidget(self.x2Label, 1, 0)
        positionLayout.addWidget(self.x2Input, 1, 1)
        positionLayout.addWidget(self.y2Label, 1, 2)
        positionLayout.addWidget(self.y2Input, 1, 3)
        roiLayout.addLayout(positionLayout)
        self.roiGroupBox.setLayout(roiLayout)   

        # layout
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.roiGroupBox, 7, 0)
        self.setLayout(layout)

        # signals for input changes
        self.x1Input.valueChanged.connect(self.updateX1)
        self.x2Input.valueChanged.connect(self.updateX2)
        self.y1Input.valueChanged.connect(self.updateY2)
        self.y2Input.valueChanged.connect(self.updateY1)


    # limit x ROI changes
    def updateX1(self):

        newX1Value = int(self.x1Input.text())
        x2Value = self.x2Input.value()
        if x2Value - newX1Value < 2:
            self.x1Input.setValue(newX1Value - 2)
        else:
            self.x1Input.setValue(newX1Value)
        self.applyROI()
    
    def updateX2(self):

        newX2Value = int(self.x2Input.text())
        x1Value = self.x1Input.value()
        if newX2Value - x1Value < 2:
            self.x2Input.setValue(x1Value + 2)
        else:
            self.x2Input.setValue(newX2Value)
        self.applyROI()

    # being ROI symmetric on y axis
    def updateY1(self):
        try:
            self.y1Input.blockSignals(True)
            self.y2Input.blockSignals(True)
            y2 = int(self.y2Input.text())
            y1 = self.yMax - y2  
            self.y1Input.setValue(y1)  
            self.applyROI()   
        except ValueError:
            pass  
        finally:
            self.y1Input.blockSignals(False)
            self.y2Input.blockSignals(False)

    # being ROI symmetric on y axis
    def updateY2(self):
        try:
            self.y1Input.blockSignals(True)
            self.y2Input.blockSignals(True)
            y1 = int(self.y1Input.text())
            y2 = self.yMax - y1  
            self.y2Input.setValue(y2)
            self.applyROI()
        except ValueError:
            pass  
        finally:
            self.y1Input.blockSignals(False)
            self.y2Input.blockSignals(False)
            
    def applyROI(self):
        x0 = int(self.x1Input.text())
        y0 = int(self.y1Input.text())
        x1 = int(self.x2Input.text())
        y1 = int(self.y2Input.text())
        self.server.setRoi(x0,y0,x1,y1)