from PyQt5 import QtWidgets, QtCore,QtGui

class KafDrag(QtGui.QDrag):
    """class pour drag drop information"""
    def __init__(self,parent=None,mere=None,**arguments):
        super(KafDrag, self).__init__(parent)
        self.mere=mere

    def mettre(self, kobjet):
        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData,QtCore.QIODevice.WriteOnly)
        dbid_ByAr = QtCore.QByteArray()
        dbid_ByAr.setNum(kobjet.dbid, 10)
        dataStream  << dbid_ByAr
        mimeData = QtCore.QMimeData()
        mimeData.setData(kobjet.__class__.__name__, itemData)
        print(kobjet.__class__.__name__)
        self.setMimeData(mimeData)
        pixmap=kobjet.pixmap
        self.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        self.setPixmap(pixmap)
