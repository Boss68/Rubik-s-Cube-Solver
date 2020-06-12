import sys
from PyQt5 import QtWidgets

def say_hello():
    print("Button clicked, Hello!")


if __name__ == "__main__":
    # Create a QApplication
    app = QtWidgets.QApplication([])

    # Create a button
    window=QtWidgets.QMainWindow()
    window.show()

    # Connect the button "clicked" signal to the exit() method
    # that finishes the QApplication
    app.exec_()