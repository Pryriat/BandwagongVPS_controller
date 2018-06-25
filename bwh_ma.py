import PyQt5
import base64
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from bwh_stat import bwh_stat
from bwh_ctr import bwh_controls

class mainwindow(QWidget):
    '''
    mainwindow：控制器的主窗体类
    参数说明：
    TAR : KiwiVM VPS信息API的地址
    web_playload : 身份验证信息，包括VEID 和 api_key
    trans : 语言选项 0为英文，1为中文
    '''
    def __init__(self,TAR,head,web_payload,trans,parent=None):
        super().__init__()
        self.tray = QSystemTrayIcon(self)#托盘类
        self.trans = trans
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap("final.ico"))
        self.web_payload = web_payload
        #self.timer = QTimer(self)
        #self.timer.timeout.connect(self.warn)
        #self.timer.start(20*1000)
        self.quitAction = QAction(self.tr("&Quit"),self,triggered=qApp.quit)
        self.showAction = QAction(self.tr("&Show"),self,triggered=self.showNormal)
        self.Tray_icon_menu = QMenu(self)
        self.Tray_icon_menu.addAction(self.showAction)
        self.Tray_icon_menu.addAction(self.quitAction)
        self.tray.setContextMenu(self.Tray_icon_menu)
        self.tray.setIcon(self.icon)
        self.setWindowIcon(self.icon)
        self.tray.activated.connect(self.db_cilcked)
        self.tray.messageClicked.connect(self.showNormal)
        self.tray.show()

        self.bwh_stat = bwh_stat(TAR,head,self.web_payload,self.trans)#初始化信息窗体
        self.bwh_control =bwh_controls(self,TAR,head,self.web_payload,self.trans)#初始化控制窗体

        #根据trans的值改变输出内容
        if self.trans == 0:
            self.tray.setToolTip(self.tr("IP : %s\nRAM : %s%%\nSwap : %s%% \nBandwidth : %s%% "%(self.bwh_stat.info_data['ip_addresses'][0],str(self.bwh_stat.ram_stat_value),\
                str(self.bwh_stat.swap_stat_value),str(self.bwh_stat.data_usage_value))))
        elif self.trans == 1:
            self.tray.setToolTip(self.tr("IP地址 : %s\n内存 : %s%%\n交换分区 : %s%% \n流量使用情况 : %s%% "%(self.bwh_stat.info_data['ip_addresses'][0],str(self.bwh_stat.ram_stat_value),\
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
        '''最小化方法'''
        self.hide()
    def closeEvent(self, QCloseEvent):
        '''重写关闭方法，增加了隐藏图标的过程'''
        self.tray.hide()
        return super().closeEvent(QCloseEvent)
    def db_cilcked(self,reason):
        '''双击显示窗体'''
        if reason == 2:
            self.showNormal()
    def warn(self):
        '''警告窗体，内存占用过高(未实装)'''
        if int((float(self.bwh_stat.live_data['plan_ram']/1024-self.bwh_stat.live_data['mem_available_kb'])/float(self.bwh_stat.live_data['plan_ram']/1024))*100) >= 50:
            self.tray.showMessage("",self.tr('Ram too high'))
