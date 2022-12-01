# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wsTool.py'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import websocket
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import time
from designer.wsTool import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import threading
isDisplay = True
isSave = False
isSend = False
# websocket回调
def on_message(ws, message):
    global f
    # ui_components.textBrowser_recvMsg.setText(str(message))+"\n"
    if (isDisplay):
        ui_components.textBrowser_recvMsg.append(str(message))
        ui_components.textBrowser_recvMsg.moveCursor(ui_components.textBrowser_recvMsg.textCursor().End)
    if (isSave):
        f.write(str(message) + "\n")

# websocket回调
def on_error(ws, error):
    print(ws)
    print(error)

# websocket回调
def on_close(ws):
    print(ws)
    print("### closed ###")

# websocket连接
def ws(ws_host):
    print(ws_host)
    websocket.enableTrace(True)
    global wsclient
    wsclient = websocket.WebSocketApp(
        ws_host,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close)
    print("send")
    # ws.send("112321312")
    wsclient.run_forever()

def saveFile():
    global isSave,f
    if(isSave):
        # f.close()
        ui_components.label_5.setText("未存储")
        ui_components.pushButton_save.setText(QtCore.QCoreApplication.translate("MainWindow", "开始"))
        # print("关闭文件")
        f.close()
        isSave = False
    else:
        ui_components.label_5.setText("存储中")
        ui_components.pushButton_save.setText(QtCore.QCoreApplication.translate("MainWindow", "完成"))
        # print("打开文件写入")
        file_name = str(ui_components.textEdit_fileName.toPlainText()) + ".txt"
        f = open(file_name, "a")
        isSave = True

class ws_conn(QThread):
    def __init__(self, parent=None):
            super().__init__(parent)

    def run(self):
        # global ws
        ws_url = str(ui_components.textEdit_wsUrl.toPlainText())
        ws(ws_url)




def chageDisplay():
    global isDisplay
    if(isDisplay):
        isDisplay = False
        ui_components.pushButton_break.setText(QtCore.QCoreApplication.translate("MainWindow", "继续"))
    else:
        isDisplay = True
        ui_components.pushButton_break.setText(QtCore.QCoreApplication.translate("MainWindow", "暂停"))

def clearDisplay():
    ui_components.textBrowser_recvMsg.clear()

def sendMsg():
    global wsclient
    msg = str(ui_components.textEdit_sendMsg.toPlainText())
    wsclient.send(msg)

def sendMsgOntime():
    global isSend

    if(isSend):
        ui_components.pushButton_rateSend.setText(QtCore.QCoreApplication.translate("MainWindow", "定时发送"))
        isSend = False
    else:
        ui_components.pushButton_rateSend.setText(QtCore.QCoreApplication.translate("MainWindow", "结束发送"))
        isSend = True

class sendTimer(QThread):
    def __init__(self, parent=None):
            super().__init__(parent)

    def run(self):
        global isSend
        while True:
            if(isSend):
                rate = ui_components.lineEdit_rate.text()
                sendMsg()
                time.sleep(float(rate))
            else:
                pass



if __name__ == '__main__':
    # application 对象
    app = QApplication(sys.argv)

    # QMainWindow对象
    mainwindow = QMainWindow()

    # 这是qt designer实现的Ui_MainWindow类
    ui_components = Ui_MainWindow()

    # 调用setupUi()方法，注册到QMainWindwo对象
    ui_components.setupUi(mainwindow)

    ui_components.ws_conn = ws_conn()
    ui_components.ws_sendTimer = sendTimer()
    ui_components.ws_sendTimer.start()
    ui_components.pushButton_connect.clicked.connect(lambda :ui_components.ws_conn.start())
    ui_components.pushButton_break.clicked.connect(lambda :chageDisplay())
    ui_components.pushButton_clear.clicked.connect(lambda :clearDisplay())
    ui_components.pushButton_save.clicked.connect(lambda :saveFile())
    ui_components.pushButton_send.clicked.connect(lambda: sendMsg())
    ui_components.pushButton_rateSend.clicked.connect(lambda: sendMsgOntime())



    # 显示
    mainwindow.show()

    sys.exit(app.exec_())