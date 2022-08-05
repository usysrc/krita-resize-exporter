from krita import *
from PyQt5.QtWidgets import QFileDialog

class MyExtension(Extension):

     
    def __init__(self, parent):
        # This is initialising the parent, always important when subclassing.
        super().__init__(parent)
        self.cache = {}

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("myAction", "Rexpo") 
        action.triggered.connect(self.exportDocument)        

    def exportDocument(self):
        # Get the document:
        doc = Krita.instance().activeDocument()
        # Saving a non-existent document causes crashes, so lets check for that first.
        if doc is not None:
            doc.scaleImage(int(doc.width()/10), int(doc.height()/10), int(doc.xRes()), int(doc.yRes()),"Bilinear")
            if doc.name() in self.cache:
                doc.setBatchmode(True)
                exportParameters = InfoObject()
                exportParameters.setProperty("alpha", True)
                exportParameters.setProperty("compression", 1)
                exportParameters.setProperty("indexed", False)
                doc.exportImage(self.cache[doc.name()], exportParameters)
                doc.scaleImage(int(doc.width()*10), int(doc.height()*10), int(doc.xRes()), int(doc.yRes()),"Bilinear")
                return
            # This calls up the save dialog. The save dialog returns a tuple.
            fileName = QFileDialog.getSaveFileName()[0]
            # And export the document to the fileName location.
            # InfoObject is a dictionary with specific export options, but when we make an empty one Krita will use the export defaults.
            doc.exportImage(fileName, InfoObject())
            self.cache[doc.name()] = fileName
            doc.scaleImage(int(doc.width()*10), int(doc.height()*10), int(doc.xRes()), int(doc.yRes()),"Bilinear")

# And add the extension to Krita's list of extensions:
Krita.instance().addExtension(MyExtension(Krita.instance()))
