import urllib3
import requests
import time
import sys
import PyQt5
import io
import os
import base64
import json
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

stat = 0
TAR = 'https://api.64clouds.com/v1/'

web_payload = {}

head = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
}


class bwh_stat(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.get_info = 'getServiceInfo'
        self.get_live_info = 'getLiveServiceInfo'
        self.get_usage = 'getRawUsageStats'
        self.info_url = TAR + self.get_info
        self.live_url = TAR+self.get_live_info
        self.payload = [self.get_info,self.get_live_info,self.get_usage]
        self.info_data = requests.get(self.info_url,headers=head,params=web_payload,timeout=500).json()
        self.live_data = requests.get(self.live_url,headers=head,params=web_payload,timeout=500).json()
        self.info_res = ['ip_addresses','node_location','os','plan','data_usage']
        self.live_res=['ve_status','ve_mac1','disk_usage','ram_stat','swap_stat','ssh_port']


        num = range(0,len(self.info_res))
        self.MainLayout = QVBoxLayout()
        self.ft = QFont()
        self.ft.setPointSize(15)
        for (x,y) in zip(self.info_res, num):
            tmplayout = QFormLayout()
            tmplayout.setFormAlignment(Qt.AlignJustify)
            label1 = QLabel(x+' : ',self)
            label1.setFont(self.ft)
            label1.setMinimumWidth(200)
            if x == 'data_usage':
                label2 = QProgressBar(self)
                label2.setValue(int(self.info_data['data_counter']/self.info_data['plan_monthly_data']*100))
                label2.setFormat('%sG / %sG'%(str(round(self.info_data['data_counter']/1024/1024/1024,2)),str(round(self.info_data['plan_monthly_data']/1024/1024/1024,2))))
                label2.setAlignment(Qt.AlignRight)
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

        num = range(0,len(self.live_res))
        for (x,y) in zip(self.live_res, num):
            tmplayout = QFormLayout()
            tmplayout.setFormAlignment(Qt.AlignJustify)
            label1 = QLabel(x+' : ',self)
            label1.setFont(self.ft)
            label1.setMinimumWidth(200)
            if x == 'disk_usage':
                label2 = QProgressBar(self)
                label2.setValue(int(self.live_data['ve_used_disk_space_b']/self.info_data['plan_disk']*100))
                label2.setFormat('%sG / %sG'%(str(round(self.live_data['ve_used_disk_space_b']/1024/1024/1024,2)),str(round(self.live_data['plan_disk']/1024/1024/1024,2))))
                label2.setAlignment(Qt.AlignRight)
            elif x == 'ram_stat':
                label2 = QProgressBar(self)
                label2.setValue(int((float(self.live_data['plan_ram']/1024-self.live_data['mem_available_kb'])/float(self.live_data['plan_ram']/1024))*100))
                label2.setFormat('%sM / %sM'%(str(round((self.live_data['plan_ram']/1024/1024-self.live_data['mem_available_kb']/1024),2)),str(round(self.live_data['plan_ram']/1024/1024,2))))
                label2.setAlignment(Qt.AlignRight)
            elif x == 'swap_stat':
                label2 = QProgressBar(self)
                label2.setValue(int( ((self.live_data['swap_total_kb'] - self.live_data['swap_available_kb']) /self.live_data['swap_total_kb'])*100 ))
                label2.setFormat('%sM / %sM'%(str(round(self.live_data['swap_total_kb']/1024 - self.live_data['swap_available_kb']/1024,2)),str(round(self.live_data['swap_total_kb']/1024,2))))
            else:
                label2 = QLabel(str(self.live_data[x]),self)
                
            label2.setFont(self.ft)
            label2.setMinimumWidth(50)
            tmplayout.setWidget(y,QFormLayout.LabelRole,label1)
            tmplayout.setWidget(y,QFormLayout.FieldRole,label2)
            tmplayout.setRowWrapPolicy(QFormLayout.DontWrapRows)
            self.MainLayout.addLayout(tmplayout,Qt.AlignCenter)

        self.MainLayout.addStretch(1)
        self.setLayout(self.MainLayout)
        self.show()

class bwh_controls(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.shell_url = TAR+'basicShell/exec'
        self.lft_layout = QFormLayout()
        self.rht_layout = QVBoxLayout()
        self.send_layout = QHBoxLayout()
        self.mainlayout = QGridLayout()

        self.lft_layout.setFormAlignment(Qt.AlignAbsolute)
        self.start_btn = QPushButton("Start")
        self.start_btn.resize(50,50)
        self.start_lab = QLabel("Start success")
        self.start_lab.setVisible(False)
        self.stop_btn = QPushButton("Stop")
        self.stop_lab = QLabel("Stop success")
        self.stop_lab.setVisible(False)
        self.kill_btn = QPushButton("Kill")
        self.kill_lab = QLabel("Kill success")
        self.kill_lab.setVisible(False)
        self.restart_btn = QPushButton("Restart")
        self.restart_lab = QLabel("Restart success")
        self.restart_lab.setVisible(False)
        self.shell_label = QLabel("Basic shell")
        self.shell_btn = QPushButton("Send")
        self.shell_output = QTextEdit()
        self.shell_input = QLineEdit()
        self.shell_output.setReadOnly(True)

        self.lft_layout.setWidget(0,QFormLayout.LabelRole,self.start_btn)
        self.lft_layout.setWidget(0,QFormLayout.FieldRole,self.start_lab)
        self.lft_layout.setWidget(1,QFormLayout.LabelRole,self.stop_btn)
        self.lft_layout.setWidget(1,QFormLayout.FieldRole,self.stop_lab)
        self.lft_layout.setWidget(2,QFormLayout.LabelRole,self.kill_btn)
        self.lft_layout.setWidget(2,QFormLayout.FieldRole,self.kill_lab)
        self.lft_layout.setWidget(3,QFormLayout.LabelRole,self.restart_btn)
        self.lft_layout.setWidget(3,QFormLayout.FieldRole,self.restart_lab)
        self.lft_layout.setRowWrapPolicy(QFormLayout.DontWrapRows)

        self.send_layout.addWidget(self.shell_input)
        self.send_layout.addWidget(self.shell_btn)
        self.mainlayout.setColumnStretch(0,1)
        self.mainlayout.setColumnStretch(1,4)

        self.rht_layout.addWidget(self.shell_label)
        self.rht_layout.addWidget(self.shell_output)
        self.rht_layout.addLayout(self.send_layout)


        self.restart_btn.clicked.connect(self.restart_event)
        self.start_btn.clicked.connect(self.start_event)
        self.stop_btn.clicked.connect(self.stop_event)
        self.kill_btn.clicked.connect(self.kill_event)
        self.shell_btn.clicked.connect(self.shell_event)

        self.mainlayout.addLayout(self.lft_layout,0,0)
        self.mainlayout.addLayout(self.rht_layout,0,1)

        self.setLayout(self.mainlayout)
    def restart_event(self):
        self.restart_data = requests.get(TAR+'restart',headers=head,params=web_payload,timeout=500).json()
        if(self.restart_data['error'] == 0):
            self.restart_lab.setVisible(True)
        else:
            self.restart_lab.setText("Restart failed, error code = %d"%(self.restart_data['error']))
            self.restart_lab.setVisible(True)
    def start_event(self):
        self.start_data = requests.get(TAR+'start',headers=head,params=web_payload,timeout=500).json()
        if(self.start_data['error'] == 0):
            self.start_lab.setVisible(True)
        else:
            self.start_lab.setText("Start failed, error code = %d"%(self.start_data['error']))
            self.start_lab.setVisible(True)
    def stop_event(self):
        self.stop_data = requests.get(TAR+'stop',headers=head,params=web_payload,timeout=500).json()
        if(self.stop_data['error'] == 0):
            self.stop_lab.setVisible(True)
        else:
            self.stop_lab.setText("Stop failed, error code = %d"%(self.stop_data['error']))
            self.stop_lab.setVisible(True)
    def kill_event(self):
        self.kill_data = requests.get(TAR+'kill',headers=head,params=web_payload,timeout=500).json()
        if(self.restart_data['error'] == 0):
            self.kill_lab.setVisible(True)
        else:
            self.kill_lab.setText("Kill failed, error code = %d"%(self.restart_data['error']))
            self.kill_lab.setVisible(True)
    def shell_event(self):
        script = self.shell_input.text()
        shell_payload = web_payload
        shell_payload['command'] = script
        self.shell_output.insertPlainText('[root@#]'+script+'\n')
        self.shell_input.clear()
        data = requests.get(self.shell_url,headers=head,params=shell_payload,timeout=500).json()
        if data['error'] == 0:
            self.shell_output.insertPlainText(data['message']+'\n')
        else:
            self.shell_output.insertPlainText("Error!\n, Error_code : %d"%(data['error']))
        self.shell_output.moveCursor(QTextCursor.End)
        

class mainwindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.bwh_stat = bwh_stat()
        self.bwh_control = bwh_controls()
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
 
class login(QDialog):
     def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle("Login")
        self.api_input = QLineEdit(self)
        self.veid_input = QLineEdit(self)
        self.api_lab = QLabel("API_KEY")
        self.veid_lab = QLabel("VEID")
        self.mainlayout = QFormLayout()
        self.mainlayout.setWidget(0,QFormLayout.LabelRole,self.veid_lab)
        self.mainlayout.setWidget(0,QFormLayout.FieldRole,self.veid_input)
        self.mainlayout.setWidget(1,QFormLayout.LabelRole,self.api_lab)
        self.mainlayout.setWidget(1,QFormLayout.FieldRole,self.api_input)
        self.ml = QVBoxLayout()
        self.ml.addLayout(self.mainlayout)
        self.btn = QPushButton("Confirm")
        self.btn.clicked.connect(self.login_event)
        self.ml.addWidget(self.btn)
        self.setLayout(self.ml)
        self.resize(400,120)

     def login_event(self):
        self.file = open(".\data.ini",'wb')
        self.data = base64.b64encode(json.dumps({'veid':self.veid_input.text(),'api':self.api_input.text()}).encode())
        global web_payload
        web_payload = {'veid':self.veid_input.text(),'api_key':self.api_input.text()}
        self.file.write(self.data)
        self.file.close()
        self.accept()

        
app = QApplication(sys.argv)
if os.path.exists("./data.ini") == True:
    file = open("./data.ini",'rb')
    data = file.read()
    data = base64.b64decode(data)
    data = json.loads(data.decode())
    global web_payload
    web_payload = {'api_key':data['api'],'veid':data['veid']}
    file.close()
    ma = mainwindow()
    ma.show()
else:
    lo = login()
    lo.show()
    if lo.exec_() == QDialog.Accepted: 
        ma = mainwindow()
        ma.show()
    else:
        sys.exit()
if stat == 3:
    sys.exit()
sys.exit(app.exec())

