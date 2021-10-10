import datetime
import time
import threading
from pynput.keyboard import Key, Listener, KeyCode
from PyQt5 import QtCore, QtGui, QtWidgets

class Clock(QtCore.QThread):

    tick = QtCore.pyqtSignal()
    is_playing = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.timecode_ms = 0
        self.timecode = datetime.timedelta()
        self.playing = False
        self.kill = False
        self.lock = threading.Lock()
        self.keyboard_listener = Listener(on_release=self.set_keyboard)
        self.keyboard_listening = True
        self.keyboard_listener.start()
        self.srt_ready = False

    def play(self):
        a = 0
        b = time.perf_counter() * 1000
        c = 0
        d = 0
        refresh_buffer = 1
        while self.kill == False:
            time.sleep(0.05)
            a = time.perf_counter() * 1000
            c = a-b
            if self.playing == True:
                self.lock.acquire()
                self.timecode_ms += c
                self.timecode_ms += d
                self.timecode = datetime.timedelta(milliseconds=self.timecode_ms)
                self.lock.release()
                if refresh_buffer >= 5:
                    self.tick.emit()
                    refresh_buffer = 0
            b = time.perf_counter() * 1000
            d = b-a
            refresh_buffer += 1
    
    def run(self):
        self.play()
    
    def stop(self):
        self.kill = True
    
    def set_keyboard(self,key:Key):
        if key == Key.pause:
            if self.srt_ready == True:
                self.lock.acquire()
                self.playing = not self.playing
                self.is_playing.emit(self.playing)
                self.lock.release()
        if self.keyboard_listening == True:
            if key == Key.tab:
                print(self.timecode)
            if key == Key.home:
                self.lock.acquire()
                self.timecode_ms = 0
                self.timecode = datetime.timedelta(milliseconds=self.timecode_ms)
                self.tick.emit()
                self.lock.release()
            if key == Key.right:
                self.lock.acquire()
                self.timecode_ms += 100
                self.timecode = datetime.timedelta(milliseconds=self.timecode_ms)
                self.tick.emit()
                self.lock.release()
            if key == Key.left:
                self.lock.acquire()
                if self.timecode_ms >= 100:
                    self.timecode_ms -= 100
                else:
                    self.timecode_ms = 0
                self.timecode = datetime.timedelta(milliseconds=self.timecode_ms)
                self.tick.emit()
                self.lock.release()
            if key == Key.up:
                self.lock.acquire()
                self.timecode_ms += 1000
                self.timecode = datetime.timedelta(milliseconds=self.timecode_ms)
                self.tick.emit()
                self.lock.release()
            if key == Key.down:
                self.lock.acquire()
                if self.timecode_ms >= 1000:
                    self.timecode_ms -= 1000
                else:
                    self.timecode_ms = 0
                self.timecode = datetime.timedelta(milliseconds=self.timecode_ms)
                self.tick.emit()
                self.lock.release()
            if key == Key.page_up:
                self.lock.acquire()
                self.timecode_ms += 5000
                self.timecode = datetime.timedelta(milliseconds=self.timecode_ms)
                self.tick.emit()
                self.lock.release()
            if key == Key.page_down:
                self.lock.acquire()
                if self.timecode_ms >= 5000:
                    self.timecode_ms -= 5000
                else:
                    self.timecode_ms = 0
                self.timecode = datetime.timedelta(milliseconds=self.timecode_ms)
                self.tick.emit()
                self.lock.release()
            if key == KeyCode.from_char('m'):
                self.lock.acquire()
                self.timecode_ms += 60000
                self.timecode = datetime.timedelta(milliseconds=self.timecode_ms)
                self.tick.emit()
                self.lock.release()
            if key == KeyCode.from_char('n'):
                self.lock.acquire()
                self.timecode_ms += 600000
                self.timecode = datetime.timedelta(milliseconds=self.timecode_ms)
                self.tick.emit()
                self.lock.release()
            if key == KeyCode.from_char('h'):
                self.lock.acquire()
                self.timecode_ms += 3600000
                self.timecode = datetime.timedelta(milliseconds=self.timecode_ms)
                self.tick.emit()
                self.lock.release()

if __name__ == "__main__":
    clock = Clock()
    clock.play()