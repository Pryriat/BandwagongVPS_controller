import urllib3
import requests
import time
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class res_gui(QThread):
     up = pyqtSignal()
     def __int__(self):
        super(WorkThread, self).__init__()
     def run(self):
        self.up.emit()

class bwh_stat(QWidget):
    def __init__(self,TAR,head,payload):
        super().__init__()
        self.TAR = TAR
        self.head = head
        self.web_payload = payload
        self.timer = QTimer(self)
        self.auto_res = QTimer(self)
        self.res_thread = res_gui()
        self.initUI()
    def initUI(self):
        self.timer.timeout.connect(self.res_label_event)
        self.auto_res.timeout.connect(self.start_update)
        self.auto_res.start(60*1000)
        self.res_thread.up.connect(self.update_data)
        self.setStyleSheet('QProgressBar::chunk{background:rgb(153, 204, 255)}QProgressBar{text-align:center;}')
        self.res_button=QPushButton("Refresh")
        self.res_label=QLabel("Success.")
        self.res_label.setVisible(False)
        self.get_info = 'getServiceInfo'
        self.get_live_info = 'getLiveServiceInfo'
        self.get_usage = 'getRawUsageStats'
        self.info_url = self.TAR + self.get_info
        self.live_url = self.TAR+self.get_live_info
        self.payload = [self.get_info,self.get_live_info,self.get_usage]
        self.info_res = ['ip_addresses','node_location','os','plan','data_usage']
        self.live_res=['ve_status','ve_mac1','disk_usage','ram_stat','swap_stat','ssh_port']
        self.info_data = requests.get(self.info_url,headers=self.head,params=self.web_payload,timeout=500).json()
        self.live_data = requests.get(self.live_url,headers=self.head,params=self.web_payload,timeout=500).json()
        num = range(0,len(self.info_res))
        self.MainLayout = QVBoxLayout()
        self.res_layout = QHBoxLayout()
        self.res_layout.addWidget(self.res_label,Qt.AlignRight)
        self.res_layout.addWidget(self.res_button,Qt.AlignRight)
        self.res_layout.setContentsMargins(450,0,0,0)
        self.status = self.live_data['ve_status']                               
        self.ft = QFont()
        self.ft.setPointSize(15)
        self.label_dict={}
        self.res_button.clicked.connect(self.start_update)

        for (x,y) in zip(self.info_res, num):
            tmplayout = QFormLayout()
            tmplayout.setFormAlignment(Qt.AlignJustify)
            label1 = QLabel(x+' : ',self)
            label1.setFont(self.ft)
            label1.setMinimumWidth(200)
            if x == 'data_usage':
                label2 = QProgressBar(self)
                if self.status != 'Stopped':
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
                    label2.setValue(0)
                    label2.setFormat('%s'%('VPS Stopped'))
            elif x == 'ip_addresses':
                label2 = QLabel(str(self.info_data[x][0]),self)
            else:
                label2 = QLabel(str(self.info_data[x]),self)
            label2.setFont(self.ft)
            label2.setMinimumWidth(50)
            tmplayout.setWidget(y,QFormLayout.LabelRole,label1)
            tmplayout.setWidget(y,QFormLayout.FieldRole,label2)
            tmplayout.setRowWrapPolicy(QFormLayout.DontWrapRows)
            self.MainLayout.addLayout(tmplayout,Qt.AlignCenter)
            self.label_dict[x]=label2

        num = range(0,len(self.live_res))
        for (x,y) in zip(self.live_res, num):
            tmplayout = QFormLayout()
            tmplayout.setFormAlignment(Qt.AlignJustify)
            label1 = QLabel(x+' : ',self)
            label1.setFont(self.ft)
            label1.setMinimumWidth(200)
            if x == 'disk_usage':
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
        self.MainLayout.addLayout(self.res_layout,Qt.AlignCenter)

        self.MainLayout.addStretch(1)
        self.setLayout(self.MainLayout)
        self.show()

    def start_update(self):
        self.res_thread.start()
    def update_data(self):
        self.res_label.setVisible(True)
        self.timer.start(10*1000)
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
                    self.label_dict[x].setFormat('%s'%('VPS Stopped'))
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
                    self.label_dict[x].setFormat('%s'%('VPS Stopped'))
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
                    self.label_dict[x].setFormat('%s'%('VPS Stopped'))
            elif x == 'swap_stat':
                if self.status != 'Stopped':
                    if self.live_data['swap_total_kb'] is None or self.live_data['swap_available_kb'] is None:
                        self.label_dict[x].setValue(0)
                        self.label_dict[x].setFormat('%s'%('SWAP Unloaded'))
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
                    self.label_dict[x].setFormat('%s'%('VPS Stopped'))
            else:
               self.label_dict[x].setText(str(self.live_data[x]))
        self.update()
    def res_label_event(self):
        self.res_label.setVisible(False)



