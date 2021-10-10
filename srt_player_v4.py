import clock
import datetime
import multiprocessing
import re
import srt_loader
import srt_prompter
import threading
import time
import widgets
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):

    def __init__(self,MainWindow:widgets.MainWindow, app:QtWidgets.QApplication):
        self.app = app
        self.MainWindow = MainWindow
        self.clock = clock.Clock(MainWindow)
        self.clock.tick.connect(self.refresh_timecode)
        self.clock.is_playing.connect(self.is_playing)
        self.srt_loader = srt_loader.SrtLoader()
        self.srt_prompter = srt_prompter.SrtPrompter(self.clock,self.srt_loader,MainWindow)
        self.srt_prompter.update_text.connect(self.update_text)
        self.srt_prompter.srt_end.connect(self.is_playing)
        self.mousein = True
        self.new_line_pattern = r'\n'
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(622, 160)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 160))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 160))
        MainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_open = widgets.PushButton(self.centralwidget)
        self.btn_open.text = "Open srt file"
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.btn_open.setFont(font)
        self.btn_open.setObjectName("btn_open")
        self.horizontalLayout.addWidget(self.btn_open)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.lcd_h = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_h.setMinimumSize(QtCore.QSize(0, 30))
        self.lcd_h.setMaximumSize(QtCore.QSize(35, 30))
        self.lcd_h.setDigitCount(2)
        self.lcd_h.setObjectName("lcd_h")
        self.horizontalLayout.addWidget(self.lcd_h)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lcd_m = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_m.setMinimumSize(QtCore.QSize(0, 30))
        self.lcd_m.setMaximumSize(QtCore.QSize(35, 30))
        self.lcd_m.setDigitCount(2)
        self.lcd_m.setObjectName("lcd_m")
        self.horizontalLayout.addWidget(self.lcd_m)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lcd_s = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_s.setMinimumSize(QtCore.QSize(0, 30))
        self.lcd_s.setMaximumSize(QtCore.QSize(35, 30))
        self.lcd_s.setDigitCount(2)
        self.lcd_s.setProperty("intValue", 0)
        self.lcd_s.setObjectName("lcd_s")
        self.horizontalLayout.addWidget(self.lcd_s)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.btn_play = widgets.PushButton(self.centralwidget)
        self.btn_play.text = "Play"
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.btn_play.setFont(font)
        self.btn_play.setObjectName("btn_play")
        self.horizontalLayout.addWidget(self.btn_play)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.btn_leave = widgets.PushButton(self.centralwidget)
        self.btn_leave.setMaximumSize(QtCore.QSize(50, 16777215))
        self.btn_leave.text = " Exit"
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.btn_leave.setFont(font)
        self.btn_leave.setObjectName("btn_leave")
        self.horizontalLayout.addWidget(self.btn_leave)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.sld_time = QtWidgets.QSlider(self.centralwidget)
        self.sld_time.setMinimum(0)
        self.sld_time.setMaximum(100)
        self.sld_time.setProperty("value", 0)
        self.sld_time.setSliderPosition(0)
        self.sld_time.setOrientation(QtCore.Qt.Horizontal)
        self.sld_time.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sld_time.setTickInterval(10)
        self.sld_time.setObjectName("sld_time")
        self.verticalLayout.addWidget(self.sld_time)
        self.text_view = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_view.sizePolicy().hasHeightForWidth())
        self.text_view.setSizePolicy(sizePolicy)
        self.text_view.setMinimumSize(QtCore.QSize(0, 75))
        self.text_view.setMaximumSize(QtCore.QSize(16777215, 75))
        self.text_view.setReadOnly(True)
        self.text_view.setObjectName("text_view")
        self.verticalLayout.addWidget(self.text_view)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        ######
        MainWindow.mouseover.connect(self.mouseover)
        MainWindow.is_focused.connect(self.is_focused)
        self.text_view.setStyleSheet("QTextEdit{font-size:20px;}")
        self.text_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.sld_time.setTracking(True)
        self.sld_time.setSingleStep(0)
        self.sld_time.setPageStep(0)
        self.sld_time.sliderMoved.connect(self.slider_move)
        self.btn_open.clicked.connect(self.open_srt)
        self.btn_play.clicked.connect(self.play)
        self.btn_play.setDisabled(True)
        self.btn_leave.clicked.connect(self.exit)
        self.clock.start()
        self.srt_prompter.start()
        ######

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SRT Player"))
        self.text_view.setHtml(_translate("MainWindow", ""))
        self.label.setText(_translate("MainWindow", ":"))
        self.label_2.setText(_translate("MainWindow", ":"))
        self.btn_open.setText(_translate("MainWindow", "Open srt file"))
        self.btn_play.setText(_translate("MainWindow", "Play"))
        self.btn_leave.setText(_translate("MainWindow", "Eixt"))
    
    def mouseover(self, mouseover:bool):
        self.MainWindow.mouseover.disconnect()
        if mouseover != self.mousein:
            self.mousein = mouseover
            if self.mousein == False:
                self.btn_open.setVisible(False)
                self.btn_play.setVisible(False)
                self.btn_leave.setVisible(False)
                self.sld_time.setVisible(False)
                self.lcd_h.setVisible(False)
                self.lcd_m.setVisible(False)
                self.lcd_s.setVisible(False)
                self.label.setVisible(False)
                self.label_2.setVisible(False)
            if self.mousein == True:
                self.btn_open.setVisible(True)
                self.btn_play.setVisible(True)
                self.btn_leave.setVisible(True)
                self.sld_time.setVisible(True)
                self.lcd_h.setVisible(True)
                self.lcd_m.setVisible(True)
                self.lcd_s.setVisible(True)
                self.label.setVisible(True)
                self.label_2.setVisible(True)
        self.MainWindow.mouseover.connect(self.mouseover)
    
    def is_focused(self, focused:bool):
        if focused == True:
            self.clock.keyboard_listening = True
        else:
            self.clock.keyboard_listening = False
        
    def update_text(self, text:str):
        if text == '':
            self.text_view.setText(text)
        else:
            rich_text = ""
            lines = re.split(self.new_line_pattern,text)
            for line in lines:
                rich_text += """<p align="center" style="line-height:0.7;">"""+line+"""</p>"""
            self.text_view.setText(rich_text)

    def slider_move(self, sld_pos:int):
        if self.srt_loader.file_exist == True and self.srt_loader.srt_dur > 0:
            self.clock.lock.acquire()
            self.clock.timecode_ms = sld_pos*self.srt_loader.srt_dur/100
            self.clock.lock.release()
            self.refresh_timecode()
        
    def open_srt(self):
        filedialog = QtWidgets.QFileDialog()
        fileName = filedialog.getOpenFileName(self.MainWindow,caption="Open srt File", filter="srt files(*.srt)")
        if fileName[0] != "":
            self.clock.lock.acquire()
            self.clock.playing = False
            self.clock.timecode_ms = 0
            self.clock.timecode = datetime.timedelta()
            self.is_playing(False)
            code = self.srt_loader.load(fileName[0])
            if code == 0:
                msg = "Error! File doesn't exist!"
                self.update_text(msg)
            if code == 2:
                msg = "Error! Can't read this file!"
                self.update_text(msg)
            if code == 1:
                msg = "Ready!"
                self.update_text(msg)
                self.srt_ready()
            self.clock.lock.release()
            self.refresh_timecode()
    
    def srt_ready(self):
        if self.srt_loader.srt_ready == True:
            self.clock.srt_ready = True
            self.btn_play.setDisabled(False)

    def refresh_timecode(self):
        now = datetime.timedelta(milliseconds=self.clock.timecode_ms)
        hour_now = int(now/datetime.timedelta(hours=1))
        now = now - datetime.timedelta(hours=hour_now)
        minute_now = int(now/datetime.timedelta(minutes=1))
        now = now - datetime.timedelta(minutes=minute_now)
        second_now = int(now/datetime.timedelta(seconds=1))
        self.lcd_s.display(second_now)
        self.lcd_m.display(minute_now)
        self.lcd_h.display(hour_now)
        if self.srt_loader.srt_dur != 0:
            sld_pos = int(self.clock.timecode_ms/(self.srt_loader.srt_dur/100))
            self.sld_time.setValue(sld_pos)

    def play(self):
        if self.srt_loader.file_exist == True and self.srt_loader.srt_dur > 0:
            self.clock.playing = not self.clock.playing
            self.is_playing(self.clock.playing)
    
    def is_playing(self, is_playing:bool):
        if is_playing == True:
            self.btn_play.text = "Pause"
            self.btn_play.update()
        else:
            self.btn_play.text = "Play"
            self.btn_play.update()
    
    def exit(self):
        self.clock.stop()
        self.clock.wait()
        self.srt_prompter.stop()
        self.srt_prompter.wait()
        self.app.quit()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = widgets.MainWindow()
    MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)
    MainWindow.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
    MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
    ui = Ui_MainWindow(MainWindow,app)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())