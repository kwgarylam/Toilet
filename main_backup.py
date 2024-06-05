from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage
from GUI import Ui_MainWindow
import sys
import cv2
import time

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ### Add code here ###

        # Time
        time_str = str(time.strftime("%Y-%b-%d %H:%M"))
        self.ui.label_6.setText(time_str)

        # Video
        self.filename = 'Snapshot_' + time_str + '.png'  # Hold the image address
        self.tmp = None  # Will hold the temporary image for display
        self.fps = 0

        # Push Buttons
        self.ui.pushButton.clicked.connect(self.buttonClicked_Diagnose)
        self.ui.pushButton_6.clicked.connect(self.buttonClicked_Advise)
        self.ui.pushButton_3.clicked.connect(self.buttonClicked_Snapshot)
        self.ui.pushButton_4.clicked.connect(self.loadImage)

        # Hide Window Title
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

    ### Add functions here ###

    # Video
    def loadImage(self):
        cam = True  # True for webcam
        if cam:
            vid = cv2.VideoCapture(0)
        else:
            vid = cv2.VideoCapture(r"C:/Users/kwgarylam/PycharmProjects/toilet/video.mp4")

        cnt = 0
        frames_to_count = 20
        st = 0
        fps = 0

        while (vid.isOpened()):
            QtWidgets.QApplication.processEvents()
            img, self.image = vid.read()

            print("HIHI")
            print(type(img))
            print(img.shape)

            self.image = cv2.resize(self.image, (640, 360), interpolation=cv2.INTER_AREA)


            if cnt == frames_to_count:
                try:  # To avoid divide by 0 we put it in try except
                    print(frames_to_count / (time.time() - st), 'FPS')
                    self.fps = round(frames_to_count / (time.time() - st))

                    st = time.time()
                    cnt = 0
                except:
                    pass

            cnt += 1

            self.update()
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

    def update(self):
        """ This function will update the photo and set it to photo label.
        """
        img = self.image

        # Here we add display text to the image
        #text = 'FPS: ' + str(self.fps)

        self.setPhoto(img)

    def setPhoto(self, image):
        """ This function will take image input and resize it
            only for display purpose and convert it to QImage
            to set at the label.
        """
        self.tmp = image
        image = cv2.resize(image, (640, 360), interpolation=cv2.INTER_AREA)

        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)

        self.label_2.setPixmap(QtGui.QPixmap.fromImage(image))
        print("HERE")


    # Push Button Functions
    def buttonClicked_Diagnose(self):
        self.statusBar().showMessage("Diagnose button clicked!")

    def buttonClicked_Advise(self):
        self.statusBar().showMessage("Advise button clicked!")

    def buttonClicked_Snapshot(self):
        self.statusBar().showMessage("Snapshot button clicked!")



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())