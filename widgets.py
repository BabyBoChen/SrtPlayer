import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QMainWindow):

    mouseover = QtCore.pyqtSignal(bool)
    is_focused = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None, flags=QtCore.Qt.WindowFlags()):
        super().__init__(parent=parent, flags=flags)
        self.opacity = 1
        self.setMouseTracking(True)
        self.is_clicked = False
        self.is_clicked_pos = [0,0]
        self.pos = self.geometry()
    
    def event(self, QEvent:QtCore.QEvent):
        if QEvent.type() == 129: #mouseover = 129
            self.mouseover.emit(True)
            self.opacity = 1
            self.update()
            if self.is_clicked == True:
                x_prime = QtGui.QCursor.pos().x() - self.is_clicked_pos[0] + self.pos.left()
                y_prime = QtGui.QCursor.pos().y() - self.is_clicked_pos[1] + self.pos.top()
                self.setGeometry(x_prime,y_prime,self.pos.width(),self.pos.height())
                pass
        if QEvent.type() == 128: #mouseleave = 128
            self.mouseover.emit(False)
            self.opacity = 0
            self.update()
        if QEvent.type() == 2: #mouse_leftkey_pressed = 2
            self.is_clicked = True
            self.is_clicked_pos[0] = QtGui.QCursor.pos().x()
            self.is_clicked_pos[1] = QtGui.QCursor.pos().y()
            self.pos = self.geometry()
        if QEvent.type() == 3: #mouse_leftkey_release = 3
            self.is_clicked = False
        if QEvent.type() == 99: #window_focus_change = 99
            self.is_focused.emit(self.isActiveWindow())
            pass
        return super().event(QEvent)
    
    def paintEvent(self, event=None):
        painter = QtGui.QPainter(self)
        painter.setOpacity(self.opacity)
        painter.setBrush(QtCore.Qt.white)
        painter.setPen(QtGui.QPen(QtCore.Qt.white))
        painter.drawRect(self.rect())

class PushButton(QtWidgets.QPushButton):

    def __init__(self,parent=None):
        super().__init__(parent=parent)
        self.text = ""
        self.opacity = 1
        self.brush_color = QtCore.Qt.white
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(12)
        self.setFont(font)
    
    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setOpacity(self.opacity)
        painter.setBrush(self.brush_color)
        painter.setPen(QtGui.QPen(QtGui.QColor(200,200,200,255)))
        width = self.rect().width()-1
        height = self.rect().height()-1
        new_rect = QtCore.QRect(0,0,width,height)
        painter.drawRoundedRect(new_rect,2,2)
        if self.isEnabled() == False:
            painter.setPen(QtGui.QPen(QtGui.QColor(200,200,200,255)))
        else:
            painter.setPen(QtGui.QPen(QtGui.QColor(0,0,0,255)))
        painter.setBrush(QtCore.Qt.black)
        btn_text = QtGui.QStaticText(self.text)
        left = int((width-1-btn_text.size().width())/2)-1
        top = int((height-1-btn_text.size().height())/2)
        painter.drawStaticText(QtCore.QPoint(left,top),btn_text)
    
    def event(self, QEvent):
        if QEvent.type() == 129 and self.isEnabled() == True: #mouseover = 129
            self.brush_color = QtGui.QColor(168, 211, 241,127)
        if QEvent.type() == 128: #mouseleave = 128
            self.brush_color = QtCore.Qt.white
        return super().event(QEvent)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pushbutton = PushButton()
    pushbutton.show()
    sys.exit(app.exec_())