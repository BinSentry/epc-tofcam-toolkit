from PySide6.QtWidgets import QMainWindow, QGridLayout, QVBoxLayout, QWidget
from epc.tofCam_gui.video_widget import VideoWidget
from epc.tofCam_gui.settings_widget import ToolBar

class Base_GUI_TOFcam(QMainWindow):
    def __init__(self, title: str, parent=None):
        super(Base_GUI_TOFcam, self).__init__()
        self.setWindowTitle(title)

        # create main widgets
        self.toolBar = ToolBar(self)
        self.imageView = VideoWidget()
        self.settingsLayout = QVBoxLayout()
        self.mainLayout = QGridLayout()
        self.widget = QWidget()

        self.addToolBar(self.toolBar)

    def complete_setup(self):
        self.mainLayout.setSpacing(10)
        self.mainLayout.addLayout(self.settingsLayout, 0, 0)
        self.mainLayout.addWidget(self.imageView, 0, 1)
        self.mainLayout.setColumnStretch(1, 3)

        self.widget.setLayout(self.mainLayout)  
        self.setCentralWidget(self.widget)

        self.resize(1200, 600)
