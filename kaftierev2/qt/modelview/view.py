'''
Created on 8 mai 2013------------------------------------

@author: moustache
'''
from PyQt5 import QtCore, QtWidgets,QtGui
from qt.format import KafDrag
from qt.modelview.delegate import GridTourneeDelegate,ComboBoxDelegate,ComboBoxGeoResultDelegate,LineEditDelegate

class TableView(QtWidgets.QTableView):
    """Super class des Tableview"""
    def __init__(self,parent=None,mere=None,**arguments):
        super(TableView, self).__init__(parent)
        self.mere=mere
        self.parent=parent
        self.setDragEnabled(True)#accepte de drager ces items
        self.setAcceptDrops(True)#accepte de drooper les items
        self.setDropIndicatorShown(True)#indique quand item est draggind and dropping
        self.setFont(self.parent.FONT['table'])
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        #self.horizontalHeader().setStretchLastSection(True)
        self._initNext(**arguments)
    
    def _initNext(self,**arguments):
        pass
#        self.ResizeToContents()
   
class ViewClient(TableView):
    """Tableau gestion du client dans la fenetre Client/Contrat/Pedaleur"""
    def _initNext(self):
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)


class ViewContrat(TableView):
    """Tableau gestion du contrat dans la fenetre Client/Contrat/Pedaleur"""
    def _initNext(self):
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("item-contrat"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("item-contrat"):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

#    def dropEvent(self, event):
#        if event.mimeData().hasFormat('item-contrat'):
#            itemData = event.mimeData().data('item-contrat')
#            dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.ReadOnly)
#            pixmap = QtWidgets.QPixmap()
#            dbid=QtCore.QByteArray()
#            dataStream >> pixmap >> dbid
#            ind=self.indexAt(event.pos())      
#            self.model().setIco(pixmap=pixmap,origine=dbid,new_ind=ind)
#            event.setDropAction(QtCore.Qt.MoveAction)
#            event.accept()
#        else:
#            event.ignore()

    def startDrag(self, supportedActions):
        contrat = self.model().data(self.currentIndex(),QtCore.Qt.UserRole)
        drag=KafDrag(parent=self,mere=self.mere)
        drag.mettre(contrat)
        if drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            pass
#            self.model().removeIco(origine=self.currentIndex())  


class ViewPedaleur(TableView):
    """Tableau gestion du pedaleur dans la fenetre Client/Contrat/Pedaleur"""
    def _initNext(self):
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    def startDrag(self, supportedActions):
        objetK = self.model().data(self.currentIndex(),QtCore.Qt.UserRole)
        drag=KafDrag(parent=self,mere=self.mere)
        drag.mettre(objetK)
        if drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            pass

class ViewTournee(TableView):
    """Tableau gestion tournee dans la fenetre Tournee/Parcours"""
    def _initNext(self):
        self.setShowGrid(False)
        grid_delegate=GridTourneeDelegate(parent=self)
        self.setItemDelegate(grid_delegate)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.horizontalHeader().setStretchLastSection(True)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("ContratQ") or event.mimeData().hasFormat("TourneeQ"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("ContratQ") or event.mimeData().hasFormat("TourneeQ"):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat('ContratQ'):
            itemData = event.mimeData().data('ContratQ')
            dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.ReadOnly)
            dbid_ByAr = QtCore.QByteArray()
            dataStream >> dbid_ByAr
            dbid=dbid_ByAr.toInt(10)[0]
            contrat=self.mere.Contrat(dbid)
            index_cible=self.indexAt(event.pos())
            tournee_cible=self.model().data(index=self.model().createIndex(index_cible.row(), 0), role=QtCore.Qt.UserRole)
            if contrat.tournee != tournee_cible:
                self.model().setData(index=index_cible, value=contrat, role=QtCore.Qt.UserRole)
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore() 

    def startDrag(self, supportedActions):
        objetK = self.model().data(self.currentIndex(),QtCore.Qt.UserRole)
        drag=KafDrag(parent=self,mere=self.mere)
        drag.mettre(objetK)
        if drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            self.model().setData(index=drag.source().currentIndex(), value=objetK, role=QtCore.Qt.UserRole+1) #pass ???
     
     
class ViewParcours(TableView):
    """Tableau gestion du parcours dans la fenetre Tournée/Parcours"""
    def _initNext(self):
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectColumns)     
     
    def dropEvent(self, event):
        if event.mimeData().hasFormat('PedaleurQ'):
            itemData = event.mimeData().data('PedaleurQ')
            dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.ReadOnly)
            dbid_ByAr = QtCore.QByteArray()
            dataStream >> dbid_ByAr
            dbid=dbid_ByAr.toInt(10)[0]
            pedaleur=self.mere.Pedaleur(dbid)
            index_cible=self.indexAt(event.pos())
            self.model().setData(index=index_cible, value=pedaleur, role=QtCore.Qt.UserRole)
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore() 

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("PedaleurQ"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("PedaleurQ"):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()


class ViewLieuDB(TableView):
    def _initNext(self):
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        genre_delegate=ComboBoxDelegate(parent=self,comboBoxTable=self.mere.genreslieux_tb,comboBoxArg='genre')
        self.setItemDelegateForColumn(3,genre_delegate)


class ViewLieuEditAdresse(TableView):
    def _initNext(self):
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        cp_delegate=ComboBoxDelegate(parent=self,comboBoxTable=self.mere.cpvilles_tb,comboBoxArg='cp')
        res_geo_delegate=ComboBoxGeoResultDelegate(parent=self)
        ville_delegate=ComboBoxDelegate(parent=self,comboBoxTable=self.mere.cpvilles_tb,comboBoxArg='ville')
        etat_delegate=ComboBoxDelegate(parent=self,comboBoxTable=self.mere.etatslieux_tb,comboBoxArg='etat')
        self.setItemDelegateForColumn(1,etat_delegate)
        self.setItemDelegateForColumn(4,cp_delegate)
        self.setItemDelegateForColumn(5,ville_delegate)
        self.setItemDelegateForColumn(9,res_geo_delegate)
  
class ViewMatchingLieu(TableView):
    def _initNext(self):
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

class ViewImportListing(TableView):
    def _initNext(self):
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        cp_delegate=ComboBoxDelegate(parent=self,comboBoxTable=self.mere.cpvilles_tb,comboBoxArg='cp')
        res_geo_delegate=ComboBoxGeoResultDelegate(parent=self)
        ville_delegate=ComboBoxDelegate(parent=self,comboBoxTable=self.mere.cpvilles_tb,comboBoxArg='ville')
        line_edit=LineEditDelegate(parent=self)
        self.setItemDelegateForColumn(7,line_edit)
        self.setItemDelegateForColumn(8,cp_delegate)
        self.setItemDelegateForColumn(9,ville_delegate)
        self.setItemDelegateForColumn(13,res_geo_delegate)
        
class ViewMatchingListing(TableView):
    def _initNext(self):
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

class ViewDepotLieuQuantite(TableView):
    def _initNext(self):
        pass

