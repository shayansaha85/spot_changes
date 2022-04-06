import sys
import platform
import paramiko
import subprocess
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient, QWindow)
from PySide2.QtWidgets import *
#from PyQt5 import QtWidgets
#from PyQt5.QtWidgets import QMainWindow,QApplication
#from PyQt5.uic import loadUi
import webbrowser

from CPUStress_Window_Dynamic import Ui_MainWindow
from CPUStress_Window_Dynamic_Service import Ui_MainWindow1
from CPUStress_Window_Dynamic_Infra import Ui_MainWindow2
from CPUStress_Window_Dynamic_CPU import Ui_MainWindow3
from CPUStress_Window_Dynamic_Loadtest import Ui_MainWindow4
from CPUStress_Window_Dynamic_Memory import Ui_MainWindow5
from CPUStress_Window_Dynamic_Applayer import Ui_MainWindow6
from cryptography.fernet import Fernet
from datetime import date
import threading
import time
#from MemoryClass import Memory


class MainScreen(QMainWindow):
    def __init__(self):
        
        QMainWindow.__init__(self)
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        
        self.expiry_verification()
        self.ui.ConnectBtn.clicked.connect(self.connect_server)

    def connect_server(self):
        server_user = self.ui.UserInp.text()
        server_name = self.ui.ServerInp.text()
        server_pwd = self.ui.PwdInp.text()
        self.Serveroptn = self.ui.Option_RBGrp.checkedButton().text()
        

        if (server_user == '' or server_name == '' or server_pwd == ''):
            #self.ui.ConnStatusTxt.setStyleSheet('color : red')
            self.ui.ConnStatusTxt.setAlignment(Qt.AlignCenter)
            self.ui.ConnStatusTxt.setStyleSheet("font-size:15pt;color : red;")
            self.ui.ConnStatusTxt.setText('Please enter Server Details')
            return

        self.conn = paramiko.SSHClient()
        self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:

            if(self.Serveroptn == "Linux"):
                print("linux")
                self.server = "Linux"
                self.conn.connect(hostname=server_name, port=22, username=server_user, password=server_pwd)
                self.ui.ConnStatusTxt.setStyleSheet('color : green')
                self.ui.ConnStatusTxt.setText('Connected')
                self.connstatus = self.ui.ConnStatusTxt.text()

                stdin, stdout, stderr = self.conn.exec_command('hostname -i')
                print(''.join(stderr.readlines()))
                if ((''.join(stderr.readlines())).strip() != ''):
                    self.ui.ConnStatusTxt.setStyleSheet('color : red')
                    self.ui.ConnStatusTxt.setText('ConnectAgain')
                    return

                #print(''.join(stdin.readlines()))
                print('connected to ', ''.join(stdout.readlines()))
                print(''.join(stderr.readlines()))
                if(self.connstatus == "Connected"):
                    provider = ServiceProvider(self.conn, self.server)
                    widget.addWidget(provider)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            
            elif(self.Serveroptn == "Windows"):
                print("windows")
                self.server = "Windows"
                print(server_name)
                print(server_user)
                print(server_pwd)
                #self.conn.connect(hostname=server_name, port=22, username=server_user, password=server_pwd)
                self.conn.connect(hostname=server_name, username=server_user, password=server_pwd)
                self.ui.ConnStatusTxt.setStyleSheet('color : green')
                self.ui.ConnStatusTxt.setText('Connected')
                self.connstatus = self.ui.ConnStatusTxt.text()

                stdin, stdout, stderr = self.conn.exec_command('hostname')
                print(''.join(stderr.readlines()))
                if ((''.join(stderr.readlines())).strip() != ''):
                    self.ui.ConnStatusTxt.setStyleSheet('color : red')
                    self.ui.ConnStatusTxt.setText('ConnectAgain')
                    return

                #print(''.join(stdin.readlines()))
                print('connected to ', ''.join(stdout.readlines()))
                print(''.join(stderr.readlines()))
                if(self.connstatus == "Connected"):
                    print("yes")
                    provider = ServiceProvider(self.conn,self.server)
                    widget.addWidget(provider)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                
        except Exception as e:
            self.ui.ConnStatusTxt.setAlignment(Qt.AlignCenter)
            self.ui.ConnStatusTxt.setText('Connection Refused')
            print(e)
            return
    
    

    def expiry_verification(self):
        self.app_key = b'z4WgegchrnsyRaKJXWg4sN9iaqEvaVjWjfZSI2gH5jE='
        self.crypto_fer = Fernet(self.app_key)

        with open('Licence.key', 'rb') as f:
            self.enc_code = f.read()
        
        #print(self.enc_code)
        self.dec_code = str(self.crypto_fer.decrypt(self.enc_code), 'utf-8')
        #print(self.dec_code)
        self.dec_code = self.dec_code.split('-')
        #print(self.dec_code)
        self.exp_date = date(year=int(self.dec_code[0]), month=int(self.dec_code[1]), day=int(self.dec_code[2]))
        self.curr_date = date.today()

        if(self.curr_date > self.exp_date):
            self.exp_msg = QMessageBox()
            self.exp_msg.setIcon(QMessageBox.Critical)
            self.exp_msg.setText('Your Licence has been Expired')
            self.exp_msg.setWindowTitle('Application Expiration')
            self.exp_msg.setStandardButtons(QMessageBox.Ok)
            self.exp_msg.buttonClicked.connect(lambda: sys.exit())
            self.exp_msg.show()
            print('Exiting....')
        else:
            self.show()
            
           


class ServiceProvider(QMainWindow):
    def __init__(self, conn, server):
        QMainWindow.__init__(self)
        self.conn = conn
        self.server = server
        self.ui1 = Ui_MainWindow1()
        self.ui1.setupUi1(self)
        self.ui1.Infrabtn.clicked.connect(self.gotoinfralayer)
        self.ui1.applayerbtn.clicked.connect(self.gotoapplayer)
        

    def gotoinfralayer(self):
        infra = InfraLayer(self.conn, self.server)
        widget.addWidget(infra)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoapplayer(self):
        app = AppLayer(self.conn, self.server)
        widget.addWidget(app)
        widget.setCurrentIndex(widget.currentIndex()+1)


class InfraLayer(QMainWindow):
    def __init__(self, conn, server):
        QMainWindow.__init__(self)
        self.conn = conn
        self.server = server
        self.ui2 = Ui_MainWindow2()
        self.ui2.setupUi2(self)
        self.ui2.Cpustressbutton.clicked.connect(self.gotocpustress)
        self.ui2.Loadtest.clicked.connect(self.gotoloadtest)
        self.ui2.infrabackbutton.clicked.connect(self.gotobackservice)
        self.ui2.monitorbtn.clicked.connect(self.grafanamonitorthread)
        self.ui2.MemStress_pushButton.clicked.connect(self.gotoMemorystress)

    def gotocpustress(self):
        cpu = Cpu(self.conn, self.server)
        widget.addWidget(cpu)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoMemorystress(self):
        mem = Memory(self.conn, self.server)
        widget.addWidget(mem)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoloadtest(self):
        load = Loadtest(self.conn, self.server)
        widget.addWidget(load)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotobackservice(self):
        provider = ServiceProvider(self.conn, self.server)
        widget.addWidget(provider)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def grafanamonitor(self):
        url = 'http://localhost:3000/d/000000127/telegraf-system-dashboard?orgId=1&refresh=1m&from=now-5m&to=now'
        #chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        #webbrowser.get(chrome_path).open(url)
        webbrowser.get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(url)

    def grafanamonitorthread(self):
        trdgrafana = threading.Thread(target=self.grafanamonitor)
        trdgrafana.start()

class AppLayer(QMainWindow):
    def __init__(self, conn, server):
        QMainWindow.__init__(self)
        self.conn = conn
        self.server = server
        self.ui6 = Ui_MainWindow6()
        self.ui6.setupUi6(self)
        self.ui6.appbackbtn.clicked.connect(self.gotobackservice)
        self.ui6.stackedWidget.setCurrentWidget(self.ui6.kill_page)
        self.ui6.kill.clicked.connect(lambda: self.ui6.stackedWidget.setCurrentWidget(self.ui6.kill_page))
        self.ui6.mq.clicked.connect(lambda: self.ui6.stackedWidget.setCurrentWidget(self.ui6.mq_page))
        self.ui6.exception.clicked.connect(lambda: self.ui6.stackedWidget.setCurrentWidget(self.ui6.exeception_page))
        self.ui6.jdbc.clicked.connect(lambda: self.ui6.stackedWidget.setCurrentWidget(self.ui6.tomcat_page))


    def gotobackservice(self):
        provider = ServiceProvider(self.conn, self.server)
        widget.addWidget(provider)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def httpaddlayout(self):
        self.ui6.stackedWidget.setCurrentWidget(self)
        wid = QtWidgets.QWidget(self)
        #self.setCentralWidget(wid)
        layout = QtWidgets.QVBoxLayout()
        Button1 = QPushButton("1")
        layout.addWidget(Button1)
        wid.setLayout(layout)
        self.show()
        
    
    def display(self,i):
      self.Stack.setCurrentIndex(i)

        
        

        
class Cpu(QMainWindow):
    def __init__(self, conn, server):
        QMainWindow.__init__(self)
        self.conn = conn
        self.server = server
        self.ui3 = Ui_MainWindow3()
        self.ui3.setupUi3(self)
        self.ui3.cpubackbtn.clicked.connect(self.gobackinfra)
        #self.ui3.pushButton.clicked.connect(self.execute_stress)
        self.ui3.pushButton.clicked.connect(self.cputhread)

    
    def gobackinfra(self):  
        infra = InfraLayer(self.conn, self.server)
        widget.addWidget(infra)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def execute_stress(self):
        try:
            if(self.server == "Linux"):
                self.ui3.CPUSExecStatusTxt.setAlignment(Qt.AlignCenter)
                self.ui3.CPUSExecStatusTxt.setStyleSheet('font-size:15pt;color : blue')
                self.ui3.CPUSExecStatusTxt.setText('Executing...')
                self.ui3.CPUSExecStatusTxt.repaint()
                self.selected_CPUper = self.ui3.CPUper_RBGrp.checkedButton().text()
                stdin, stdout, stderr = self.conn.exec_command('nproc')
            
                self.CPU_cores = stdout.read().decode().strip()
                print(self.CPU_cores)

                if(self.selected_CPUper == "100%"):
                    self.CPU_cores = self.CPU_cores
                    print(self.CPU_cores)
                elif(self.selected_CPUper == "75%"):
                    self.CPU_cores = (int(self.CPU_cores)*3)/4
                    print(self.CPU_cores)
                elif(self.selected_CPUper == "50%"):
                    self.CPU_cores = (int(self.CPU_cores))/2
                    print(self.CPU_cores)
                elif(self.selected_CPUper == "25%"):
                    self.CPU_cores = (int(self.CPU_cores))/4
                    print(self.CPU_cores)
                
                self.CPU_duration = self.ui3.spinBox.text()
                
                stdin, stdout, stderr = self.conn.exec_command('seq {cores} | xargs -P0 -n1 timeout {duration} md5sum /dev/zero'.format(cores = self.CPU_cores, duration = self.CPU_duration))

            elif(self.server == "Windows"):
                self.ui3.CPUSExecStatusTxt.setAlignment(Qt.AlignCenter)
                self.ui3.CPUSExecStatusTxt.setStyleSheet('font-size:15pt;color : blue')
                self.ui3.CPUSExecStatusTxt.setText('Executing...')
                self.ui3.CPUSExecStatusTxt.repaint()
                self.selected_CPUper = self.ui3.CPUper_RBGrp.checkedButton().text()
            
                self.CPU_cores = None
                if(self.selected_CPUper == "100%"):
                    self.CPU_cores = 4
                elif(self.selected_CPUper == "75%"):
                    self.CPU_cores = 3
                elif(self.selected_CPUper == "50%"):
                    self.CPU_cores = 2
                elif(self.selected_CPUper == "25%"):
                    self.CPU_cores = 1
                
                self.CPU_duration = self.ui3.spinBox.text()
                
                #stdin, stdout, stderr = self.conn.exec_command('seq {cores} | xargs -P0 -n1 timeout {duration} md5sum /dev/zero'.format(cores = self.CPU_cores, duration = self.CPU_duration))
                p = subprocess.Popen('powershell.exe -ExecutionPolicy RemoteSigned -file "cpu.ps1"', stdout=sys.stdout)
                p.communicate()

        except Exception as e:
            print(e)
            self.ui3.CPUSExecStatusTxt.setAlignment(Qt.AlignCenter)
            self.ui3.CPUSExecStatusTxt.setStyleSheet("font-size:15pt;color : red")
            #self.ui3.CPUSExecStatusTxt.setStyleSheet('color : red')
            self.ui3.CPUSExecStatusTxt.setText('Not Executed')
            self.ui3.CPUSExecStatusTxt.repaint()
            return
        #print('---',''.join(stderr.readlines()),'---')

        #print(len(''.join(stderr.readlines())))

        #if(len(''.join(stderr.readlines())) > 0):
        if ((''.join(stderr.readlines())).strip() != ''):
            self.ui3.CPUSExecStatusTxt.setAlignment(Qt.AlignCenter)
            self.ui3.CPUSExecStatusTxt.setStyleSheet("font-size:15pt;color : red")
            self.ui3.CPUSExecStatusTxt.setText('Not Executed')
        else:
            self.ui3.CPUSExecStatusTxt.setAlignment(Qt.AlignCenter)
            self.ui3.CPUSExecStatusTxt.setStyleSheet("font-size:15pt;color : green")
            self.ui3.CPUSExecStatusTxt.setText('Executed')

    def cputhread(self):
        trd = threading.Thread(target=self.execute_stress)
        trd.start()

class Memory(QMainWindow):
    def __init__(self, conn, server):
        QMainWindow.__init__(self)
        self.conn = conn
        self.server = server
        self.ui5 = Ui_MainWindow5()
        self.ui5.setupUi5(self)
        self.ui5.Memorybackbtn.clicked.connect(self.gobackinfra)
        self.ui5.MemoryExecute.clicked.connect(self.Memorythread)

    
    def gobackinfra(self):  
        infra = InfraLayer(self.conn, self.server)
        widget.addWidget(infra)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def execute_Memorystress(self):
        try:

            self.ui5.MemoryExecStatusTxt.setAlignment(Qt.AlignCenter)
            self.ui5.MemoryExecStatusTxt.setStyleSheet('font-size:15pt;color : blue')
            self.ui5.MemoryExecStatusTxt.setText('Executing...')
            self.ui5.MemoryExecStatusTxt.repaint()
            self.Memtoburn = self.ui5.Memoryburn.text()
            self.Memory_duration = self.ui5.MemorySpin.text()
            t_end = time.time() + 1 * int(self.Memory_duration)
            stdin, stdout, stderr = self.conn.exec_command('dd if=/dev/zero bs={MemoryMB}M of=/dev/null'.format(MemoryMB = self.Memtoburn))
            self.Memorycmd = ('dd if=/dev/zero bs={MemoryMB}M of=/dev/null'.format(MemoryMB = self.Memtoburn))
            self.Memorycmd1 = "'"+self.Memorycmd+"'"
            self.pscmd = ('/bin/ps -C {Memorycmd2} -o pid='.format(Memorycmd2 = self.Memorycmd1))
            stdin, stdout, stderr = self.conn.exec_command('/bin/ps -C {Memorycmd2} -o pid='.format(Memorycmd2 = self.Memorycmd1))
            self.processid = stdout.read().decode().strip()
            print(self.processid)
            while True:
                if time.time() > t_end:
                    stdin, stdout, stderr = self.conn.exec_command('kill {processid1}'.format(processid1 = self.processid))
                    print('done')
                    self.ui5.MemoryExecStatusTxt.setAlignment(Qt.AlignCenter)
                    self.ui5.MemoryExecStatusTxt.setStyleSheet("font-size:15pt;color : green")
                    self.ui5.MemoryExecStatusTxt.setText('Executed')
                    return

        except Exception as e:
            print(e)
            self.ui5.MemoryExecStatusTxt.setAlignment(Qt.AlignCenter)
            self.ui5.MemoryExecStatusTxt.setStyleSheet("font-size:15pt;color : red")
            self.ui5.MemoryExecStatusTxt.setText('Not Executed')
            self.ui5.MemoryExecStatusTxt.repaint()
            return
            
    def Memorythread(self):
        trd = threading.Thread(target=self.execute_Memorystress)
        trd.start()

class Loadtest(QMainWindow):
    def __init__(self,conn, server):
        self.conn = conn
        self.server = server
        QMainWindow.__init__(self)
        self.ui4 = Ui_MainWindow4()
        self.ui4.setupUi4(self) 
        self.ui4.jmeterbackbtn.clicked.connect(self.gobackinfra1)
        self.ui4.JMBatchFileBrowseBtn.clicked.connect(lambda: self.browse_files(set_text_ele= self.ui4.JMBatchFileLocInp, caption= self.ui4.JMBatchLblTxt.text(), filetype= 'Jmeter batch file(*.bat)'))
        self.ui4.JMScriptFileBrowseBtn.clicked.connect(lambda: self.browse_files(set_text_ele= self.ui4.JMScriptFileLocInp, caption= self.ui4.JMScriptLblTxt.text(), filetype= 'Jmeter Script (*.jmx)'))
        self.ui4.JMOputFolderBrowseBtn.clicked.connect(lambda: self.browse_folder(set_text_ele= self.ui4.JMOputFolderLocInp, caption= self.ui4.JMOputFileLblTxt.text()))
        """ self.ui4.JMExecBtn.clicked.connect(lambda: self.run_Jmeter(
            JM_batch=self.ui4.JMBatchFileLocInp.text(),
            JM_script=self.ui4.JMScriptFileLocInp.text(),
            JM_res=self.ui4.JMOputFolderLocInp.text() +'''/'''+ self.ui4.JMOputFileInp.text()
        )) """
        
        self.ui4.JMExecBtn.clicked.connect(self.executejmeterthread)
    
    def browse_files(self, set_text_ele, filetype, caption='Open File'):
        fname = QFileDialog.getOpenFileName(self, caption, '', filetype)
        set_text_ele.setText(str(fname[0]))

    def browse_folder(self, set_text_ele, caption='Open Folder'):
        fname = QFileDialog.getExistingDirectory(self, caption=caption)
        set_text_ele.setText(str(fname))

    #def run_Jmeter(self, JM_batch, JM_script, JM_res):
    def run_Jmeter(self):
        JM_batch=self.ui4.JMBatchFileLocInp.text()
        JM_script=self.ui4.JMScriptFileLocInp.text()
        JM_res=self.ui4.JMOputFolderLocInp.text() +'''/'''+ self.ui4.JMOputFileInp.text()
        print(JM_res)
        print(JM_batch)
        print(JM_script)
        self.ui4.JMExecStatusTxt.setAlignment(Qt.AlignCenter)
        self.ui4.JMExecStatusTxt.setStyleSheet('font-size:15pt;color : blue')
        self.ui4.JMExecStatusTxt.setText('Executing...')
        #self.ui4.JMExecStatusTxt.repaint()
        try:
            process = subprocess.Popen('''"{JM_batch}" -n -t "{JM_script}" -l "{JM_res}"'''.format(JM_batch = JM_batch, JM_script = JM_script, JM_res = JM_res), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            for out in iter(process.stdout.readline, b''):
                sys.stdout.write(str(out, 'utf-8'))

        except Exception as e:
            print(e)
            self.ui4.JMExecStatusTxt.setAlignment(Qt.AlignCenter)
            self.ui4.JMExecStatusTxt.setStyleSheet('font-size:15pt;color : red')
            self.ui4.JMExecStatusTxt.setText('Not Executed')
            self.ui4.JMExecStatusTxt.repaint()
            return
        self.ui4.JMExecStatusTxt.setAlignment(Qt.AlignCenter)
        self.ui4.JMExecStatusTxt.setStyleSheet('font-size:15pt;color : green')
        self.ui4.JMExecStatusTxt.setText('Executed')
        self.ui4.JMExecStatusTxt.repaint()

    def gobackinfra1(self):
        infra = InfraLayer(self.conn, self.server)
        widget.addWidget(infra)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def executejmeterthread(self):
        trd1 = threading.Thread(target=self.run_Jmeter, name="Thread #1", daemon=True)
        trd1.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainScreen()
    #window.show()
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(window)
    widget.setFixedWidth(800)
    widget.setFixedHeight(600)
    widget.show()
    sys.exit(app.exec_())