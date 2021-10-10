import clock
import datetime
import srt_loader
import time
import threading
from PyQt5 import QtCore, QtGui, QtWidgets

class SrtPrompter(QtCore.QThread):

    update_text = QtCore.pyqtSignal(str)
    srt_end = QtCore.pyqtSignal(bool)
    kill = False

    def __init__(self,clock:clock.Clock, srt_loader:srt_loader.SrtLoader, parent=None):
        super().__init__(parent=parent)
        self.clock = clock
        self.srt_loader = srt_loader
    
    def run(self):
        while True:
            ##while srt_loader is not ready, sleep for 0.5s
            while self.srt_loader.srt_ready == False:
                time.sleep(0.5)
                if self.kill == True:
                    return
            ##Once srt_loader is ready, begin to iterate through all the srt records
            for i in range(len(self.srt_loader.records)):
                ##while this player is paused, sleep for 0.5s
                while self.clock.playing == False:
                    time.sleep(0.5)
                    if self.kill == True:
                        return
                ##if the timecode reaches to the end, stop playing and set timecode to 0
                if self.clock.timecode_ms >= self.srt_loader.srt_dur:
                    self.update_text.emit("")
                    self.clock.lock.acquire()
                    self.clock.timecode_ms = 0
                    self.clock.timecode = datetime.timedelta()
                    self.clock.playing = not self.clock.playing
                    self.clock.lock.release()
                    self.clock.tick.emit()
                    self.srt_end.emit(False)
                    pass
                try:
                    ##if the current timecode is greater than the current srt record's out,
                    ##jump to the next srt record
                    if self.clock.timecode_ms >= self.srt_loader.records[i]['out']:
                        self.update_text.emit("")
                        pass
                    else:
                        if i != 0:
                            ##if the current timecode is less than the previous srt record's out,
                            ##break the for-loop, restart the loop from the first srt record
                            if self.clock.timecode_ms < self.srt_loader.records[i-1]['out']:
                                self.update_text.emit("")
                                break
                            ##while the current timecode is greater than the previous srtRecord's out
                            ##but hasn't reach the current srt record's in, wait for 50ms
                            ##until reaching the current srt record's in
                            if self.clock.timecode_ms > self.srt_loader.records[i-1]['out'] and self.clock.timecode_ms < self.srt_loader.records[i]['in']:
                                self.update_text.emit("")
                                while self.clock.timecode_ms > self.srt_loader.records[i-1]['out'] and self.clock.timecode_ms < self.srt_loader.records[i]['in']:
                                    time.sleep(0.05)
                                    if self.kill == True:
                                        return
                                    pass
                        else:
                            ##same situation as above but dealing with i = 0
                            ##while the current timecode hasn't reached the first srt record's in
                            ##wait for 50ms until reaching the first srt record's in
                            if self.clock.timecode_ms < self.srt_loader.records[i]['in']:
                                self.update_text.emit("")
                                while self.clock.timecode_ms < self.srt_loader.records[i]['in']:
                                    self.update_text.emit("")
                                    time.sleep(0.05)
                                    if self.kill == True:
                                        return
                                    pass
                        ##if the current timecode is within the current srt record's time span,
                        ##display the current srt record's text and 
                        ##sleep for 50ms until the timecode reaches this srt record's out
                        if self.clock.timecode_ms >= self.srt_loader.records[i]['in'] and self.clock.timecode_ms <= self.srt_loader.records[i]['out']:
                            self.update_text.emit(self.srt_loader.records[i]['text'])
                            while self.clock.timecode_ms >= self.srt_loader.records[i]['in'] and self.clock.timecode_ms <= self.srt_loader.records[i]['out']:
                                time.sleep(0.05)
                                if self.kill == True:
                                    return
                                pass
                ##this error handler handles the out of index error
                ##in the case where the user open another srt file whose
                ##srt_dur is less than the previous one's
                except IndexError as e:
                    if self.kill == True:
                        return
                    break
                
                except Exception as e:
                    print(e)
                    if self.kill == True:
                        return
                    break

    def stop(self):
        self.kill = True
