# -*- coding: utf-8 -*-

################################################################################################################################
## 主要功能 查詢窗口(視窗)信息
#  直接拖拉到想查詢的窗口上即可
#  顯示的信息有 程序的 icon, 句炳, 類名, 標題, 線程ID, 進程ID, 進程名稱, 進程路徑, CPU使用量, 線程數, 窗口左上角的座標, 窗口四角座標
#  下方功能按鈕功能有 指定窗口置頂與取消, 窗口顯示到頂部, 強制關閉程序, 打開程序的文件所在的資料夾
#
## 作者: Miles J
################################################################################################################################

import sys

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt, Signal
from PySide6.QtGui import QFont, QIcon, QPixmap, QMouseEvent
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QWidget

import win32gui
import win32ui
import win32con
import win32api

import win32process
import psutil
import subprocess
from PIL import Image
import os


class LongButton(QPushButton):
    val = Signal(
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        str)

    def __init__(self, text: str, parent):
        super().__init__(text, parent)
        self.ico_x = 32

    def i_con(self, exePath2):
        try:
            exe_path = exePath2.replace("\\", "/")  # 替換
            large, small = win32gui.ExtractIconEx(f'{exe_path}', 0)
            use_icon = large[0]
            destroy_icon = small[0]
            win32gui.DestroyIcon(destroy_icon)
            hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
            hbmp = win32ui.CreateBitmap()
            hbmp.CreateCompatibleBitmap(hdc, self.ico_x, self.ico_x)
            hdc = hdc.CreateCompatibleDC()
            hdc.SelectObject(hbmp)
            hdc.DrawIcon((0, 0), use_icon)
            bmpstr = hbmp.GetBitmapBits(True)
            img = Image.frombuffer(
                'RGBA',
                (32, 32),
                bmpstr, 'raw', 'BGRA', 0, 1
            )
            img.save('icon.png')
        except BaseException:
            pass

    # 重寫mouseReleaseEvent方法，關閉timer
    def mouseReleaseEvent(self, e):
        try:
            point = win32api.GetCursorPos()  # 鼠標位置
            hwnd = win32gui.WindowFromPoint(point)  # 窗口句柄
            title = win32gui.GetWindowText(hwnd)  # 窗口標題
            clsname = win32gui.GetClassName(hwnd)  # 窗口類名
            hread_id, process_id = win32process.GetWindowThreadProcessId(
                hwnd)  # 線程ID  進程ID
            process = psutil.Process(process_id)  # 程序名稱  通過進程ID獲取
            p_bin = psutil.Process(process_id).exe()  # 程序路徑  通過進程ID獲取
            mem_percent = psutil.Process(
                process_id).memory_percent()  # CPU利用率  通過進程ID獲取
            num_threads = psutil.Process(
                process_id).num_threads()  # 線程數  通過進程ID獲取
            left, top, right, bottom = win32gui.GetWindowRect(
                hwnd)  # 窗口坐標  通過窗口句柄獲取 四個角的坐標
            self.i_con(p_bin)

            self.val.emit(str(hwnd),
                          str(clsname),
                          str(title),
                          str(hread_id),
                          str(process_id),
                          str(process.name()),
                          str(p_bin),
                          str(mem_percent),
                          str(num_threads),
                          str(point[0]),
                          str(point[1]),
                          str(left),
                          str(top),
                          str(right),
                          str(bottom))
        except:
            pass


class MaskWindow(QWidget):
    def __init__(self):
        super(MaskWindow, self).__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowOpacity(0.1)
        self.setWindowFlags(Qt.Tool)
        # tt = Window()
        # print(tt.drag)

    # def mouseReleaseEvent(self, e):
    #     if self.drag:
    #         distance = event.globalPosition().toPoint() - self.mouse_start_pt
    #         self.move(self.window_pos + distance)


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setup_ui(self)
        self.drag = False
        drag = False
        # 准許拖拉
        self.setAcceptDrops(True)
        # 隱藏窗口編筐
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # self.v_hwnd = None
        # self.v_process_id = None
        # self.v_process = None
        # self.v_p_bin = None

    def setup_ui(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(520, 740)
        icon = QIcon()
        icon.addFile(u"icons.png", QSize(), QIcon.Normal, QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet(u"background-color: #1B1E23;")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 40, 121, 31))
        font = QFont()
        font.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC;")
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(360, 50, 50, 50))
        self.label_2.setStyleSheet(u"background-color: none;\n"
"border: none;")
        self.label_2.setPixmap(QPixmap(u"pictures.png"))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(0, 110, 520, 631))
        self.label_4.setStyleSheet(u"background-color: #30303C;\n"
"border-top-left-radius: 20px;\n"
"border-top-right-radius: 20px;")
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 130, 61, 25))
        font1 = QFont()
        font1.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font1.setPointSize(11)
        font1.setBold(True)
        self.label_5.setFont(font1)
        self.label_5.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC;")
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(90, 130, 121, 25))
        font2 = QFont()
        font2.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font2.setPointSize(9)
        self.label_6.setFont(font2)
        self.label_6.setStyleSheet(u"background-color: #1B1E23;\n"
"color: #DCE1EC;\n"
"padding-left: 2px;")

        # self.pushButton = QPushButton(Form)
        self.pushButton = LongButton('Click', self)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(440, 50, 50, 50))
        self.pushButton.setStyleSheet(u"background-color: none;\n"
"border: none;")
        icon1 = QIcon()
        icon1.addFile(u"Key.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setIconSize(QSize(50, 50))

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(100, 420, 326, 251))
        self.label_3.setStyleSheet(u"background-color: none;")
        self.label_3.setPixmap(QPixmap(u"win.png"))
        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(240, 130, 61, 25))
        self.label_7.setFont(font1)
        self.label_7.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC")
        self.label_8 = QLabel(Form)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(310, 130, 191, 25))
        self.label_8.setFont(font2)
        self.label_8.setStyleSheet(u"background-color: #1B1E23;\n"
"color: #DCE1EC;\n"
"padding-left: 2px;")
        self.label_9 = QLabel(Form)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(20, 170, 61, 25))
        self.label_9.setFont(font1)
        self.label_9.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC")
        self.label_10 = QLabel(Form)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(90, 170, 411, 25))
        self.label_10.setFont(font2)
        self.label_10.setStyleSheet(u"background-color: #1B1E23;\n"
"color: #DCE1EC;\n"
"padding-left: 2px;")
        self.label_11 = QLabel(Form)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(20, 210, 61, 25))
        self.label_11.setFont(font1)
        self.label_11.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC")
        self.label_12 = QLabel(Form)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(90, 210, 121, 25))
        self.label_12.setFont(font2)
        self.label_12.setStyleSheet(u"background-color: #1B1E23;\n"
"color: #DCE1EC;\n"
"padding-left: 2px;")
        self.label_13 = QLabel(Form)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(310, 210, 61, 25))
        self.label_13.setFont(font1)
        self.label_13.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC")
        self.label_14 = QLabel(Form)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(380, 210, 121, 25))
        self.label_14.setFont(font2)
        self.label_14.setStyleSheet(u"background-color: #1B1E23;\n"
"color: #DCE1EC;\n"
"padding-left: 2px;")
        self.label_15 = QLabel(Form)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(20, 250, 61, 25))
        self.label_15.setFont(font1)
        self.label_15.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC")
        self.label_16 = QLabel(Form)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(90, 250, 411, 25))
        self.label_16.setFont(font2)
        self.label_16.setStyleSheet(u"background-color: #1B1E23;\n"
"color: #DCE1EC;\n"
"padding-left: 2px;")
        self.label_17 = QLabel(Form)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(20, 290, 61, 25))
        self.label_17.setFont(font1)
        self.label_17.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC")
        self.label_18 = QLabel(Form)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(90, 290, 411, 25))
        self.label_18.setFont(font2)
        self.label_18.setStyleSheet(u"background-color: #1B1E23;\n"
"color: #DCE1EC;\n"
"padding-left: 2px;")
        self.label_19 = QLabel(Form)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(20, 330, 71, 25))
        self.label_19.setFont(font1)
        self.label_19.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC")
        self.label_20 = QLabel(Form)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(100, 330, 181, 25))
        self.label_20.setFont(font2)
        self.label_20.setStyleSheet(u"background-color: #1B1E23;\n"
"color: #DCE1EC;\n"
"padding-left: 2px;")
        self.label_21 = QLabel(Form)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(310, 330, 61, 25))
        self.label_21.setFont(font1)
        self.label_21.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC")
        self.label_22 = QLabel(Form)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QRect(380, 330, 121, 25))
        self.label_22.setFont(font2)
        self.label_22.setStyleSheet(u"background-color: #1B1E23;\n"
"color: #DCE1EC;\n"
"padding-left: 2px;")
        self.label_23 = QLabel(Form)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setGeometry(QRect(150, 430, 61, 25))
        self.label_23.setFont(font1)
        self.label_23.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC")
        self.label_24 = QLabel(Form)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setGeometry(QRect(76, 430, 51, 25))
        font3 = QFont()
        font3.setPointSize(11)
        font3.setBold(True)
        self.label_24.setFont(font3)
        self.label_24.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC;")
        self.label_24.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_25 = QLabel(Form)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(313, 430, 61, 25))
        self.label_25.setFont(font1)
        self.label_25.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC")
        self.label_26 = QLabel(Form)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setGeometry(QRect(398, 430, 51, 25))
        self.label_26.setFont(font3)
        self.label_26.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC;")
        self.label_27 = QLabel(Form)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setGeometry(QRect(150, 640, 61, 25))
        self.label_27.setFont(font1)
        self.label_27.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC")
        self.label_28 = QLabel(Form)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setGeometry(QRect(76, 640, 51, 25))
        self.label_28.setFont(font3)
        self.label_28.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC;")
        self.label_28.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_29 = QLabel(Form)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setGeometry(QRect(313, 640, 61, 25))
        self.label_29.setFont(font1)
        self.label_29.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC")
        self.label_30 = QLabel(Form)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setGeometry(QRect(398, 640, 51, 25))
        self.label_30.setFont(font3)
        self.label_30.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC;")
        self.label_31 = QLabel(Form)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setGeometry(QRect(20, 370, 71, 25))
        self.label_31.setFont(font1)
        self.label_31.setStyleSheet(u"background-color: none;\n"
"color: #DCE1EC")
        self.label_32 = QLabel(Form)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setGeometry(QRect(100, 370, 121, 25))
        self.label_32.setFont(font2)
        self.label_32.setStyleSheet(u"background-color: #1B1E23;\n"
"color: #DCE1EC;\n"
"padding-left: 2px;")
        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(435, 0, 40, 36))
        self.pushButton_2.setStyleSheet(u"QPushButton {background-color: none;\n"
"border: none;}\n"
"QPushButton::hover {background-color: #30303C;}\n"
"")
        icon2 = QIcon()
        icon2.addFile(u"narr.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_2.setIcon(icon2)
        self.pushButton_3 = QPushButton(Form)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(475, 0, 40, 36))
        self.pushButton_3.setStyleSheet(u"QPushButton {background-color: none;\n"
"border: none;}\n"
"QPushButton::hover {background-color: #E81123;}\n"
"")
        icon3 = QIcon()
        icon3.addFile(u"close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_3.setIcon(icon3)
        self.pushButton_4 = QPushButton(Form)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(10, 10, 31, 24))
        self.pushButton_4.setStyleSheet(u"background-color: none;\n"
"border: none;")
        self.pushButton_4.setIcon(icon)
        self.pushButton_4.setIconSize(QSize(22, 22))
        self.pushButton_5 = QPushButton(Form)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(20, 700, 75, 26))
        font4 = QFont()
        font4.setFamilies([u"\u5fae\u8f6f\u96c5\u9ed1"])
        font4.setPointSize(10)
        font4.setBold(True)
        self.pushButton_5.setFont(font4)
        self.pushButton_5.setStyleSheet(u"QPushButton {background-color: #568AF2;\n"
"border-radius: 2px;\n"
"color: #F5F6F9;}\n"
"QPushButton::hover {background-color: #1B1E23;\n"
"color: #C3CCDF;}")
        self.pushButton_6 = QPushButton(Form)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(107, 700, 75, 26))
        self.pushButton_6.setFont(font4)
        self.pushButton_6.setStyleSheet(u"QPushButton {background-color: #568AF2;\n"
"border-radius: 2px;\n"
"color: #F5F6F9;}\n"
"QPushButton::hover {background-color: #1B1E23;\n"
"color: #C3CCDF;}")
        self.pushButton_7 = QPushButton(Form)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(194, 700, 75, 26))
        self.pushButton_7.setFont(font4)
        self.pushButton_7.setStyleSheet(u"QPushButton {background-color: #568AF2;\n"
"border-radius: 2px;\n"
"color: #F5F6F9;}\n"
"QPushButton::hover {background-color: #1B1E23;\n"
"color: #C3CCDF;}")
        self.pushButton_8 = QPushButton(Form)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(281, 700, 75, 26))
        self.pushButton_8.setFont(font4)
        self.pushButton_8.setStyleSheet(u"QPushButton {background-color: #568AF2;\n"
"border-radius: 2px;\n"
"color: #F5F6F9;}\n"
"QPushButton::hover {background-color: #1B1E23;\n"
"color: #C3CCDF;}")
        self.pushButton_9 = QPushButton(Form)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setGeometry(QRect(368, 700, 130, 26))
        self.pushButton_9.setFont(font4)
        self.pushButton_9.setStyleSheet(u"QPushButton {background-color: #568AF2;\n"
"border-radius: 2px;\n"
"color: #F5F6F9;}\n"
"QPushButton::hover {background-color: #1B1E23;\n"
"color: #C3CCDF;}")

        self.retranslateUi(Form)

        self.pushButton.val.connect(self.obtain)
        # 區域 光標 樣式: Cross
        self.pushButton.setCursor(Qt.CrossCursor)
        self.pushButton_2.clicked.connect(self.mini_button)
        self.pushButton_3.clicked.connect(self.close_button)

        self.pushButton_5.clicked.connect(self.set_top)
        # self.pushButton_5.clicked.connect(self.set_mask)

        self.pushButton_6.clicked.connect(self.set_down)
        self.pushButton_7.clicked.connect(self.set_top_p)
        self.pushButton_8.clicked.connect(self.get_over)
        self.pushButton_9.clicked.connect(self.open_folder)

        QMetaObject.connectSlotsByName(Form)
        # setupUi

    def set_mask(self):
        # self.mask = MaskWindow()
        # # self.mask.move(self.v_left + 7, self.v_top)
        # self.mask.setGeometry(self.v_left + 8, self.v_top + 30, (self.v_right - self.v_left) - 16, (self.v_bottom - self.v_top) - 38)
        # self.mask.show()

        # self.setCursor(Qt.CrossCursor)

        print(self.v_left + 8, self.v_top + 30, (self.v_right - self.v_left) - 16, (self.v_bottom - self.v_top) - 38)

        # self.setEnabled(False)


    def obtain(
            self,
            hwnd,
            clsname,
            title,
            hread_id,
            process_id,
            process,
            p_bin,
            mem_percent,
            num_threads,
            point0,
            point1,
            left,
            top,
            right,
            bottom):
        self.v_hwnd = hwnd
        self.v_process_id = process_id
        self.v_process = process
        self.v_p_bin = p_bin

        self.v_left = int(left)
        self.v_top = int(top)
        self.v_right = int(right)
        self.v_bottom = int(bottom)

        self.label_6.setText(hwnd)
        self.label_8.setText(clsname)
        self.label_10.setText(title)
        self.label_12.setText(hread_id)
        self.label_14.setText(process_id)
        self.label_16.setText(process)
        self.label_18.setText(p_bin)
        self.label_20.setText(mem_percent)
        self.label_22.setText(num_threads)
        self.label_32.setText('{}， {}'.format(point0, point1))
        self.label_24.setText(top)
        self.label_26.setText(right)
        self.label_28.setText(left)
        self.label_30.setText(bottom)
        pixmap = QPixmap('icon.png')
        self.label_2.setPixmap(pixmap)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u7a97\u53e3\u53e5\u67c4\u83b7\u53d6", None))
        self.label_2.setText("")
        self.label_4.setText("")
        self.label_5.setText(QCoreApplication.translate("Form", u"\u7a97\u53e3\u53e5\u67c4", None))
        self.label_6.setText("")
        self.pushButton.setText("")
        self.label_3.setText("")
        self.label_7.setText(QCoreApplication.translate("Form", u"\u7a97\u53e3\u7c7b\u540d", None))
        self.label_8.setText("")
        self.label_9.setText(QCoreApplication.translate("Form", u"\u7a97\u53e3\u6807\u9898", None))
        self.label_10.setText("")
        self.label_11.setText(QCoreApplication.translate("Form", u"\u7ebf\u7a0b ID", None))
        self.label_12.setText("")
        self.label_13.setText(QCoreApplication.translate("Form", u"\u8fdb\u7a0b ID", None))
        self.label_14.setText("")
        self.label_15.setText(QCoreApplication.translate("Form", u"\u8fdb\u7a0b\u540d\u79f0", None))
        self.label_16.setText("")
        self.label_17.setText(QCoreApplication.translate("Form", u"\u8fdb\u7a0b\u8def\u5f84", None))
        self.label_18.setText("")
        self.label_19.setText(QCoreApplication.translate("Form", u"CPU \u7528\u91cf", None))
        self.label_20.setText("")
        self.label_21.setText(QCoreApplication.translate("Form", u"\u7ebf\u7a0b\u6570", None))
        self.label_22.setText("")
        self.label_23.setText(QCoreApplication.translate("Form", u"\u7a97\u53e3\u5de6\u4e0a", None))
        self.label_24.setText("")
        self.label_25.setText(QCoreApplication.translate("Form", u"\u7a97\u53e3\u53f3\u4e0a", None))
        self.label_26.setText("")
        self.label_27.setText(QCoreApplication.translate("Form", u"\u7a97\u53e3\u5de6\u4e0b", None))
        self.label_28.setText("")
        self.label_29.setText(QCoreApplication.translate("Form", u"\u7a97\u53e3\u53f3\u4e0b", None))
        self.label_30.setText("")
        self.label_31.setText(QCoreApplication.translate("Form", u"\u5750\u6807 X , Y", None))
        self.label_32.setText("")
        self.pushButton_2.setText("")
        self.pushButton_3.setText("")
        self.pushButton_4.setText("")
        self.pushButton_5.setText(QCoreApplication.translate("Form", u"\u5f3a\u5236\u7f6e\u9876", None))
        self.pushButton_6.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88\u7f6e\u9876", None))
        self.pushButton_7.setText(QCoreApplication.translate("Form", u"\u663e\u793a\u9876\u90e8", None))
        self.pushButton_8.setText(QCoreApplication.translate("Form", u"\u5f3a\u5236\u7ec8\u6b62", None))
        self.pushButton_9.setText(QCoreApplication.translate("Form", u"\u6253\u5f00\u6587\u4ef6\u6240\u5728\u4f4d\u7f6e", None))
    # retranslateUi

    def mousePressEvent(self, event: QMouseEvent):
        if event.position().y() <= 35:
            if event.button() == Qt.LeftButton:
                self.mouse_start_pt = event.globalPosition().toPoint()
                self.window_pos = self.frameGeometry().topLeft()
                self.drag = True

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drag:
            distance = event.globalPosition().toPoint() - self.mouse_start_pt
            self.move(self.window_pos + distance)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag = False

    def set_top(self):
        try:
            win32gui.SetWindowPos(self.v_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER |
                                  win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
            self.pushButton_5.setStyleSheet(u"QPushButton {background-color: #FF007F;\n"
                                            "border-radius: 2px;\n"
                                            "color: #F5F6F9;}")
        except:
            pass

    def set_down(self):
        try:
            win32gui.SetWindowPos(self.v_hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_SHOWWINDOW |
                                  win32con.SWP_NOSIZE|win32con.SWP_NOMOVE)
            self.pushButton_5.setStyleSheet(u"QPushButton {background-color: #568AF2;\n"
                                            "border-radius: 2px;\n"
                                            "color: #F5F6F9;}\n"
                                            "QPushButton::hover {background-color: #1B1E23;\n"
                                            "color: #C3CCDF;}")

        except:
            pass

    def set_top_p(self):
        try:
            win32gui.SetForegroundWindow(self.v_hwnd)
        except:
            pass

    def get_over(self):
        try:
            subprocess.Popen("taskkill /F /T /PID " + self.v_process_id, shell=True)
            subprocess.Popen("taskkill /F /T /IM " + self.v_process, shell=True)
        except:
            pass

   def open_folder(self):
        bins = self.v_p_bin.replace("\\", "/")  # 替換
        bins = os.path.split(bins)[0].replace("\\", "/")
        os.startfile(str(bins))

    def mini_button(self):
        # 最小化
        self.showMinimized()

    def close_button(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 創建一個QApplication，也就是你要開發的軟件app
    window = Window()
    window.show()
    sys.exit(app.exec())
