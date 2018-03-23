import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from bwh_stat import bwh_stat
from bwh_ctr import bwh_controls

class mainwindow(QDialog):
    def __init__(self,TAR,head,web_payload,parent=None):
        super().__init__()
        self.bwh_stat = bwh_stat(TAR,head,web_payload)
        self.bwh_control =bwh_controls(TAR,head,web_payload)
        self.setWindowTitle(self.tr("bwh_contorler"))
        self.tabwidget = QTabWidget(self)
        self.tabwidget.addTab(self.bwh_stat,"bwh_stat")
        self.tabwidget.addTab(self.bwh_control,"bwh_control")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tabwidget)
        self.setLayout(self.vbox)
        self.resize(800,480)
    def closeEvent(self, QCloseEvent):
        global stat 
        stat =3 
        return super().closeEvent(QCloseEvent)
