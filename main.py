#!/usr/bin/env python3

import sys

from graphics import Client
from PyQt5.QtWidgets import QApplication

from functions import task1, task2, task3, task4


if __name__ == '__main__':
    app = QApplication(sys.argv)
    grapg = Client([
        task1.Function09,
        task2.Function06,
        task3.Function01,
        task4.Function03,
    ])
    sys.exit(app.exec_())
