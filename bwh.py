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
from bwh_stat import bwh_stat
from bwh_ctr import bwh_controls
from bwh_ma import mainwindow
from bwh_lg import login

stat = 0
TAR = 'https://api.64clouds.com/v1/'
web_payload = {}
head = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
}
if __name__ == '__main__':
    app = QApplication(sys.argv)
    trans = QTranslator()
    if os.path.exists("./data.ini") == False:
        lo = login()
        lo.show()
        if lo.exec_() == QDialog.Accepted:
            pass
        else:
            sys.exit()
    file = open("./data.ini",'rb')
    data = file.read()
    data = base64.b64decode(data)
    try:
        data = json.loads(data.decode())
        web_payload= {'api_key':data['api'],'veid':data['veid']}
        lan = data['lan']
        file.close()
    except:
        file.close()
        a = QMessageBox()
        a.critical(a,"Error","stored data error,please restart appliacation to login again")
        os.remove("./data.ini")
        sys.exit()
    if lan == 1:
        trans.load("zh_CN")
        app.installTranslator(trans)
    ma = mainwindow(TAR,head,web_payload,lan)
    ma.show()
    sys.exit(app.exec())
