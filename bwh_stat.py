import urllib3
import requests
import time
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class res_gui(QThread):
    '''重写线程类，负责开启新线程刷新控件'''
     up = pyqtSignal()
     def __int__(self):
        super(WorkThread, self).__init__()
     def run(self):
        self.up.emit()

class bwh_stat(QWidget):
    def __init__(self,TAR,head,payload,trans):
        '''VPS信息窗体类
        参数说明：
        与主窗体类相同（参见bwh_ma.py)
        '''
        super().__init__()
        self.TAR = TAR
        self.trans = trans
        self.head = head
        self.web_payload = payload
        self.timer = QTimer(self)#用于设置控件显示超时的QTimer类
        self.auto_res = QTimer(self)#用于设置自动刷新时间的QTimer类
        self.res_thread = res_gui()#用于开启新线程刷新控件的线程类
        self.initUI()

    def trans_label(self):
        '''
        由于使用了迭代的方式初始化控件名称，tr()方法无法获取程序动态运行时的字符串，因此需使用对应键修改的方式汉化
        '''
        for key in self.text_dict.keys():
            if key == 'ip_addresses':
                self.text_dict[key].setText("IP地址")
            elif key == 'node_location':
                self.text_dict[key].setText("VPS节点位置")
            elif key == 'os':
                self.text_dict[key].setText("操作系统")
            elif key == 'plan':
                self.text_dict[key].setText("VPS类型")
            elif key == 'data_usage':
                self.text_dict[key].setText("流量使用情况")
            elif key == 've_status':
                self.text_dict[key].setText("VPS状态")
            elif key == 've_mac1':
                self.text_dict[key].setText("MAC地址")
            elif key == 'disk_usage':
                self.text_dict[key].setText("存储使用情况")
            elif key == 'ram_stat':
                self.text_dict[key].setText("内存使用情况")
            elif key == 'swap_stat':
                self.text_dict[key].setText("交换分区使用情况")
            elif key == 'ssh_port':
                self.text_dict[key].setText("SSH端口")

    def initUI(self):
        self.timer.timeout.connect(self.res_label_event)
        self.auto_res.timeout.connect(self.start_update)
        self.auto_res.start(60*1000)#自动更新时间间隔为60妙
        self.res_thread.up.connect(self.update_data)
        self.setStyleSheet('QProgressBar::chunk{background:rgb(153, 204, 255)}QProgressBar{text-align:center;}')
        self.res_button=QPushButton(self.tr("Refresh"))
        self.res_button.clicked.connect(self.start_update)
        self.res_label=QLabel(self.tr("Success."))
        self.res_label.setVisible(False)
        self.get_info = 'getServiceInfo'
        self.get_live_info = 'getLiveServiceInfo'
        self.get_usage = 'getRawUsageStats'
        self.info_url = self.TAR + self.get_info#获取信息的URL
        self.live_url = self.TAR+self.get_live_info#同上
        self.payload = [self.get_info,self.get_live_info,self.get_usage]
        self.info_res = ['ip_addresses','node_location','os','plan','data_usage']
        self.live_res=['ve_status','ve_mac1','disk_usage','ram_stat','swap_stat','ssh_port']
        self.info_data = requests.get(self.info_url,headers=self.head,params=self.web_payload,timeout=500).json()#获取当前VPS信息
        self.live_data = requests.get(self.live_url,headers=self.head,params=self.web_payload,timeout=500).json()#同上
        self.label_dict={}#存储控件信息
        self.text_dict={}#存储标签信息

        num = range(0,len(self.info_res))
        self.MainLayout = QVBoxLayout()
        self.res_layout = QHBoxLayout()
        self.res_layout.addWidget(self.res_label,Qt.AlignRight)
        self.res_layout.addWidget(self.res_button,Qt.AlignRight)
        self.res_layout.setContentsMargins(450,0,0,0)
        self.status = self.live_data['ve_status']
        self.ft = QFont()
        self.ft.setPointSize(15)


        #根据信息初始化标签
        for (x,y) in zip(self.info_res, num):
            tmplayout = QFormLayout()
            tmplayout.setFormAlignment(Qt.AlignJustify)
            label1 = QLabel(self.tr(x+' : '),self)#设置对应的标签名
            label1.setFont(self.ft)
            label1.setMinimumWidth(200)
            if x == 'data_usage':
                '''流量使用情况控件的处理过程'''
                label2 = QProgressBar(self)
                if self.status != 'Stopped':
                    '''如未停机，则输出相应信息'''
                    self.data_usage_value = int(self.info_data['data_counter']/self.info_data['plan_monthly_data']*100)
                    label2.setValue(self.data_usage_value)
                    label2.setFormat('%sG / %sG'%(str(round(self.info_data['data_counter']/1024/1024/1024,2)),str(round(self.info_data['plan_monthly_data']/1024/1024/1024,2))))
                    label2.setAlignment(Qt.AlignRight)
                    if self.data_usage_value <= 70:
                        label2.setStyleSheet('QProgressBar::chunk{background:rgb(153, 204, 255)}QProgressBar{text-align:center;}')
                    elif self.data_usage_value > 70 and self.data_usage_value <= 90:
                        label2.setStyleSheet('QProgressBar::chunk{background:rgb(255,255,0)}QProgressBar{text-align:center;}')
                    else:
                        label2.setStyleSheet('QProgressBar::chunk{background:rgb(255,0,51)}QProgressBar{text-align:center;}')
                else:
                    '''停机则显示为0'''
                    label2.setValue(0)
                    label2.setFormat('%s'%('VPS Stopped'))
            elif x == 'ip_addresses':
                '''IP地址处理过程'''
                label2 = QLabel(str(self.info_data[x][0]),self)
            else:
                label2 = QLabel(str(self.info_data[x]),self)

            label2.setFont(self.ft)
            label2.setMinimumWidth(50)
            tmplayout.setWidget(y,QFormLayout.LabelRole,label1)
            tmplayout.setWidget(y,QFormLayout.FieldRole,label2)
            tmplayout.setRowWrapPolicy(QFormLayout.DontWrapRows)
            self.MainLayout.addLayout(tmplayout,Qt.AlignCenter)
            self.label_dict[x]=label2#控件信息加入label_dict
            self.text_dict[x]=label1#标签信息加入text_dict

        num = range(0,len(self.live_res))

        #初始化实时信息
        for (x,y) in zip(self.live_res, num):
            tmplayout = QFormLayout()
            tmplayout.setFormAlignment(Qt.AlignJustify)
            label1 = QLabel(self.tr(x+' : '),self)
            label1.setFont(self.ft)
            label1.setMinimumWidth(200)
            if x == 'disk_usage':
                '''存储空间使用情况的处理过程'''
                label2 = QProgressBar(self)
                if self.status != 'Stopped':
                    self.disk_usage_value = int(self.live_data['ve_used_disk_space_b']/self.info_data['plan_disk']*100)
                    label2.setValue(self.disk_usage_value)
                    label2.setFormat('%sG / %sG'%(str(round(self.live_data['ve_used_disk_space_b']/1024/1024/1024,2)),str(round(self.live_data['plan_disk']/1024/1024/1024,2))))
                    label2.setAlignment(Qt.AlignRight)
                    if self.disk_usage_value <= 70:
                        label2.setStyleSheet('QProgressBar::chunk{background:rgb(153, 204, 255)}QProgressBar{text-align:center;}')
                    elif self.disk_usage_value > 70 and self.disk_usage_value <= 90:
                        label2.setStyleSheet('QProgressBar::chunk{background:rgb(255,255,0)}QProgressBar{text-align:center;}')
                    else:
                        label2.setStyleSheet('QProgressBar::chunk{background:rgb(255,0,51)}QProgressBar{text-align:center;}')
                else:
                    label2.setValue(0)
                    label2.setFormat('%s'%('VPS Stopped'))

            elif x == 'ram_stat':
                '''内存占用'''
                label2 = QProgressBar(self)
                if self.status != 'Stopped':
                    self.ram_stat_value = int((float(self.live_data['plan_ram']/1024-self.live_data['mem_available_kb'])/float(self.live_data['plan_ram']/1024))*100)
                    label2.setValue(self.ram_stat_value)
                    label2.setFormat('%sM / %sM'%(str(round((self.live_data['plan_ram']/1024/1024-self.live_data['mem_available_kb']/1024),2)),str(round(self.live_data['plan_ram']/1024/1024,2))))
                    label2.setAlignment(Qt.AlignRight)
                    if self.ram_stat_value <= 70:
                        label2.setStyleSheet('QProgressBar::chunk{background:rgb(153, 204, 255)}QProgressBar{text-align:center;}')
                    elif self.ram_stat_value > 70 and self.ram_stat_value <= 90:
                        label2.setStyleSheet('QProgressBar::chunk{background:rgb(255,255,0)}QProgressBar{text-align:center;}')
                    else:
                        label2.setStyleSheet('QProgressBar::chunk{background:rgb(255,0,51)}QProgressBar{text-align:center;}')
                else:
                    label2.setValue(0)
                    label2.setFormat('%s'%('VPS Stopped'))

            elif x == 'swap_stat':
                '''交换分区'''
                label2 = QProgressBar(self)
                if self.status != 'Stopped':
                    self.swap_stat_value = int( ((self.live_data['swap_total_kb'] - self.live_data['swap_available_kb']) /self.live_data['swap_total_kb'])*100 )
                    label2.setValue(self.swap_stat_value)
                    label2.setFormat('%sM / %sM'%(str(round(self.live_data['swap_total_kb']/1024 - self.live_data['swap_available_kb']/1024,2)),str(round(self.live_data['swap_total_kb']/1024,2))))
                    label2.setAlignment(Qt.AlignRight)
                    if self.swap_stat_value <= 70:
                        label2.setStyleSheet('QProgressBar::chunk{background:rgb(153, 204, 255)}QProgressBar{text-align:center;}')
                    elif self.swap_stat_value > 70 and self.swap_stat_value <= 90:
                        label2.setStyleSheet('QProgressBar::chunk{background:rgb(255,255,0)}QProgressBar{text-align:center;}')
                    else:
                        label2.setStyleSheet('QProgressBar::chunk{background:rgb(255,0,51)}QProgressBar{text-align:center;}')
                else:
                    label2.setValue(0)
                    label2.setFormat('%s'%('VPS Stopped'))

            else:
                label2 = QLabel(str(self.live_data[x]),self)
            label2.setFont(self.ft)
            label2.setMinimumWidth(50)
            tmplayout.setWidget(y,QFormLayout.LabelRole,label1)
            tmplayout.setWidget(y,QFormLayout.FieldRole,label2)
            tmplayout.setRowWrapPolicy(QFormLayout.DontWrapRows)
            self.MainLayout.addLayout(tmplayout,Qt.AlignCenter)
            self.label_dict[x]=label2
            self.text_dict[x]=label1
        self.MainLayout.addLayout(self.res_layout,Qt.AlignCenter)

        self.MainLayout.addStretch(1)
        self.setLayout(self.MainLayout)

        if self.trans == 1:
            #如显示中文则调用翻译标签的方法
            self.trans_label()
        self.show()

    def start_update(self):
        '''自动更新信息'''
        self.res_thread.start()

    def update_data(self):
        '''更新信息的实现'''
        self.res_label.setVisible(True)
        self.timer.start(10*1000)#设置标签的显示超时未10秒
        self.info_data = requests.get(self.info_url,headers=self.head,params=self.web_payload,timeout=500).json()
        self.live_data = requests.get(self.live_url,headers=self.head,params=self.web_payload,timeout=500).json()
        self.status = self.live_data['ve_status']
        num = range(0,len(self.info_res))
        for (x,y) in zip(self.info_res, num):
            if x == 'data_usage':
                if self.status != 'Stopped':
                    self.data_usage_value = int(self.info_data['data_counter']/self.info_data['plan_monthly_data']*100)
                    self.label_dict[x].setValue(self.data_usage_value)
                    self.label_dict[x].setFormat('%sG / %sG'%(str(round(self.info_data['data_counter']/1024/1024/1024,2)),str(round(self.info_data['plan_monthly_data']/1024/1024/1024,2))))
                    self.label_dict[x].setAlignment(Qt.AlignRight)
                    if self.data_usage_value <= 70:
                        self.label_dict[x].setStyleSheet('QProgressBar::chunk{background:rgb(153, 204, 255)}QProgressBar{text-align:center;}')
                    elif self.data_usage_value > 70 and self.data_usage_value <= 90:
                        self.label_dict[x].setStyleSheet('QProgressBar::chunk{background:rgb(255,255,0)}QProgressBar{text-align:center;}')
                    else:
                        self.label_dict[x].setStyleSheet('QProgressBar::chunk{background:rgb(255,0,51)}QProgressBar{text-align:center;}')
                else:
                    self.label_dict[x].setValue(0)
                    self.label_dict[x].setFormat('%s'%(self.tr('VPS Stopped')))
            elif x == 'ip_addresses':
                self.label_dict[x].setText(str(self.info_data[x][0]))
            else :
                self.label_dict[x].setText(str(self.info_data[x]))

        num = range(0,len(self.live_res))

        for (x,y) in zip(self.live_res, num):
            if x == 'disk_usage':
                if self.status != 'Stopped':
                    self.disk_usage_value = int(self.live_data['ve_used_disk_space_b']/self.info_data['plan_disk']*100)
                    self.label_dict[x] .setValue(self.disk_usage_value)
                    self.label_dict[x] .setFormat('%sG / %sG'%(str(round(self.live_data['ve_used_disk_space_b']/1024/1024/1024,2)),str(round(self.live_data['plan_disk']/1024/1024/1024,2))))
                    self.label_dict[x] .setAlignment(Qt.AlignRight)
                    if self.disk_usage_value <= 70:
                        self.label_dict[x].setStyleSheet('QProgressBar::chunk{background:rgb(153, 204, 255)}QProgressBar{text-align:center;}')
                    elif self.disk_usage_value > 70 and self.disk_usage_value <= 90:
                        self.label_dict[x].setStyleSheet('QProgressBar::chunk{background:rgb(255,255,0)}QProgressBar{text-align:center;}')
                    else:
                        self.label_dict[x].setStyleSheet('QProgressBar::chunk{background:rgb(255,0,51)}QProgressBar{text-align:center;}')
                else:
                    self.label_dict[x].setValue(0)
                    self.label_dict[x].setFormat('%s'%(self.tr('VPS Stopped')))
            elif x == 'ram_stat':
                if self.status != 'Stopped':
                    self.ram_stat_value = int((float(self.live_data['plan_ram']/1024-self.live_data['mem_available_kb'])/float(self.live_data['plan_ram']/1024))*100)
                    self.label_dict[x] .setValue(self.ram_stat_value)
                    self.label_dict[x] .setFormat('%sM / %sM'%(str(round((self.live_data['plan_ram']/1024/1024-self.live_data['mem_available_kb']/1024),2)),str(round(self.live_data['plan_ram']/1024/1024,2))))
                    self.label_dict[x] .setAlignment(Qt.AlignRight)
                    if self.ram_stat_value <= 70:
                        self.label_dict[x].setStyleSheet('QProgressBar::chunk{background:rgb(153, 204, 255)}QProgressBar{text-align:center;}')
                    elif self.ram_stat_value > 70 and self.ram_stat_value <= 90:
                        self.label_dict[x].setStyleSheet('QProgressBar::chunk{background:rgb(255,255,0)}QProgressBar{text-align:center;}')
                    else:
                        self.label_dict[x].setStyleSheet('QProgressBar::chunk{background:rgb(255,0,51)}QProgressBar{text-align:center;}')
                else:
                    self.label_dict[x].setValue(0)
                    self.label_dict[x].setFormat('%s'%(self.te('VPS Stopped')))
            elif x == 'swap_stat':
                if self.status != 'Stopped':
                    if self.live_data['swap_total_kb'] is None or self.live_data['swap_available_kb'] is None:
                        self.label_dict[x].setValue(0)
                        self.label_dict[x].setFormat('%s'%(self.tr('SWAP Unloaded')))
                    else:
                        self.swap_stat_value = int( ((self.live_data['swap_total_kb'] - self.live_data['swap_available_kb']) /self.live_data['swap_total_kb'])*100 )
                        self.label_dict[x] .setValue(self.swap_stat_value)
                        self.label_dict[x] .setFormat('%sM / %sM'%(str(round(self.live_data['swap_total_kb']/1024 - self.live_data['swap_available_kb']/1024,2)),str(round(self.live_data['swap_total_kb']/1024,2))))
                        if self.swap_stat_value <= 70:
                            self.label_dict[x].setStyleSheet('QProgressBar::chunk{background:rgb(153, 204, 255)}QProgressBar{text-align:center;}')
                        elif self.swap_stat_value > 70 and self.swap_stat_value <= 90:
                            self.label_dict[x].setStyleSheet('QProgressBar::chunk{background:rgb(255,255,0)}QProgressBar{text-align:center;}')
                        else:
                            self.label_dict[x].setStyleSheet('QProgressBar::chunk{background:rgb(255,0,51)}QProgressBar{text-align:center;}')
                else:
                    self.label_dict[x].setValue(0)
                    self.label_dict[x].setFormat('%s'%(self.te('VPS Stopped')))
            else:
               self.label_dict[x].setText(str(self.live_data[x]))
        self.update()
    def res_label_event(self):
        '''隐藏控件的方法'''
        self.res_label.setVisible(False)
