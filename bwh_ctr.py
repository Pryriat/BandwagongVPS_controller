import urllib3
import requests
import time
import PyQt5
import base64
import json
import linecache
from bwh_add_host import bwh_add_host
#from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class bwh_controls(QWidget):
    '''
    控制窗口
    参数说明：
    与主窗体类相同（参见bwh_ma.py)
    '''
    def __init__(self,fa,TAR,head,web_payload,trans):
        super().__init__()
        self.fa = fa
        self.TAR = TAR
        self.head = head
        self.web_payload = web_payload
        self.timer = QTimer(self)#用于定时隐藏按钮的QTimer类
        self.trans = trans
        self.initUI()
    def initUI(self):
        self.shell_url = self.TAR+'basicShell/exec'#shell API的URL

        #布局初始化
        self.lft_main_layout = QVBoxLayout()
        self.lft_down_layout = QGridLayout()
        self.lft_layout = QFormLayout()
        self.rht_layout = QVBoxLayout()
        self.send_layout = QHBoxLayout()
        self.mainlayout = QGridLayout()

        #控件初始化
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
        self.dual_host_view = QListWidget()
        self.dual_host_delete = QPushButton(self.tr("delete"))
        self.dual_host_add = QPushButton(self.tr("add host"))
        self.dual_host_select = QPushButton(self.tr("select"))
        self.current_host_label = QLabel(self.tr("current host:"))
        self.current_host = QLabel()

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
        self.lft_layout.setWidget(6,QFormLayout.LabelRole,self.current_host_label)
        self.lft_layout.setWidget(6,QFormLayout.FieldRole,self.current_host)
        self.lft_layout.setRowWrapPolicy(QFormLayout.DontWrapRows)

        self.lft_down_layout.addWidget(self.dual_host_view,0,0,3,3)
        self.lft_down_layout.addWidget(self.dual_host_add,3,0,1,1)
        self.lft_down_layout.addWidget(self.dual_host_delete,3,1,1,1)
        self.lft_down_layout.addWidget(self.dual_host_select,3,2,1,1)
        self.lft_main_layout.addLayout(self.lft_layout)
        self.lft_main_layout.addLayout(self.lft_down_layout)

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
        self.dual_host_add.clicked.connect(self.dual_host_add_event)
        self.dual_host_delete.clicked.connect(self.dual_host_delete_event)
        self.dual_host_select.clicked.connect(self.dual_host_select_event)

        self.mainlayout.addLayout(self.lft_main_layout,0,0)
        self.mainlayout.addLayout(self.rht_layout,0,1)

        self.setLayout(self.mainlayout)
        self.dual_host_view_update()

    def restart_event(self):
        '''重启VPS'''
        self.timer.timeout.connect(lambda:self.label_event(self.restart_lab))#QTimer与隐藏按钮的方法挂钩
        self.timer.start(10*1000)#默认显示10秒
        self.restart_data = requests.get(self.TAR+'restart',headers=self.head,params=self.web_payload,timeout=500).json()
        if(self.restart_data['error'] == 0):
            self.restart_lab.setVisible(True)
        else:
            self.restart_lab.setText(self.tr("Restart failed, error code = %d"%(self.restart_data['error'])))
            self.restart_lab.setVisible(True)

    def start_event(self):
        '''启动VPS'''
        self.timer.timeout.connect(lambda:self.label_event(self.start_lab))
        self.timer.start(10*1000)
        self.start_data = requests.get(self.TAR+'start',headers=self.head,params=self.web_payload,timeout=500).json()
        if(self.start_data['error'] == 0):
            self.start_lab.setVisible(True)
        else:
            self.start_lab.setText(self.tr("Start failed, error code = %d"%(self.start_data['error'])))
            self.start_lab.setVisible(True)

    def stop_event(self):
        '''停止VPS'''
        self.timer.timeout.connect(lambda:self.label_event(self.stop_lab))
        self.timer.start(10*1000)
        self.stop_data = requests.get(self.TAR+'stop',headers=self.head,params=self.web_payload,timeout=500).json()
        if(self.stop_data['error'] == 0):
            self.stop_lab.setVisible(True)
        else:
            self.stop_lab.setText(self.tr("Stop failed, error code = %d"%(stop_data['error'])))
            self.stop_lab.setVisible(True)

    def kill_event(self):
        '''强制停机'''
        self.timer.timeout.connect(lambda:self.label_event(self.kill_lab))
        self.timer.start(10*1000)
        self.kill_data = requests.get(self.TAR+'kill',headers=self.head,params=self.web_payload,timeout=500).json()
        if(self.restart_data['error'] == 0):
            self.kill_lab.setVisible(True)
        else:
            self.kill_lab.setText(self.tr("Kill failed, error code = %d"%(restart_data['error'])))
            self.kill_lab.setVisible(True)

    def shell_event(self):
        '''命令行方法'''
        script = self.shell_input.text()
        shell_payload = self.web_payload
        shell_payload['command'] = script
        self.shell_output.insertPlainText('[root@#]'+script+'\n')#模拟终端的输出
        self.shell_input.clear()#点击发送按钮后清空输入框
        data = requests.get(self.shell_url,headers=self.head,params=shell_payload,timeout=500).json()
        if data['error'] == 0:
            self.shell_output.insertPlainText(data['message']+'\n')
        else:
            self.shell_output.insertPlainText(self.tr("Error!\n, Error_code : %d"%(data['error'])))
        self.shell_output.moveCursor(QTextCursor.End)

    def lan_event(self):
        '''变更语言的方法'''
        #读取本地配置文件
        num = 0
        with open(".\data.ini",'rb') as f:
            self.lan_data = f.readlines()
        with open(".\data.ini",'wb') as f:
            for line in self.lan_data:
                if num == self.dual_host_view.currentRow() + 1:
                    data = base64.b64decode(line)
                    data = json.loads(data.decode())
                    data['lan'] = self.lan_input.currentIndex()
                    f.write(base64.b64encode(json.dumps(data).encode()))
                    f.write('\n'.encode())
                else:
                    f.write(line)
                num += 1

        a = QMessageBox()
        #写入成功提示
        a.information(a,self.tr("Success"),self.tr("Language will be changed after resrart the application"))


    def label_event(self,label):
        '''隐藏控件的方法'''
        label.setVisible(False)

    def dual_host_view_update(self):
        self.dual_host_view.clear()
        self.file = open(".\data.ini",'rb')
        fr = True
        tmp_i = 0
        for lines in self.file:
            if fr:
                self.dual_host_currentindex = int(base64.b64decode(lines).decode())
                fr = False
            else:
                tmp_data = json.loads(base64.b64decode(lines).decode())
                self.dual_host_view.addItem(tmp_data['name'])
                if tmp_i == self.dual_host_currentindex:
                    self.current_host.setText(tmp_data['name'])
            tmp_i += 1
        self.dual_host_view.setCurrentRow(self.dual_host_currentindex-1)
        self.dual_host_view.update()


    def dual_host_add_event(self):
        if bwh_add_host(self.trans).exec_() == QDialog.Accepted:
            self.dual_host_view_update()

    def dual_host_delete_event(self):
        num = 0
        a = QMessageBox.warning(self,self.tr("Warning"),self.tr("host data will be deleted!"),QMessageBox.Yes|QMessageBox.No)
        if a == QMessageBox.Yes:
            with open(".\data.ini",'rb') as f:
                self.tmp_data = f.readlines()
            with open(".\data.ini",'wb') as f:
                for line in self.tmp_data:
                    if num == self.dual_host_view.currentRow() + 1:
                        pass
                    else:
                        f.write(line)
                    num += 1
        self.dual_host_view_update()

    def dual_host_select_event(self):
        num = 0
        with open(".\data.ini",'rb') as f:
            self.tmp_data = f.readlines()
        for x in self.tmp_data:
            if num == self.dual_host_view.currentRow() + 1:
                self.change_data = json.loads(base64.b64decode(x).decode())
            else:
                pass
            num += 1

        num = 0
        with open(".\data.ini",'wb') as f:
            for x in self.tmp_data:
                if num == 0:
                    f.write(base64.b64encode(str(self.dual_host_view.currentRow()+1).encode()))
                    f.write('\n'.encode())
                else:
                    f.write(x)
                num += 1

        a = QMessageBox()
        #写入成功提示
        a.information(a,self.tr("Success"),self.tr("host will be changed after resrart the application"))
