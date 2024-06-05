#!/usr/bin/env python

"""
Project Title:
Description:

Written by:
Last update:

"""

import controller
import sys

if __name__ == '__main__':
    try:
        app = controller.QtWidgets.QApplication([])
        window = controller.MainWindow()
        window.show()
    except:
        print("ERR!!")
        pass
    sys.exit(app.exec_())
    print("Program Closed...")