
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import matplotlib.pyplot as plt
# define form pyqt5 to create a window 
class Ui_Collatz(object):
    def setupUi(self, Collatz):
        Collatz.setObjectName("Collatz")
        Collatz.resize(640, 479)
        self.centralwidget = QtWidgets.QWidget(Collatz)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(20, 20, 600, 190))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.number1 = QtWidgets.QLabel(self.centralwidget)
        self.number1.setGeometry(QtCore.QRect(20, 220, 509, 39))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.number1.setFont(font)
        self.number1.setObjectName("number1")
        self.lineNum1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineNum1.setGeometry(QtCore.QRect(20, 260, 441, 38))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineNum1.setFont(font)
        self.lineNum1.setText("")
        self.lineNum1.setPlaceholderText("")
        self.lineNum1.setObjectName("lineNum1")
        self.number2 = QtWidgets.QLabel(self.centralwidget)
        self.number2.setGeometry(QtCore.QRect(20, 300, 226, 53))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.number2.setFont(font)
        self.number2.setObjectName("number2")
        self.lineNum2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineNum2.setGeometry(QtCore.QRect(20, 350, 441, 38))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineNum2.setFont(font)
        self.lineNum2.setObjectName("lineNum2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(470, 350, 150, 38))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("color: rgb(0, 0, 255);")
        self.pushButton.setObjectName("pushButton")
        Collatz.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Collatz)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 38))
        self.menubar.setObjectName("menubar")
        Collatz.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Collatz)
        self.statusbar.setObjectName("statusbar")
        Collatz.setStatusBar(self.statusbar)
        # click button
        self.pushButton.clicked.connect(self.calculate)
        self.retranslateUi(Collatz)
        QtCore.QMetaObject.connectSlotsByName(Collatz)
    def retranslateUi(self, Collatz):
        _translate = QtCore.QCoreApplication.translate
        Collatz.setWindowTitle(_translate("Collatz", "Collatz conjucture"))
        self.textBrowser.setHtml(_translate("Collatz", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'sans-serif\'; font-size:12pt; color:#202122; background-color:#ffffff;\">The </span><span style=\" font-family:\'sans-serif\'; font-size:12pt; font-weight:600; color:#202122; background-color:#ffffff;\">Collatz conjecture</span><span style=\" font-family:\'sans-serif\'; font-size:12pt; color:#202122; background-color:#ffffff;\"> is one of the most famous unsolved problems in mathematics. The conjecture asks whether repeating two simple arithmetic operations will eventually transform every positive integer into 1. It concerns sequences of integers in which each term is obtained from the previous term as follows: if the previous term is even, the next term is one half of the previous term. If the previous term is odd, the next term is 3 times the previous term plus 1. The conjecture is that these sequences always reach 1, no matter which positive integer is chosen to start the sequence.</span></p></body></html>"))
        self.number1.setText(_translate("Collatz", "Number / begin"))
        self.number2.setText(_translate("Collatz", "Number / end"))
        self.pushButton.setText(_translate("Collatz", "Start"))
    #  show popup message   
    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Please enter a integer number")
        x=msg.exec_()
    # get input first
    def get_input_first(self):
        try:            
            num_first = int(self.lineNum1.text())
            return num_first 
        except ValueError:  # if not a number
            self.show_popup()            
            return 1
    # get input second
    def get_input_second(self):
        try:
            if self.lineNum2.text() == "":
                return None                
            num_second = int(self.lineNum2.text())
            return num_second 
        except ValueError:  # if not a number
            self.show_popup()            
            return 1    
    # calculate collatz 
    def calculate(self):
        num_first = self.get_input_first()                  
        num_second = self.get_input_second()
        if num_second == None or num_second <= num_first:
            # define constant
            x=num_first
            field_num=[num_first]
            # calculate collatz loop
            while x != 1:
                if x % 2 == 0:
                    x = x // 2
                    field_num.append(x)
                else:
                    x = 3 * x + 1
                    field_num.append(x)
            # plot a sequence graph            
            plt.title(f'Collatz sequence for x={num_first}')
            plt.grid(True)
            plt.xlabel("number in sequence")
            plt.ylabel("value Collatz")
            plt.plot(field_num) 
            plt.show()
        if num_second != None and num_second > num_first:
            # define constant
            x=num_first
            x_field=num_first
            y=num_second-num_first
            x_max=num_first
            field_x=[];field_y=[]            
            # calculate collatz loop
            while x_field<=num_first+y:
                x=x_field; x_max=x_field
                while x != 1:
                    if x % 2 == 0:
                        x = x // 2                              
                    else:
                        x = 3 * x + 1
                        if x > x_max:
                            x_max = x
                field_x.append(x_field)
                field_y.append(x_max)
                x_field +=1
            # plot a sequence graph
            plt.title(f'Maximum value for Collatz sequence: for x={num_first} ... {num_second}')
            plt.grid(True)           
            plt.xlabel("x in sequence")
            plt.ylabel("Max value Collatz")
            plt.plot(field_x,field_y) 
            plt.show()                     
        return

# create a main window
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Collatz = QtWidgets.QMainWindow()
    ui = Ui_Collatz()
    ui.setupUi(Collatz)
    Collatz.show()
    sys.exit(app.exec_())