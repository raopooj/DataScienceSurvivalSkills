import sys # System-specific parameters and functions

from PyQt5.QtWidgets import (QApplication, QPushButton, QWidget,QMainWindow,QAction,
                             QFileDialog, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox)
from PyQt5 import QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import json
import imageio.v2 as io

# Preparing the environment for the image:

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText('Drag and drop the image(*.png,*jpg) here')



class Interface(QWidget):
    def __init__(self):
        super().__init__() #super() is used to refer the superclass from the subclass.
        self.setWindowTitle("Pooja_Rao")

        # Initialize a QGridLayout
        self.l = QGridLayout(self)
        # Create an ImageView inside the central widget
        self.imv = pg.ImageView()
        self.l.addWidget(self.imv)



#Let's define our widget
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        ## Run the function to set defaults
        self.set_defaults()
        self.setAcceptDrops(True)
        self.setWindowIcon(QtGui.QIcon('C:\\Users\\nadine\\OneDrive\\FAU\\WS23-24\\DSSS\\Exercises\\Exercise 10\\dsss.ico'))

        # Creating a CentralWidget
        w = QWidget(self)
        self.setCentralWidget(w) # QMainWindow takes ownership of the widget pointer and deletes it at the appropriate time.
        self.mainLayout = QVBoxLayout()
        w.setLayout(self.mainLayout)

        # setting the minimum size
        self.setMinimumSize(250, 300) #images of 256x256+space for buttons
        self.setMaximumSize(1920,1080)

        ### ------ add the drag and drop image label -----###
        self.dragdroplabel = QLabel("Drag and drop the image(*.png,*jpg) here", self)
        self.dragdroplabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.dragdroplabel)


        #self.dragimage = ImageLabel()
        #self.mainLayout.addWidget(self.dragimage)

        ####------- IMAGE WIDGET -------####
        self.imageViewer = Interface()
        self.mainLayout.addWidget(self.imageViewer)

        ####------- Make the layout look better -------####
        self.mainLayout.addStretch(1)

        # Create a label to display messages
        self.message_label = QLabel("Press Ctrl+S to save the image", self)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.addWidget(self.message_label)



 
    def set_defaults(self): ## Set default values for the application
        # Settings for the window:
        self.status = self.statusBar()
        self.showNormal() # Shows the window maximized
        # self.setAcceptDrops(True) #enables drop events

        # Initialize the variable containing the image 
        self.im = None

        ## Set window options (width, height)
        width = 500
        height = 500
        self.resize(width, height)

        ## Change the window title depending on the default language
        self.setWindowTitle("Pooja Rao")

        #####-------add the menu bar----#
        self.menubar = self.menuBar()
        open_image_action = QAction('Open', self)
        open_image_action.triggered.connect(self.load_from_dialog)
        self.menuBar().addAction(open_image_action)

        save_image_action = QAction('Save',self)
        save_image_action.triggered.connect(self.save)
        save_image_action.setShortcut(QKeySequence("Ctrl+S"))
        self.menuBar().addAction(save_image_action)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)

            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        self.show_image(file_path)

    ####----CLEAR WIDGETS----#### Think a way to clear properly!
    ### Clear items inside a Layout
    def clearItems(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clearItems(item.layout())
    
    ### Clear layouts inside layouts 
    def clearLayouts(self, layout):
        self.clearItems(layout)
        for i in reversed (range(layout.count())):
            layout_item = layout.itemAt(i)
            self.clearItems(layout_item.layout())
            layout.removeItem(layout_item)

    ## Function to load an image from the file explorer
    ##input : can only be .png, .jpg
    ## returns : filepath of the image
    def load_from_dialog(self):
        fn, _ = QFileDialog.getOpenFileName(filter="*.png *.jpg")
        self.show_image(fn)

    def show_image(self,fn):
        if fn:
            self.status.showMessage(fn)
            self.im = io.imread(fn)
            self.imageViewer.imv.setImage(self.im)
            QMessageBox.information(self, 
            "file loaded", 
            "Image succesfully loaded!")
        else: 
            QMessageBox.critical(self, 
            "Meaningful error", 
            "Something went wrong!")

    def save(self):
        # selecting file path
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        # if file path is blank return back
        if filePath:
            try :
                io.imwrite(filePath,self.im)
                self.showdialog(False)
            except :
                self.showdialog(True)
                return

        else:
            self.showdialog(True)
            return



    ## We need to give some feedback to the user, don't we? :)
    def showdialog(self, flag):
            msg = QMessageBox()
            if flag:
                msg.setIcon(QMessageBox.Critical)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Retry)
                msg.setWindowTitle("Error")
                msg.setText("Error trying to save the image!")
                msg.setInformativeText("Image could not be saved")
                returnValue = msg.exec()
            else:
                msg.setWindowTitle("Info")
                msg.setText("Image was saved succesfully!")
                msg.setIcon(QMessageBox.Information)
                msg.setStandardButtons(QMessageBox.Ok)
                returnValue = msg.exec()

def main():

    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()