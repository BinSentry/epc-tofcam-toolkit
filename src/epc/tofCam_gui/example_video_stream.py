import sys

sys.path.append('.')

import numpy as np
import cv2

from PyQt5 import QtWidgets  
import pyqtgraph as pg
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QPushButton, QComboBox
from .roi_widget import ROIWidget
from .settings_widget import SettingsWidget

from epc.tofCam660.productfactory import ProductFactory
from epc.tofCam660.server import Server

from .transformations import *


#ESTABLISH CONNECTION
server = Server()
server.setProduct(ProductFactory().create_product('660_ethernet', 0)) #'660_ethernet' for ethernet, '660_usb' for usb connection
server.startup()

#CAMERA SETTINGS
server.setMinAmplitude(0)
server.disableFilter()
server.setModulationFrequencyMHz(24)
server.disableBinning()
server.disableHdr()
server.setIntTimesus(50000,100)
server.setMinAmplitude(10)
server.setRoi(0,0,320,240)

#GET INITIAL IMAGES
dist= server.getTofDistance()[0]
gray=np.rot90(server.getGrayscaleAmplitude()[0],1,(1,0))
amp = server.getTofAmplitude()[0]

def main():
    #OPEN THE QTGUI DEFINED BELOW
    app = QtWidgets.QApplication(sys.argv)
    stream = Stream()
    stream.show()
    sys.exit(app.exec_())


class Stream(QtWidgets.QWidget):
    def __init__(self):

        super(Stream, self).__init__()
        self.initUI()

    def initUI(self):
        self.mode='default'
        #GENERAL
        self.sg1_image=pg.ImageView()
        self.sg1_image.setImage(gray)
        #GENERAL COLORMAPS
        colors = [  (  0,   0,   0),
                     (255,   0,   0),
                     (255, 255,   0),
                     (  0, 255,   0),
                     (  0, 240, 240),
                     (  0,   0, 255),
                     (255,   0, 255) ]

        default=  [
            (0, 0, 0),
            (51, 51, 51),
            (102, 102, 102),
            (153, 153, 153),
            (204, 204, 204),
            (255, 255, 255)
        ]

        self.defaultmap=pg.ColorMap(pos=np.linspace(0.0, 1.0, 6), color=default)
        self.cmap = pg.ColorMap(pos=np.linspace(0.0, 1.0, 6), color=colors)
        self.endbtn=QPushButton('Stop')
        self.endbtn.clicked.connect(self.endTimer)

        #GREYSCALE
        self.timerGrsc=QTimer()
        self.timerGrsc.timeout.connect(self.updateGrsc)

        #DISTANCE
        self.timerdistance=QTimer()
        self.timerdistance.timeout.connect(self.updateDistance)

        #AMPLITUDE
        self.timeramp=QTimer()
        self.timeramp.timeout.connect(self.updateAmp)

        #SETTINGS
        self.settingsWidget = SettingsWidget(server)

        #ROI
        self.roiWidget = ROIWidget(server)

        # Image data modes
        self.imageType = QComboBox(self)
        self.imageType.addItem("Distance")
        self.imageType.addItem("Amplitude")
        self.imageType.addItem("Grayscale")
        self.imageType.setCurrentIndex(2)
        self.imageType.currentIndexChanged.connect(self.imageTypeChanged)

        # group box for image data
        self.imageTypeGroupBox = QtWidgets.QGroupBox('Image Type')
        imageTypeLayout = QtWidgets.QVBoxLayout()
        imageTypeLayout.addWidget(self.imageType)
        self.imageTypeGroupBox.setLayout(imageTypeLayout)   

        # Python image filters
        self.guiFilters = QComboBox(self)
        self.guiFilters.addItem("None")
        self.guiFilters.addItem("Gradient Image")
        self.guiFilters.addItem("Thresholded Image")
        self.guiFilters.addItem("Edge Detector")
        self.guiFilters.setCurrentIndex(0)
        self.guiFilters.currentIndexChanged.connect(self.guiFilterChanged)

        # group box for filters
        self.guiFilterGroupBox = QtWidgets.QGroupBox('GUI Filters')
        filterLayout = QtWidgets.QVBoxLayout()
        positionLayout = QtWidgets.QGridLayout()
        positionLayout.addWidget(self.guiFilters, 0, 0)
        filterLayout.addLayout(positionLayout)
        self.guiFilterGroupBox.setLayout(filterLayout)   

        #GENERAL
        gridStarts=QtWidgets.QGridLayout()
        gridStarts.addWidget(self.imageTypeGroupBox,1,0)
        gridStarts.addWidget(self.guiFilterGroupBox,2,0)
        gridStarts.addWidget(self.endbtn,3,0)
        gridStarts.addWidget(self.settingsWidget,4,0)
        gridStarts.addWidget(self.roiWidget,5,0)

        grid=QtWidgets.QGridLayout()
        grid.setSpacing(10)
        grid.addLayout(gridStarts,0,0)

        grid.addWidget(self.sg1_image,0,1)

        grid.setColumnStretch(1,3)

        self.setLayout(grid)

        chipID = server.getChipId()
        waferID = server.getWaferId()
        fwVersion = server.getFirmwareVersion() 
        self.setWindowTitle('TOF CAM 660 VIDEO STREAM                                 CHIP ID:{}     WAFER ID:{}      FW VERSION:{}.{}'
                            .format(chipID, waferID, fwVersion['major'], fwVersion['minor']))
        self.resize(1200,600)

        #FRAMCOUNTERS FOR EACH MODE
        #COULD BE USED E.G. TO CALCULATE FRAMERATE
        self.i=0 #GREYSCALE
        self.j=0 #DISTANCE
        self.k=0 #AMPLITUDE

    #ALL BUTTONS
    def startTimerGrsc(self):
        self.endTimer()
        self.sg1_image.setColorMap(self.defaultmap)
        self.timerGrsc.start(20)            #MIN TIME BETWEEN FRAMES
        self.endbtn.setEnabled(True)

    def startTimerDistance(self):
        self.endTimer()
        self.sg1_image.setColorMap(self.cmap)
        self.timerdistance.start(50)         #MIN TIME BETWEEN FRAMES
        self.endbtn.setEnabled(True)

    def startTimerAmplitude(self):
        self.endTimer()
        self.sg1_image.setColorMap(self.cmap)
        self.timeramp.start(50)                #MIN TIME BETWEEN FRAMES
        self.endbtn.setEnabled(True)

    def endTimer(self):
        self.timerdistance.stop()
        self.timerGrsc.stop()
        self.timeramp.stop()
        self.endbtn.setEnabled(True)

     #UPDATE DISPLAYED IMAGE DEPENDING ON THE CHOSEN MODE
    def updateGrsc(self):
        self.i+=1
        img=np.rot90(server.getGrayscaleAmplitude()[0],1,(1,0))
        img = img / img.max()
        img=255*img
        img=img.astype(np.uint8)
        if(self.mode!='default'):
            if(self.mode=='grad'):
                img=transformations.gradimg(img)
            if(self.mode=='thresh'):
                img=transformations.threshgrad(img)
            if(self.mode=='canny'):
                img=cv2.Canny(img,100,50)

        self.sg1_image.setImage(img)

    def updateDistance(self):
        self.j+=1
        img=np.rot90(server.getTofDistance()[0],1,(1,0))
        img = img / img.max()
        img=255*img
        img=img.astype(np.uint8)
        if(self.mode!='default'):
            if(self.mode=='grad'):
                img=transformations.gradimg(img)
            if(self.mode=='thresh'):
                img=transformations.threshgrad(img)
            if(self.mode=='canny'):
                img=cv2.Canny(img,700,600)
        self.sg1_image.setImage(img)


    def updateAmp(self):
        self.k+=1
        img=np.rot90(server.getTofAmplitude()[0],1,(1,0))
        img = img / img.max()
        img=255*img
        img=img.astype(np.uint8)
        if(self.mode!='default'):
            if(self.mode=='grad'):
                img=transformations.gradimg(img)
            if(self.mode=='thresh'):
                img=transformations.threshgrad(img)
            if(self.mode=='canny'):
                img=cv2.Canny(img,220,110)
        self.sg1_image.setImage(img)

    def guiFilterChanged(self):
    
        filterIndex = self.guiFilters.currentIndex()
        switch = {
            0: 'default',
            1: 'grad',
            2: 'thresh',
            3: 'canny',
        }
        self.mode = switch[filterIndex]
        
    def imageTypeChanged(self):
    
        index = self.imageType.currentIndex()
        if index == 0:
            self.startTimerDistance()
        elif index == 1:
            self.startTimerAmplitude()
        elif index == 2:
            self.startTimerGrsc()
        
main()
