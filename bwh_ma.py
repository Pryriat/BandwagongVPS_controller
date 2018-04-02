import PyQt5
import base64
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from bwh_stat import bwh_stat
from bwh_ctr import bwh_controls

class mainwindow(QWidget):
    def __init__(self,TAR,head,web_payload,parent=None):
        super().__init__()
        self.tray = QSystemTrayIcon(self)
        #self.timer = QTimer(self)
        #self.timer.timeout.connect(self.warn)
        #self.timer.start(20*1000)
        self.quitAction = QAction("&Quit",self,triggered=qApp.quit)
        self.showAction = QAction("&Show",self,triggered=self.showNormal)
        self.Tray_icon_menu = QMenu(self)
        self.Tray_icon_menu.addAction(self.showAction)
        self.Tray_icon_menu.addAction(self.quitAction)
        self.tray.setContextMenu(self.Tray_icon_menu)
        self.tray.setIcon(QIcon('final.ico' ))
        self.tray.activated.connect(self.db_cilcked)
        self.tray.messageClicked.connect(self.showNormal)
        self.tray.show()
        self.bwh_stat = bwh_stat(TAR,head,web_payload)
        self.bwh_control =bwh_controls(TAR,head,web_payload)
        self.tray.setToolTip("IP : %s\nRAM : %s%%\nSwap : %s%% \nBandwidth : %s%% "%(self.bwh_stat.info_data['ip_addresses'][0],str(self.bwh_stat.ram_stat_value),\
            str(self.bwh_stat.swap_stat_value),str(self.bwh_stat.data_usage_value)))
        self.setWindowTitle(self.tr("bwh_contorler"))
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint|Qt.Window)
        self.tabwidget = QTabWidget(self)
        self.tabwidget.addTab(self.bwh_stat,"bwh_stat")
        self.tabwidget.addTab(self.bwh_control,"bwh_control")
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tabwidget)
        self.setLayout(self.vbox)
        self.resize(640,480)
        self.setFixedSize(640,480)
        

    def hideEvent(self, event):
        self.hide()
    def closeEvent(self, QCloseEvent):
        self.tray.hide()
        return super().closeEvent(QCloseEvent)
    def db_cilcked(self,reason):
        if reason == 2:
            self.showNormal()
    def warn(self):
        if int((float(self.bwh_stat.live_data['plan_ram']/1024-self.bwh_stat.live_data['mem_available_kb'])/float(self.bwh_stat.live_data['plan_ram']/1024))*100) >= 50:
            self.tray.showMessage("",'Ram too high')
   