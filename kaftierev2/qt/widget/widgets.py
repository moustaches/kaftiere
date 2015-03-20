from PyQt5 import QtCore, QtWidgets,QtWidgets

class KLabelPixmap(QtWidgets.QLabel):
    def __init__(self,parent=None,mere=None):
        super(KLabelPixmap, self).__init__(parent)
        self.parent=parent
        self.mere=mere
        self.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
        self.setLineWidth(2)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("TourneeQ"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("TourneeQ"):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat('TourneeQ'):
            itemData = event.mimeData().data('TourneeQ')
            dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.ReadOnly)
            dbid_ByAr = QtCore.QByteArray()
            dataStream >> dbid_ByAr
            dbid=dbid_ByAr.toInt(10)[0]
            tournee=self.mere.Tournee(dbid)
            self.setPixmap(tournee.pixmap)
            self.parent.objetK=tournee
            self.parent.objetKInserer()
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()


class KComboBox(QtWidgets.QComboBox):
    def __init__(self,parent=None,mere=None,comboBoxTable=None,comboBoxArg=None, kobjet=None):
        super(KComboBox, self).__init__(parent)
        self.parent=parent
        self.mere=mere
        self.comboBoxTable=comboBoxTable
        self.comboBoxArg=comboBoxArg
        for genre in self.comboBoxTable.data_arg[self.comboBoxArg]:
            if isinstance(genre,int):genre=str(genre)
            self.comboBox.addItem(genre)
        self.comboBox.setEditText(getattr(kobjet,comboBoxArg))
        self.comboBox.model().sort(0,QtCore.Qt.AscendingOrder)
        

class KComboBoxCouleur(QtWidgets.QComboBox):
    COLOR_LIST = ['#ff0000','#00ff00','#0000ff','#ffff00','#ffd700','#ffc0cb', '#ffe4c4','#fffff0',
                '#000000','#ffffff','#ee82ee', '#c0c0c0','#228b22','#a52a3a','#d2691e','#fffff0','#ffa500']  
    
    def __init__(self, parent=None):
        super(KComboBoxCouleur, self).__init__(parent)
        self.parent=parent
        self.color_list = KComboBoxCouleur.COLOR_LIST
        for color in self.color_list:
            pix=QtWidgets.QPixmap(50,30)
            pix.fill(QtWidgets.QColor(color))
            self.addItem(QtWidgets.QIcon(pix), '')
        


