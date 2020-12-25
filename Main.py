import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
import func


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.map1 = QWebEngineView(self)
        self.button_waves_month = QPushButton("Waves by month")
        self.button_waves_month_day = QPushButton("Waves by DD/MM")
        self.button_des_houses = QPushButton("All_houses")
        self.button_source_country = QPushButton("Sources in more than 1 country")
        self.button_waves_source = QPushButton("Avarge waves amount")
        self.button_height = QPushButton("Waves heigh(magnitude)")
        self.button_distance_from_source = QPushButton("Waves distance from source", self)
        self.button_japan = QPushButton('Waves height in Japan', self)
        self.button_wave = QPushButton('Waves by country', self)
        self.button_source = QPushButton('Sources by country', self)
        self.button_do_not_remember = QPushButton("Sources by validity and century", self)
        self.title = "Data_Play"
        self.initUI()
        self.setFixedHeight(600)
        self.setFixedWidth(1000)

    def initUI(self):
        self.setWindowTitle(self.title)

        vlayout = QVBoxLayout(self)
        hlayout = QHBoxLayout(self)

        hlayout.addWidget(self.button_source)
        hlayout.addWidget(self.button_wave)
        hlayout.addWidget(self.button_japan)

        vlayout.addLayout(hlayout)

        hlayout1 = QHBoxLayout(self)
        hlayout1.addWidget(self.button_distance_from_source)
        hlayout1.addWidget(self.button_height)
        hlayout1.addWidget(self.button_waves_source)

        vlayout.addLayout(hlayout1)

        hlayout2 = QHBoxLayout(self)
        hlayout2.addWidget(self.button_source_country)
        hlayout2.addWidget(self.button_des_houses)
        hlayout2.addWidget(self.button_waves_month_day)
        vlayout.addLayout(hlayout2)
        hlayout3 = QHBoxLayout(self)
        hlayout3.addWidget(self.button_waves_month)
        hlayout3.addWidget(self.button_do_not_remember)
        vlayout.addLayout(hlayout3)
        vlayout.addWidget(self.map1)

        self.button_wave.clicked.connect(self.on_click_waves)
        self.button_source.clicked.connect(self.on_click_source)
        self.button_japan.clicked.connect(self.on_click_japan)
        self.button_distance_from_source.clicked.connect(self.on_click_distance)
        self.button_height.clicked.connect(self.on_click_height)
        self.button_waves_source.clicked.connect(self.on_click_waves_source)
        self.button_source_country.clicked.connect(self.on_click_source_country)
        self.button_des_houses.clicked.connect(self.on_click_des_houses)
        self.button_waves_month_day.clicked.connect(self.on_click_waves_month_day)
        self.button_waves_month.clicked.connect(self.on_click_waves_month)
        self.button_do_not_remember.clicked.connect(self.on_click_too_big_name)

    def on_click_waves(self):
        map = func.map_waves_country()
        self.map1.setHtml(map.to_html(include_plotlyjs='cdn'))

    def on_click_source(self):
        map = func.map_source_country()
        self.map1.setHtml(map.to_html(include_plotlyjs='cdn'))

    def on_click_japan(self):
        map = func.wave_height_japan()
        self.map1.setHtml(map.to_html(include_plotlyjs='cdn'))

    def on_click_distance(self):
        func.waves_source_distance()

    def on_click_height(self):
        func.height_magnitude()

    def on_click_waves_source(self):
        i, okPressed = QInputDialog.getInt(self, "Years", "Input how many years:", 30, 0, 1000, 1)
        if okPressed:
            func.waves_source(i)

    def on_click_source_country(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Saved to file: SOURCE_COUNTRY_VALUE.csv")
        msgBox.setWindowTitle("SAVED")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            map = func.source_country()
            self.map1.setHtml(map.to_html(include_plotlyjs='cdn'))

    def on_click_des_houses(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("ALL_HOUSES_DAMAGE_OR_DESTROYED.csv")
        msgBox.setWindowTitle("SAVED")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            func.des_houses()

    def on_click_waves_month_day(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("WAVES_BY_EVERY_MONTH_DAY.CSV")
        msgBox.setWindowTitle("SAVED")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            func.waves_month_day()

    def on_click_waves_month(self):
        func.waves_month()

    def on_click_too_big_name(self):
        bar = func.source_validity_century()
        self.map1.setHtml(bar.to_html(include_plotlyjs='cdn'))


app = QApplication(sys.argv)
view = App()
view.show()
app.exec_()
