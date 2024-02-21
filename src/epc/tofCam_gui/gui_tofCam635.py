import sys
import qdarktheme
from PySide6 import QtWidgets
from epc.tofCam_gui import Base_GUI_TOFcam
from epc.tofCam_gui.widgets import VideoWidget, FilterSettings, IntegrationTimes, GroupBoxSelection, DropDownSetting, SettingsGroup, SpinBoxSetting, RoiSettings

class GUI_TOFcam635(Base_GUI_TOFcam):
    def __init__(self, title='TOF CAM 635 VIDEO STREAM', parent=None):
        super(GUI_TOFcam635, self).__init__(title)

        # Create Widgets
        self.imageView = VideoWidget()
        self.imageTypeWidget = GroupBoxSelection('Image Type', ['Distance', 'Amplitude', 'Grayscale'], self)
        self.guiFilterGroupBox = GroupBoxSelection('GUI Filters', ['None'])
        self.hdrModeDropDown = DropDownSetting('HDR Mode', ['HDR Off', 'HDR Spatial', 'HDR Temporal'])
        self.modulationChannel = DropDownSetting('Modulation Channel', ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'])
        self.modulationFrequency = DropDownSetting('Modulation Frequency', ['20 MHz'])
        self.operationMode = DropDownSetting('Operation Mode', ['WFO'])
        self.modeSettings = SettingsGroup('Camera Modes', [self.modulationFrequency, self.modulationChannel, self.operationMode, self.hdrModeDropDown])
        self.integrationTimes = IntegrationTimes(['WFOV1', 'WFOV2', 'WFOV3', 'WFOV4', 'Gray'], [125, 250, 375, 500, 1000], [1000, 1000, 1000, 1000, 50000])
        self.minAmplitude = SpinBoxSetting('Minimal Amplitude', 0, 1000)
        self.builtInFilter = FilterSettings()
        self.roiSettings = RoiSettings(160, 60, steps=4)

        # Create Layout for settings
        self.settingsLayout.addWidget(self.imageTypeWidget)
        self.settingsLayout.addWidget(self.guiFilterGroupBox)
        self.settingsLayout.addWidget(self.modeSettings)
        self.settingsLayout.addWidget(self.integrationTimes)
        self.settingsLayout.addWidget(self.minAmplitude)
        self.settingsLayout.addWidget(self.builtInFilter)
        self.settingsLayout.addWidget(self.roiSettings)

        self.complete_setup()
        
def main():
    app = QtWidgets.QApplication(sys.argv)

    qdarktheme.setup_theme()
    stream = GUI_TOFcam635()
    stream.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()