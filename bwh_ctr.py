import urllib3
import requests
import time
import PyQt5
import base64
import json
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class bwh_controls(QWidget):
    def __init__(self,TAR,head,web_payload,trans):
        super().__init__()
        self.TAR = TAR
        self.head = head
        self.web_payload = web_payload
        self.timer = QTimer(self)
        self.trans = trans
        self.initUI()
    def initUI(self):
        self.shell_url = self.TAR+'basicShell/exec'
        self.lft_layout = QFormLayout()
        self.rht_layout = QVBoxLayout()
        self.send_layout = QHBoxLayout()
        self.mainlayout = QGridLayout()

        self.lft_layout.setFormAlignment(Qt.AlignAbsolute)
        self.start_btn = QPushButton(self.tr("Start"))
        self.start_btn.resize(50,50)
        self.start_lab = QLabel(self.tr("Start success"))
        self.start_lab.setVisible(False)
        self.stop_btn = QPushButton(self.tr("Stop"))
        self.stop_lab = QLabel(self.tr("Stop success"))
        self.stop_lab.setVisible(False)
        self.kill_btn = QPushButton(self.tr("Kill"))
        self.kill_lab = QLabel(self.tr("Kill success"))
        self.kill_lab.setVisible(False)
        self.restart_btn = QPushButton(self.tr("Restart"))
        self.restart_lab = QLabel(self.tr("Restart success"))
        self.restart_lab.setVisible(False)
        self.shell_label = QLabel(self.tr("Basic shell"))
        self.shell_btn = QPushButton(self.tr("Send"))
        self.lan_label = QLabel(self.tr("Language"))
        self.lan_input = QComboBox()
        self.lan_input.addItem("English")
        self.lan_input.addItem("简体中文")
        self.lan_input.setCurrentIndex(self.trans)
        self.lan_btn = QPushButton(self.tr("Confirm"))
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
        self.lft_layout.setWidget(4,QFormLayout.LabelRole,self.lan_label)
        self.lft_layout.setWidget(4,QFormLayout.FieldRole,self.lan_input)
        self.lft_layout.setWidget(5,QFormLayout.FieldRole,self.lan_btn)
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
        self.lan_btn.clicked.connect(self.lan_event)

        self.mainlayout.addLayout(self.lft_layout,0,0)
        self.mainlayout.addLayout(self.rht_layout,0,1)

        self.setLayout(self.mainlayout)
    def restart_event(self):
        self.timer.timeout.connect(lambda:self.label_event(self.restart_lab))
        self.timer.start(10*1000)
        self.restart_data = requests.get(self.TAR+'restart',headers=self.head,params=self.web_payload,timeout=500).json()
        if(self.restart_data['error'] == 0):
            self.restart_lab.setVisible(True)
        else:
            self.restart_lab.setText(self.tr("Restart failed, error code = %d"%(self.restart_data['error'])))
            self.restart_lab.setVisible(True)
    def start_event(self):
        self.timer.timeout.connect(lambda:self.label_event(self.start_lab))
        self.timer.start(10*1000)
        self.start_data = requests.get(self.TAR+'start',headers=self.head,params=self.web_payload,timeout=500).json()
        if(self.start_data['error'] == 0):
            self.start_lab.setVisible(True)
        else:
            self.start_lab.setText(self.tr("Start failed, error code = %d"%(self.start_data['error'])))
            self.start_lab.setVisible(True)
    def stop_event(self):
        self.timer.timeout.connect(lambda:self.label_event(self.stop_lab))
        self.timer.start(10*1000)
        self.stop_data = requests.get(self.TAR+'stop',headers=self.head,params=self.web_payload,timeout=500).json()
        if(self.stop_data['error'] == 0):
            self.stop_lab.setVisible(True)
        else:
            self.stop_lab.setText(self.tr("Stop failed, error code = %d"%(stop_data['error'])))
            self.stop_lab.setVisible(True)
    def kill_event(self):
        self.timer.timeout.connect(lambda:self.label_event(self.kill_lab))
        self.timer.start(10*1000)
        self.kill_data = requests.get(self.TAR+'kill',headers=self.head,params=self.web_payload,timeout=500).json()
        if(self.restart_data['error'] == 0):
            self.kill_lab.setVisible(True)
        else:
            self.kill_lab.setText(self.tr("Kill failed, error code = %d"%(restart_data['error'])))
            self.kill_lab.setVisible(True)
    def shell_event(self):
        script = self.shell_input.text()
        shell_payload = self.web_payload
        shell_payload['command'] = script
        self.shell_output.insertPlainText('[root@#]'+script+'\n')
        self.shell_input.clear()
        data = requests.get(self.shell_url,headers=self.head,params=shell_payload,timeout=500).json()
        if data['error'] == 0:
            self.shell_output.insertPlainText(data['message']+'\n')
        else:
            self.shell_output.insertPlainText(self.tr("Error!\n, Error_code : %d"%(data['error'])))
        self.shell_output.moveCursor(QTextCursor.End)

    def lan_event(self):
        file = open("./data.ini",'rb')
        data = file.read()
        data = base64.b64decode(data)
        data = json.loads(data.decode())
        re_data = base64.b64encode(json.dumps({'veid':data['veid'],'api':data['api'],'lan':self.lan_input.currentIndex()}).encode())
        file.close()
        file = open("./data.ini",'wb')
        file.write(re_data)
        file.close()
        a = QMessageBox()
        a.information(a,self.tr("Success"),self.tr("Language will be changed after resrart the application"))
    def label_event(self,label):
        label.setVisible(False)
