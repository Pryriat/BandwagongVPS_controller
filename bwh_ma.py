import PyQt5
import base64
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from bwh_stat import bwh_stat
from bwh_ctr import bwh_controls

class mainwindow(QWidget):
    def __init__(self,TAR,head,web_payload,trans,parent=None):
        super().__init__()
        self.tray = QSystemTrayIcon(self)
        self.trans = trans
        #self.timer = QTimer(self)
        #self.timer.timeout.connect(self.warn)
        #self.timer.start(20*1000)
        self.quitAction = QAction(self.tr("&Quit"),self,triggered=qApp.quit)
        self.showAction = QAction(self.tr("&Show"),self,triggered=self.showNormal)
        self.Tray_icon_menu = QMenu(self)
        self.Tray_icon_menu.addAction(self.showAction)
        self.Tray_icon_menu.addAction(self.quitAction)
        self.tray.setContextMenu(self.Tray_icon_menu)
        self.tray.setIcon(QIcon('final.ico' ))
        self.tray.activated.connect(self.db_cilcked)
        self.tray.messageClicked.connect(self.showNormal)
        self.tray.show()
        self.bwh_stat = bwh_stat(TAR,head,web_payload,self.trans)
        self.bwh_control =bwh_controls(TAR,head,web_payload)
        if self.trans == 0:
            self.tray.setToolTip(self.tr("IP : %s\nRAM : %s%%\nSwap : %s%% \nBandwidth : %s%% "%(self.bwh_stat.info_data['ip_addresses'][0],str(self.bwh_stat.ram_stat_value),\
                str(self.bwh_stat.swap_stat_value),str(self.bwh_stat.data_usage_value))))
        elif self.trans == 1:
            self.tray.setToolTip(self.tr("IP地址 : %s\n内存 : %s%%\n交换分区 : %s%% \n带宽使用情况 : %s%% "%(self.bwh_stat.info_data['ip_addresses'][0],str(self.bwh_stat.ram_stat_value),\
                str(self.bwh_stat.swap_stat_value),str(self.bwh_stat.data_usage_value))))
        self.setWindowTitle(self.tr("bwh_contorler"))
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint|Qt.Window)
        self.tabwidget = QTabWidget(self)
        self.tabwidget.addTab(self.bwh_stat,self.tr("bwh_stat"))
        self.tabwidget.addTab(self.bwh_control,self.tr("bwh_control"))
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.tabwidget)
        self.setLayout(self.vbox)
        self.resize(800,600)
        self.setFixedSize(800,600)


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
            self.tray.showMessage("",self.tr('Ram too high'))
