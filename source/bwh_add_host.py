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

class bwh_add_host(QDialog):
    def __init__(self, lan,parent=None):
        super().__init__()
        self.setWindowTitle(self.tr("add new host"))
        self.lan = lan
        self.api_input = QLineEdit()
        self.veid_input = QLineEdit()
        self.name_input = QLineEdit()
        self.api_lab = QLabel(self.tr("API_KEY"))
        self.veid_lab = QLabel(self.tr("VEID"))
        self.name_lab = QLabel(self.tr("Name"))
        self.mainlayout = QFormLayout()
        self.mainlayout.setWidget(0,QFormLayout.LabelRole,self.veid_lab)
        self.mainlayout.setWidget(0,QFormLayout.FieldRole,self.veid_input)
        self.mainlayout.setWidget(1,QFormLayout.LabelRole,self.api_lab)
        self.mainlayout.setWidget(1,QFormLayout.FieldRole,self.api_input)
        self.mainlayout.setWidget(2,QFormLayout.LabelRole,self.name_lab)
        self.mainlayout.setWidget(2,QFormLayout.FieldRole,self.name_input)
        self.ml = QVBoxLayout()
        self.ml.addLayout(self.mainlayout)
        self.btn = QPushButton(self.tr("Confirm"))
        self.mainlayout.addWidget(self.btn)
        self.setLayout(self.ml)
        self.resize(400,150)
        self.btn.clicked.connect(self.bwh_add_event)

    def bwh_add_event(self):
        self.ns = True
        if self.api_input.text() == '' or self.veid_input.text() == '':
            a = QMessageBox()
            a.critical(a,self.tr("Error","api or veid empty!"))
            self.close()
        elif self.name_input.text() == '':
            self.name_input.setText(self.tr("new host"))
        with open('data.ini','ab') as f:
            self.data = base64.b64encode(json.dumps({'name':self.name_input.text(),'veid':self.veid_input.text(),'api':self.api_input.text(),'lan':self.lan}).encode())
            f.write('\n'.encode())
            f.write(self.data)
        self.accept()
