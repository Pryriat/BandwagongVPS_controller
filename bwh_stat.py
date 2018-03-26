import urllib3
import requests
import time
import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class bwh_stat(QWidget):
    def __init__(self,TAR,head,payload):
        super().__init__()
        self.TAR = TAR
        self.head = head
        self.web_payload = payload
        self.timer = QTimer(self)
        self.initUI()
    def initUI(self):
        self.timer.timeout.connect(self.res_label_event)
        self.res_button=QPushButton("Refresh")
        self.res_label=QLabel("Refresh success.")
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
        self.res_layout.setContentsMargins(600,0,0,0)
        self.status = self.live_data['ve_status']                               
        self.ft = QFont()
        self.ft.setPointSize(15)
        self.label_dict={}
        self.res_button.clicked.connect(self.update_data)

        for (x,y) in zip(self.info_res, num):
            tmplayout = QFormLayout()
            tmplayout.setFormAlignment(Qt.AlignJustify)
            label1 = QLabel(x+' : ',self)
            label1.setFont(self.ft)
            label1.setMinimumWidth(200)
            if x == 'data_usage':
                label2 = QProgressBar(self)
                if self.status != 'Stopped':
                    label2.setValue(int(self.info_data['data_counter']/self.info_data['plan_monthly_data']*100))
                    label2.setFormat('%sG / %sG'%(str(round(self.info_data['data_counter']/1024/1024/1024,2)),str(round(self.info_data['plan_monthly_data']/1024/1024/1024,2))))
                    label2.setAlignment(Qt.AlignRight)
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
                    label2.setValue(int(self.live_data['ve_used_disk_space_b']/self.info_data['plan_disk']*100))
                    label2.setFormat('%sG / %sG'%(str(round(self.live_data['ve_used_disk_space_b']/1024/1024/1024,2)),str(round(self.live_data['plan_disk']/1024/1024/1024,2))))
                    label2.setAlignment(Qt.AlignRight)
                else:
                    label2.setValue(0)
                    label2.setFormat('%s'%('VPS Stopped'))
            elif x == 'ram_stat':
                label2 = QProgressBar(self)
                if self.status != 'Stopped':
                    label2.setValue(int((float(self.live_data['plan_ram']/1024-self.live_data['mem_available_kb'])/float(self.live_data['plan_ram']/1024))*100))
                    label2.setFormat('%sM / %sM'%(str(round((self.live_data['plan_ram']/1024/1024-self.live_data['mem_available_kb']/1024),2)),str(round(self.live_data['plan_ram']/1024/1024,2))))
                    label2.setAlignment(Qt.AlignRight)
                else:
                    label2.setValue(0)
                    label2.setFormat('%s'%('VPS Stopped'))
            elif x == 'swap_stat':
                label2 = QProgressBar(self)
                if self.status != 'Stopped':
                    label2.setValue(int( ((self.live_data['swap_total_kb'] - self.live_data['swap_available_kb']) /self.live_data['swap_total_kb'])*100 ))
                    label2.setFormat('%sM / %sM'%(str(round(self.live_data['swap_total_kb']/1024 - self.live_data['swap_available_kb']/1024,2)),str(round(self.live_data['swap_total_kb']/1024,2))))
                    label2.setAlignment(Qt.AlignRight)
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
                    self.label_dict[x].setValue(int(self.info_data['data_counter']/self.info_data['plan_monthly_data']*100))
                    self.label_dict[x].setFormat('%sG / %sG'%(str(round(self.info_data['data_counter']/1024/1024/1024,2)),str(round(self.info_data['plan_monthly_data']/1024/1024/1024,2))))
                    self.label_dict[x].setAlignment(Qt.AlignRight)
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
                    self.label_dict[x] .setValue(int(self.live_data['ve_used_disk_space_b']/self.info_data['plan_disk']*100))
                    self.label_dict[x] .setFormat('%sG / %sG'%(str(round(self.live_data['ve_used_disk_space_b']/1024/1024/1024,2)),str(round(self.live_data['plan_disk']/1024/1024/1024,2))))
                    self.label_dict[x] .setAlignment(Qt.AlignRight)
                else:
                    self.label_dict[x].setValue(0)
                    self.label_dict[x].setFormat('%s'%('VPS Stopped'))
            elif x == 'ram_stat':
                if self.status != 'Stopped':
                    self.label_dict[x] .setValue(int((float(self.live_data['plan_ram']/1024-self.live_data['mem_available_kb'])/float(self.live_data['plan_ram']/1024))*100))
                    self.label_dict[x] .setFormat('%sM / %sM'%(str(round((self.live_data['plan_ram']/1024/1024-self.live_data['mem_available_kb']/1024),2)),str(round(self.live_data['plan_ram']/1024/1024,2))))
                    self.label_dict[x] .setAlignment(Qt.AlignRight)
                else:
                    self.label_dict[x].setValue(0)
                    self.label_dict[x].setFormat('%s'%('VPS Stopped'))
            elif x == 'swap_stat':
                if self.status != 'Stopped':
                    if self.live_data['swap_total_kb'] is None or self.live_data['swap_available_kb'] is None:
                        self.label_dict[x].setValue(0)
                        self.label_dict[x].setFormat('%s'%('SWAP Unloaded'))
                    else:
                        self.label_dict[x] .setValue(int( ((self.live_data['swap_total_kb'] - self.live_data['swap_available_kb']) /self.live_data['swap_total_kb'])*100 ))
                        self.label_dict[x] .setFormat('%sM / %sM'%(str(round(self.live_data['swap_total_kb']/1024 - self.live_data['swap_available_kb']/1024,2)),str(round(self.live_data['swap_total_kb']/1024,2))))
                else:
                    self.label_dict[x].setValue(0)
                    self.label_dict[x].setFormat('%s'%('VPS Stopped'))
            else:
               self.label_dict[x].setText(str(self.live_data[x]))
        self.update()
    def res_label_event(self):
        self.res_label.setVisible(False)
