#!/usr/bin/env python

"""
Project Title:  Smart Diagnostic System v1.0
Description:    - Main file of the system, controlling the interaction of functions and GUI
                - The system will get the video stream of the pupu and detect the type of the pupu,
                finally advice the diagnose of the health condition.
Written by:     Gary Lam
Last update:    Nov, 2023

"""

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage
from GUI import Ui_MainWindow
from screen2 import Ui_MainWindow as Ui_SecondWindow

from PyQt5.Qt import QThreadPool, QRunnable, pyqtSlot

import model
import cv2
import numpy as np
import time
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ### Add code here ###

        # Multi-threading
        self.threadpool = QThreadPool()

        # Window size
        QtWidgets.QMainWindow.resize(self, 1280, 720)

        # Hide Window Title
        #self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        ### Variables ###

        # Video
        #self.filename = 'Snapshot_' + time_str + '.png'  # Hold the image address
        self.tmp = None  # Will hold the temporary image for display
        self.fps = 0


        ### Variables ###



        # Images
        self.filename = None  # Hold the image address
        self.originalImg = np.zeros((640, 480, 3), dtype=np.uint8)  # Hold the temporary image
        self.resultImg = np.zeros((640, 480, 3), dtype=np.uint8)
        self.snapshotImg = np.zeros((320, 240, 3), dtype=np.uint8)



        # Time
        time_str = str(time.strftime("%Y-%b-%d %H:%M"))
        #time_str = "2023-11-17 14:25"
        self.ui.label_6.setText(time_str)

        # Type result
        self.type = ""
        self.dianoType = "Detecting"


        ### Widgets ###

        # Push Buttons
        #self.ui.pushButton.clicked.connect(self.buttonClicked_Diagnose)
        #self.ui.pushButton_6.clicked.connect(self.buttonClicked_Advise)
        self.ui.pushButton_3.clicked.connect(self.buttonClicked_Snapshot)
        self.ui.pushButton_4.clicked.connect(self.buttonClicked_StartVideo)
        self.ui.pushButton_7.clicked.connect(self.buttonClicked_StopVideo)
        self.ui.pushButton_2.clicked.connect(self.exitProgram)
        self.ui.pushButton_6.clicked.connect(self.changeToPage2)

        # Update images
        logoImage = cv2.imread("logo.jpg")
        logoImage = cv2.cvtColor(logoImage, cv2.COLOR_BGR2RGB)
        formatedlogoImage = formatImages(logoImage, dim=(149, 149))
        self.ui.label.setPixmap(QtGui.QPixmap.fromImage(formatedlogoImage))  # Put the image into the label

        # Update CSS
        self.ui.pushButton_4.setStyleSheet("font: 16pt ; background-color: rgb(50, 220, 0); color: white")
        self.ui.pushButton_7.setStyleSheet("font: 16pt ; background-color: rgb(255, 0, 50); color: white")
        self.ui.pushButton_3.setStyleSheet("font: 16pt ; background-color: rgb(100, 100, 150); color: white")
        self.ui.pushButton_6.setStyleSheet("font: 16pt ; background-color: rgb(100, 100, 100); color: white")
        self.ui.pushButton_2.setStyleSheet("font: 8pt ; background-color: rgb(255, 0, 50); color: white")
        self.ui.label_7.setStyleSheet("font: 16pt ; background-color: rgb(255, 255, 50); color: Black")
        self.ui.label_10.setStyleSheet("font: 16pt ; background-color: rgb(255, 255, 255); color: Black")
        self.ui.label_8.setStyleSheet("font: 16pt ; color: Black")
        ### End of init function ###


    ### Add other functions here ###


    # Push Button Functions
#    def buttonClicked_Diagnose(self):
#        self.statusBar().showMessage("Diagnose button clicked!")
#        print("Need to run the model")
#
#        #self.resultImg = model.run(self.originalImg)


    def buttonClicked_Snapshot(self):
        self.statusBar().showMessage("Snapshot button clicked!")
        self.snapshotImg = cv2.resize(self.resultImg, (320, 240))
        #self.snapshotImg = cv2.cvtColor(self.snapshotImg, cv2.COLOR_RGB2BGR)
        formatedImage = formatImages(self.snapshotImg, dim=(320, 240))
        self.ui.label_9.setPixmap(QtGui.QPixmap.fromImage(formatedImage))  # Put the image into the label
        self.dianoType = self.type
        message = "Type: " + self.dianoType
        self.ui.label_10.setText(message)




    def buttonClicked_StartVideo(self):
        self.statusBar().showMessage("Start button clicked!")
        global runable
        runable = True
        print("Start Video button is clicked!")

        try:
            ### Video stream Started ###
            print("Starting video stream ...")
            self.ui.statusbar.showMessage("Starting video stream and thread...")
            worker = myWorker()
            self.threadpool.start(worker)


        except:
            print("Error in starting the thread")
            self.threadpool.releaseThread(worker)


    def buttonClicked_StopVideo(self):
        global runable
        runable = False

        self.ui.statusbar.showMessage("Stop video stream.")

        print("Stop video stream.")

    def formatImages(self, myImage, dim):
        """ This function will take image input and resize it. The image will be converted to QImage.
        """
        myImage = cv2.resize(myImage, (dim[0], dim[1]))

        myImage = QImage(myImage, myImage.shape[1], myImage.shape[0], myImage.strides[0],
                         QImage.Format_RGB888)  # Pixmap format

        return myImage


    def updateMainScreen(self):
        self.resultImg, self.type = model.run(self.originalImg)
        self.resultImg = cv2.cvtColor(self.resultImg, cv2.COLOR_RGB2BGR)
        formatedMainImage = formatImages(self.resultImg, dim=(640, 480))
        self.ui.label_2.setPixmap(QtGui.QPixmap.fromImage(formatedMainImage)) # Put the image into the label

        if self.type == "1" or self.type == "5" or self.type == "7":
            self.ui.label_7.setStyleSheet("font: 16pt ; background-color: rgb(255, 0, 50); color: Black")
        elif self.type == "3" or self.type == "4":
            self.ui.label_7.setStyleSheet("font: 16pt ; background-color: rgb(0, 255, 50); color: Black")
        else:
            self.ui.label_7.setStyleSheet("font: 16pt ; background-color: rgb(255, 255, 50); color: Black")
        self.ui.label_8.setText(self.type)


        # cv2.waitKey(1)

    def exitProgram(self):
        print("Program terminated!")
        global runable
        runable = False # Stop the thread
        exit(app.exec_())

    def changeToPage2(self): # Advise
        widget.setCurrentWidget(window2)
        window2.updateInfo()

# Second screen
class SecondWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(SecondWindow, self).__init__()
        self.ui2 = Ui_SecondWindow()
        self.ui2.setupUi(self)

        self.ui2.label_6.setStyleSheet("font: 16pt ; background-color: rgb(255, 255, 255); color: Black")
        self.ui2.pushButton.setStyleSheet("font: 16pt ; background-color: rgb(100, 100, 100); color: white")

        ### Widgets ###

        # Push Buttons
        self.ui2.pushButton.clicked.connect(self.changeToPage1)

        # Update images
        logoImage = cv2.imread("logo.jpg")
        logoImage = cv2.cvtColor(logoImage, cv2.COLOR_BGR2RGB)
        formatedlogoImage = formatImages(logoImage, dim=(149, 149))
        self.ui2.label.setPixmap(QtGui.QPixmap.fromImage(formatedlogoImage))  # Put the image into the label

        # Update tabs
        self.ui2.tabWidget.setTabText(0," Summary")
        self.ui2.tabWidget.setTabText(1, " Daily Report")


    def changeToPage1(self):
        widget.setCurrentWidget(window)


    def updateInfo(self):
        diagType = window.dianoType
        diagDisplayType = "Type: " + diagType
        self.ui2.label_6.setText(diagDisplayType)

        print(diagType)

        if diagType == str(1):
            path = "s" + diagType + ".jpg"
            showphoto = cv2.imread(path)
            showphoto = cv2.cvtColor(showphoto, cv2.COLOR_BGR2RGB)
            win2formatedImage = formatImages(showphoto, dim=(320, 240))
            self.ui2.label_9.setPixmap(QtGui.QPixmap.fromImage(win2formatedImage))  # Put the image into the label

            self.ui2.textBrowser.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">For a client experiencing </span><span style=\" font-size:11pt; font-weight:600; text-decoration: underline; color:#ff0000;\">type 1</span><span style=\" font-size:11pt;\"> on the Bristol stool chart most frequently (representing hard, lumpy stools), here are some brief advice:</span></p>\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">1. Drink plenty of water to stay adequately hydrated.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">2. Include high-fiber foods like fruits, vegetables, and whole grains in the diet.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">3. Consider fiber supplements after consulting a healthcare professional.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">4. Engage in regular physical activity to stimulate digestion.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">5. Adopt regular toilet habits and avoid delaying bowel movements.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">6. If the issue persists or is accompanied by other symptoms, seek advice from a healthcare professional.</span></p>\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Remember, it\'s important to consult with a healthcare professional for personalized advice based on the individual\'s specific circumstances.</span></p></body></html>")


        elif diagType == str(3):
            path = "s" + diagType + ".jpg"
            showphoto = cv2.imread(path)
            showphoto = cv2.cvtColor(showphoto, cv2.COLOR_BGR2RGB)
            win2formatedImage = formatImages(showphoto, dim=(320, 240))
            self.ui2.label_9.setPixmap(QtGui.QPixmap.fromImage(win2formatedImage))  # Put the image into the label
            self.ui2.textBrowser.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">For a client experiencing </span><span style=\" font-size:11pt; font-weight:600; text-decoration: underline; color:#ff0000;\">type 3</span><span style=\" font-size:11pt;\"> on the Bristol stool chart most frequently (representing stool with cracks on the surface), here are some brief advice:</span></p>\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">1. Drink plenty of water to stay adequately hydrated.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">2. Include high-fiber foods like fruits, vegetables, and whole grains in the diet.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">3. Maintain regular meal times and avoid skipping meals.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">4. Engage in regular physical activity to stimulate digestion.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">5. Respond to the urge to have a bowel movement promptly.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">6. If the issue persists or is accompanied by other symptoms, seek advice from a healthcare professional.</span></p>\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Remember, it\'s important to consult with a healthcare professional for personalized advice based on the individual\'s specific circumstances.</span></p></body></html>")

        elif diagType == str(4):
            path = "s" + diagType + ".jpg"
            showphoto = cv2.imread(path)
            showphoto = cv2.cvtColor(showphoto, cv2.COLOR_BGR2RGB)
            win2formatedImage = formatImages(showphoto, dim=(320, 240))
            self.ui2.label_9.setPixmap(QtGui.QPixmap.fromImage(win2formatedImage))  # Put the image into the label
            self.ui2.textBrowser.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">For a client experiencing </span><span style=\" font-size:11pt; font-weight:600; text-decoration: underline; color:#ff0000;\">type 4</span><span style=\" font-size:11pt;\"> on the Bristol stool chart most frequently (representing a healthy, well-formed stool), here are some brief advice:</span></p>\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Hydration: Drink plenty of water to stay adequately hydrated.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Maintain Fiber Intake: Continue consuming a balanced diet with sufficient fiber from fruits, vegetables, and whole grains.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Regular Meals: Maintain regular meal times and avoid skipping meals.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Physical Activity: Engage in regular physical activity to stimulate digestion.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Healthy Lifestyle: Maintain a healthy lifestyle with proper sleep, stress management, and a balanced diet.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Medical Consultation: If there are any concerns or accompanying symptoms, consult with a healthcare professional.</span></p>\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Remember, it\'s important to consult with a healthcare professional for personalized advice based on the individual\'s specific circumstances.</span></p></body></html>")

        elif diagType == str(5):
            path = "s" + diagType + ".jpg"
            showphoto = cv2.imread(path)
            showphoto = cv2.cvtColor(showphoto, cv2.COLOR_BGR2RGB)
            win2formatedImage = formatImages(showphoto, dim=(320, 240))
            self.ui2.label_9.setPixmap(QtGui.QPixmap.fromImage(win2formatedImage))  # Put the image into the label
            self.ui2.textBrowser.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                "p, li { white-space: pre-wrap; }\n"
                                                "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Here are some concise tips for someone experiencing </span><span style=\" font-size:11pt; font-weight:600; text-decoration: underline; color:#ff0000;\">type 5</span><span style=\" font-size:11pt;\"> on the Bristol stool chart most frequently:</span></p>\n"
                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">1. Stay hydrated by drinking enough water.</span></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">2. Increase dietary fiber intake from fruits, vegetables, whole grains, and legumes.</span></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">3. Maintain a balanced diet with lean proteins, healthy fats, and complex carbohydrates.</span></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">4. Consider probiotic-rich foods or supplements for a healthy gut.</span></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">5. Engage in regular physical activity to stimulate digestion.</span></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">6. Manage stress through relaxation techniques.</span></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">7. Consult a healthcare professional if the issue persists or is accompanied by concerning symptoms.</span></p>\n"
                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Remember, it\'s always best to seek personalized advice from a healthcare professional based on your specific situation.</span></p></body></html>")

        elif diagType == str(7):
            path = "s" + diagType + ".jpg"
            showphoto = cv2.imread(path)
            showphoto = cv2.cvtColor(showphoto, cv2.COLOR_BGR2RGB)
            win2formatedImage = formatImages(showphoto, dim=(320, 240))
            self.ui2.label_9.setPixmap(QtGui.QPixmap.fromImage(win2formatedImage))  # Put the image into the label
            self.ui2.textBrowser.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">For a client experiencing </span><span style=\" font-size:11pt; font-weight:600; text-decoration: underline; color:#ff0000;\">type 7</span><span style=\" font-size:11pt;\"> on the Bristol stool chart most frequently (representing watery, diarrhea-like stools), here are some brief advice:</span></p>\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Hydration: Drink plenty of fluids, such as water or electrolyte-rich beverages, to stay hydrated.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">BRAT Diet: Consider following a BRAT diet, which includes bananas, rice, applesauce, and toast, to help firm up stools.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Avoid Trigger Foods: Identify and avoid any foods that may trigger or worsen diarrhea.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Probiotics: Consider taking probiotic supplements or consuming probiotic-rich foods to promote a healthy gut.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Rest and Recover: Get enough rest to allow your body to heal and recover.</span></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Medical Consultation: If diarrhea persists, is severe, or is accompanied by other concerning symptoms, seek medical advice from a healthcare professional.</span></p>\n"
                                         "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt;\"><br /></p>\n"
                                         "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">Remember, it\'s important to consult with a healthcare professional for personalized advice based on the individual\'s specific circumstances.</span></p></body></html>")

        else:
            print("Detecting")
            self.ui2.textBrowser.setText("Detecting the type ...")


def formatImages(myImage, dim):
    """ This function will take image input and resize it. The image will be converted to QImage.
    """
    myImage = cv2.resize(myImage, (dim[0], dim[1]))

    myImage = QImage(myImage, myImage.shape[1], myImage.shape[0], myImage.strides[0],
                     QImage.Format_RGB888)  # Pixmap format

    return myImage

# Multi-threading class
# Pass the I/O consuming task to the thread
class myWorker(QRunnable):
    @pyqtSlot()
    def run(self):
        global runable
        self.prev = 0
        self.interval = 0.1

        print("Thread start ... Please wait...")
        # vs = WebcamVideoStream(src=0).start()
        stream = cv2.VideoCapture(0)
        ### Main detection loop ###
        while (runable):
            time_elapsed = time.time() - self.prev

            try:

                if time_elapsed > self.interval:

                    ret, window.originalImg = stream.read()

                    time_str = str(time.strftime("%Y-%b-%d %H:%M"))
                    window.ui.label_6.setText(time_str)

                    self.prev = time.time()
                    print("time elapsed: ", round(time_elapsed, 2), " s")


                    window.updateMainScreen() # Update main screen

                    #print("#### Start Detection ####")


                else:
                    pass

            except:
                print("No image")
                pass

        print("QThread Finish")
        # vs.stop()
        stream.release()
        print("Video steam released ...")


if __name__ == '__main__':

    app = QtWidgets.QApplication([])

    window = MainWindow()
    window2 = SecondWindow()

    # Window size
    widget = QtWidgets.QStackedWidget()
    widget.setFixedSize(1280,720)
    widget.addWidget(window)
    widget.addWidget(window2)
    widget.setCurrentWidget(window)
    widget.show()

    sys.exit(app.exec_())