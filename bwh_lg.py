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

class login(QDialog):
    '''登陆窗体类，仅在本地无登陆信息文件时使用'''
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle(self.tr("Login"))

        self.api_input = QLineEdit(self)
        self.veid_input = QLineEdit(self)
        self.lan_input = QComboBox()
        self.lan_input.addItem("English")
        self.lan_input.addItem("简体中文")
        self.api_lab = QLabel("API_KEY")
        self.veid_lab = QLabel("VEID")
        self.lan_lab = QLabel("Language")

        self.mainlayout = QFormLayout()
        self.mainlayout.setWidget(0,QFormLayout.LabelRole,self.veid_lab)
        self.mainlayout.setWidget(0,QFormLayout.FieldRole,self.veid_input)
        self.mainlayout.setWidget(1,QFormLayout.LabelRole,self.api_lab)
        self.mainlayout.setWidget(1,QFormLayout.FieldRole,self.api_input)
        self.mainlayout.setWidget(2,QFormLayout.LabelRole,self.lan_lab)
        self.mainlayout.setWidget(2,QFormLayout.FieldRole,self.lan_input)
        self.ml = QVBoxLayout()
        self.ml.addLayout(self.mainlayout)
        self.btn = QPushButton(self.tr("Confirm"))
        self.btn.clicked.connect(self.login_event)
        self.ml.addWidget(self.btn)
        self.setLayout(self.ml)
        self.resize(400,150)

    def login_event(self):
        '''将登陆窗体的信息写入本地配置文件'''
        self.file = open(".\data.ini",'wb')
        #使用base64编码防止明文存储
        self.data = base64.b64encode(json.dumps({'veid':self.veid_input.text(),'api':self.api_input.text(),'lan':self.lan_input.currentIndex()}).encode())
        global web_payload
        web_payload = {'veid':self.veid_input.text(),'api_key':self.api_input.text()}
        self.file.write(self.data)
        self.file.close()
        self.accept()
