from PyQt5 import QtCore, QtWidgets,QtWidgets

class ComboBoxGeoResultDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self,parent=None,mere=None):
        super(ComboBoxGeoResultDelegate, self).__init__(parent)
        self.parent=parent
        self.mere=mere
        
    def titleEdition(self,dict_result):
        return '{} {} | {} au {} {} {} [lat: {} long: {}]'.format(dict_result['type'],
                                                                 dict_result['i'],
                                                                 dict_result['nom'],
                                                                 dict_result['adresse'],
                                                                 dict_result['cp'],
                                                                 dict_result['ville'],
                                                                 dict_result['latitude'],
                                                                 dict_result['longitude'])
    
    def createEditor(self, parent, option, index):
        if not index.isValid():return False
        self.comboBox = QtWidgets.QComboBox(parent)
        self.comboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        lieu = index.data(QtCore.Qt.UserRole)
        for dict_resel_lieu in lieu.adresse._listResultatGeo:
            self.comboBox.addItem(self.titleEdition(dict_resel_lieu))
        return self.comboBox

    def setEditorData(self, editor, index):
        value = index.data(QtCore.Qt.DisplayRole)
        if isinstance(value,int):value=str(value)
        editor.setEditText(value)

    def setModelData(self, editor, model, index):
        if not index.isValid():return False
        index.model().setData(index, editor.currentIndex(), QtCore.Qt.EditRole)

    def paint(self, painter, option, index):
        opt= QtWidgets.QStyleOptionComboBox()
        opt.rect= option.rect
        QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)


class ComboBoxDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self,parent=None,mere=None,comboBoxTable=None,comboBoxArg=None):
        super(ComboBoxDelegate, self).__init__(parent)
        self.parent=parent
        self.mere=mere
        self.comboBoxTable=comboBoxTable
        self.comboBoxArg=comboBoxArg

    def createEditor(self, parent, option, index):
        if not index.isValid():return False
        self.currentIndex=index  
        self.comboBox = QtWidgets.QComboBox(parent)
        self.comboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        for genre in self.comboBoxTable.data_arg[self.comboBoxArg]:
            if isinstance(genre,int):genre=str(genre)
            self.comboBox.addItem(genre)
        value = index.data(QtCore.Qt.DisplayRole)
        if isinstance(value,int):value=str(value)
        self.comboBox.setEditText(value)
        self.comboBox.model().sort(0,QtCore.Qt.AscendingOrder)
        return self.comboBox

    def setEditorData(self, editor, index):
        value = index.data(QtCore.Qt.DisplayRole)
        if isinstance(value,int):value=str(value)
        editor.setEditText(value)

    def setModelData(self, editor, model, index):
        if not index.isValid():return False
        index.model().setData(index, editor.currentText(), QtCore.Qt.EditRole)

    def paint(self, painter, option, index):
        opt= QtWidgets.QStyleOptionComboBox()
        opt.rect=option.rect
        QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)


class GridTourneeDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self,parent=None,mere=None):
        super(GridTourneeDelegate, self).__init__(parent)    
    
    def paint(self, painter, option, index):    
        """appelé case par case pour en dessiner le contenu"""        
        painter.save()   
        painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())
        if index.column()<1:painter.drawLine(option.rect.topRight(), option.rect.bottomRight())
        painter.restore()
        QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)


class LineEditDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self,parent=None):
        super(LineEditDelegate, self).__init__(parent)
        self.parent=parent
        
    def createEditor(self, parent, option, index):
        if not index.isValid():return False
        self.currentIndex=index  
        self.lineEdit = QtWidgets.QLineEdit(parent)
        return self.lineEdit
              
    def setEditorData(self, editor, index):
        editor.setText(index.data(QtCore.Qt.DisplayRole))
        editor.deselect()
        editor.setCursorPosition(0);

    def setModelData(self, editor, model, index):
        if not index.isValid():return False
        index.model().setData(index, editor.text(), QtCore.Qt.EditRole)





# class ButtonGeolocDelegate(QtWidgets.QStyledItemDelegate):
#     geolocalisation = QtCore.Signal()
#     def __init__(self,parent=None,mere=None):
#         super(ButtonGeolocDelegate, self).__init__(parent)
#         self.parent=parent
#         self.mere=mere
# 
#     def createEditor(self, parent, option, index):
#         if not index.isValid():return False
#         self.bout =  QtWidgets.QPushButton(parent)
#         self.bout.clicked.connect(lambda bout_index:self.parent.parent.geolocalisation(index=bout_index))
#         return self.bout
# 
#     def paint(self, painter, option, index):
#         optButton= QtWidgets.QStyleOptionButton()
#         optButton.rect= option.rect
#         QtWidgets.QApplication.style().drawControl(QtWidgets.QStyle.CE_PushButton, optButton, painter)
        

# class ComboBoxCpVilleDelegate(ComboBoxDelegate):        
#     def __init__(self,parent=None,mere=None,comboBoxTable=None,comboBoxArg=None,col_cp=None,col_ville=None):
#         super(ComboBoxCpVilleDelegate, self).__init__(parent=parent,mere=mere,comboBoxTable=comboBoxTable,comboBoxArg=comboBoxArg)
#         self.col_cp=col_cp
#         self.col_ville=col_ville
# 
#     def setModelData(self, editor, model, index):
#         if not index.isValid():return False
#         colonne=index.column()
#         row=index.row()
#         index.model().setData(QtCore.QModelIndex(row,self.), editor.currentText(), QtCore.Qt.EditRole)

# class CalendarDelegate(QtWidgets.QStyledItemDelegate):
#     def __init__(self,parent=None):
#         super(calendarDelegate, self).__init__(parent)
#         self.parent= parent
# 
#     def createEditor(self, parent, option, index):
#         if not index.isValid():return False
#         self.currentIndex=index  
#         self.calendar = QtWidgets.QCalendarWidget(parent)
#         self.calendar = QtWidgets.QDateTimeEdit(parent)
#         self.calendar.setDisplayFormat("dd.MM.yyyy")
#         self.calendar.setCalendarPopup(True)
#         value = index.data(QtCore.Qt.DisplayRole)
#         self.calendar.setDate(value)
#         return self.calendar
# 
#     def setEditorData(self, editor, index):
#         value = index.data(QtCore.Qt.DisplayRole)
#         editor.setDate(value)
# 
#     def setModelData(self, editor, model, index):
#         if not index.isValid():return False
#         index.model().setData(index, editor.date(), QtCore.Qt.EditRole)
# #
# #    def paint(self, painter, option, index):
# #        date = index.model().data(index, QtCore.Qt.DisplayRole)
# #        myOption = option
# #        myOption.displayAlignment = QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter
# #        QtWidgets.QStyledItemDelegate.paint(painter, myOption, index)
# 
# class RailDelegate(QtWidgets.QStyledItemDelegate):
#     def __init__(self,parent=None,mere=None):
#         super(RailDelegate, self).__init__(parent)    
# 
#     def sizeHint(self,option=None, index=None):
#         pixmap = index.model().data(index,QtCore.Qt.DecorationRole)
#         return QtCore.QSize(pixmap.width(),pixmap.height())
#     
#     def updateEditorGeometry(self,editor, option,index):
#         editor.setGeometry(option.rect) 
#   
#     def paint(self,painter,option,index):
#         pixmap = index.model().data(index,QtCore.Qt.DecorationRole)
#         painter.drawPixmap(option.rect, pixmap)

#class ListDragDrougDelegate(QtWidgets.QStyledItemDelegate):
#    def __init__(self,parent=None,mere=None):
#        super(ListDragDrougDelegate, self).__init__(parent)     
#        self.parent=parent
#        self.mere=mere
#        
#    def paint(self,painter,option= QtWidgets.QStyleOptionViewItem(),index=None):
#        widgetList=QtWidgets.QListView()
#        widgetList.resize(option.rect.width(),option.rect.height())
#        tournee=index.model().data(index,QtCore.Qt.UserRole)
#        for contrat in tournee.listContrat:
#            dbid_item=QtWidgets.QListItem()
#            dbid_item.setText(str(contrat.dbid))
#            widgetList.addItem(dbid_item)
#        #painter.translate(option.rect.topLeft())
#  #      widgetList.render(painter, option.rect.topLeft(),option.rect )
##        opt= QtWidgets.QStyleOptionViewItem()
##        opt.rect=option.rect
#        painter.save()
##        painter.setClipRect(option.rect)
##        painter.translate(option.rect.topLeft())
#        widgetList.render(painter, option.rect.topLeft(),option.rect )
#        painter.restore()
#
#    def sizeHint(self,option=QtWidgets.QStyleOptionViewItem, index=None):
#        widgetList=QtWidgets.QListWidget()
#        tournee=index.model().data(index,QtCore.Qt.UserRole)
#        for contrat in tournee.listContrat:
#            dbid_item=QtWidgets.QListWidgetItem()
#            dbid_item.setText(str(contrat.dbid))
#            widgetList.addItem(dbid_item)
#        return widgetList.sizeHint()
