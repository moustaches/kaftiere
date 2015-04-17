from PyQt5 import QtCore, QtWidgets,QtGui
from qt.modelview.model import ModelListCheckDataFiltre

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
        
class KComboBoxCheck(QtWidgets.QComboBox):
    def __init__(self,parent=None,mere=None,list_data_check=[]):
        super(KComboBoxCheck, self).__init__(parent)
        self.parent=parent
        self.mere=mere
        self.setStyle(QtWidgets.QStyleFactory.create("Gtk+"))
        modelItem=QtGui.QStandardItemModel()
        for data,check in list_data_check:
            item=QtGui.QStandardItem(data)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setData(check,QtCore.Qt.CheckStateRole)
            modelItem.appendRow(item)
        self.setModel(modelItem)
        
         
class KComboBoxCouleur(QtWidgets.QComboBox):
    """combobox de couleur"""
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
         
            
class KWidgetTableDataFiltre(QtWidgets.QWidget):
    def __init__(self, parent=None,model_data=None,model_filtre=None,data=None):
        super(KWidgetTableDataFiltre, self).__init__(parent)
        self.parent=parent
        self.header=self.parent.horizontalHeader()
        self.modelFiltre=model_filtre
        self.modelData=model_data
        self.data=data
        self.ordre=None
        self.modelListCheckDataFiltre=ModelListCheckDataFiltre(parent=self, model_filtre=self.modelFiltre)
        self.createFenetre()
        self.createconnection()
        
    @property
    def index_colonne(self):
        return self.modelData.HEADERDATA.index(self.data)

    @property
    def isActive(self):
        if not self.boutAscendant.isChecked():
            if not self.boutDescendant.isChecked():
                return False
        return True
    
    def createconnection(self):
        self.header.sectionResized.connect(self.rePlacer)
        self.parent.horizontalScrollBar().valueChanged.connect(self.rePlacer)
        self.boutAscendant.clicked.connect(self.boutAscendantClicked)
        self.boutDescendant.clicked.connect(self.boutDescendantClicked)
        self.modelListCheckDataFiltre.signalListCheckSelected.connect(self.parent.listRowsHiden)
        
    def createFenetre(self):
        self.boutAscendant= QtWidgets.QToolButton(parent=self)
        self.boutAscendant.setCheckable(True)
        self.boutAscendant.setArrowType(QtCore.Qt.DownArrow)
        self.boutDescendant= QtWidgets.QToolButton(parent=self)
        self.boutDescendant.setCheckable(True)
        self.boutDescendant.setArrowType(QtCore.Qt.UpArrow)        
        self.boutToutRien= QtWidgets.QPushButton("Tout/Rien",parent=self)
        self.boutInverser= QtWidgets.QPushButton("Inverser",parent=self)
        self.listDataFiltre = QtWidgets.QListView(parent=self)
        self.listDataFiltre.setModel(self.modelListCheckDataFiltre)
        self.ligne = QtWidgets.QFrame(parent=self)
        self.ligne.setFrameShape(QtWidgets.QFrame.HLine)
        self.ligne.setFrameShadow(QtWidgets.QFrame.Sunken)
        lay = QtWidgets.QGridLayout()
        lay.addWidget(self.boutAscendant, 0, 0, 1, 1)
        lay.addWidget(self.boutDescendant, 1, 0, 1, 1)
        lay.addWidget(self.ligne, 2, 0, 1, 1)
        lay.addWidget(self.listDataFiltre, 3, 0, 1, 1)
        lay.addWidget(self.boutInverser, 4, 0, 1, 1)
        lay.addWidget(self.boutToutRien, 5, 0, 1, 1)
        self.setLayout(lay)
        self.setWindowOpacity(0.5)
        self.rePlacer()
        self.setAutoFillBackground(True)
        self.setVisible(False)
        
    @QtCore.pyqtSlot(int)
    def scrollChanged(self,value_new):
        print(value_new)
        pos_x=self.header.sectionPosition(self.index_colonne)
        self.move(pos_x+11+value_new,self.header.size().height())  
        
    @QtCore.pyqtSlot()       
    def boutAscendantClicked(self):
        self.boutDescendant.setChecked(False)
        if self.boutAscendant.isChecked():
            self.ordre=QtCore.Qt.AscendingOrder
            self.modelFiltre.ajouterFiltreWidgetOrdre(self)
        else:
            self.ordre=None
            self.modelFiltre.retirerFiltreWidgetOrdre(self)            
        self.modelFiltre.multiSort()
            
    @QtCore.pyqtSlot()       
    def boutDescendantClicked(self):
        self.boutAscendant.setChecked(False)
        if self.boutDescendant.isChecked():
            self.ordre=QtCore.Qt.DescendingOrder
            self.modelFiltre.ajouterFiltreWidgetOrdre(self)
        else:
            self.ordre=None
            self.modelFiltre.retirerFiltreWidgetOrdre(self)            
        self.modelFiltre.multiSort()        
        
    def rePlacer(self,index_colonne=None,delta_x_old=None,delta_x_new=None):
        pos_x=self.header.sectionPosition(self.index_colonne)
        #if self.index_colonne==self.parent.model().columnCount()-1:
        delta_x=self.parent.columnWidth(self.index_colonne)
            
        pos_x_rel=pos_x-self.header.sectionPosition(self.parent.horizontalScrollBar().value())
        self.move(pos_x_rel+11,self.header.size().height())
        self.resize(delta_x-20,350)
        
    def afficherVsCacher(self):
        if not self.isVisible():self.setVisible(True)
        else:self.setVisible(False)
        
        


