'''
Created on 7 mai 2013

@author: moustache
'''

from PySide import QtCore, QtGui
from objets.objet import PedaleurK,ParcoursK,AdresseK,ClientK,ContratK,DepotK,LieuK,TourneeK


class QTobjet():
    """super classe de controle des objets qt"""
    def _initData(self,**arguments):
        self._initSqlData(**arguments)
        self._initObjetData(**arguments)
        self._initQtData(**arguments)
        
    def _initQtData(self,**arguments):
        pass
        
        
class ContratQ(QTobjet,ContratK):
    """classe de controle des contrats pour qt"""
    def __init__(self,mere): 
        ContratK.__init__(self,mere)
        QTobjet.__init__(self)
#         self._pixmap=None
 
    @property
    def pixmap(self):
#         if not self._pixmap:self.dessinerPixmap()
#         return self._pixmap  
        return self.dessinerPixmap()
        
    def dessinerPixmap(self):
        """dessinne son image"""
        pix_client=self.client.pixmap
        width_pix=pix_client.width()+10
        height_pix=pix_client.height()+10
        pix=QtGui.QPixmap(width_pix,height_pix)
        pix.fill(QtCore.Qt.transparent)        
        
        pix=QtGui.QPixmap(width_pix,height_pix)
        pix.fill(QtCore.Qt.transparent)
        painter=QtGui.QPainter(pix)
        painter.drawPixmap(QtCore.QPoint(10, 0), pix_client)
        painter.setPen(QtCore.Qt.black)
        painter.setFont(QtGui.QFont("Arial", 10))
        if self.genre=='devis':painter.drawText(QtCore.QRectF(0,0,30,20),  "{}*".format(self.num))
        else:painter.drawText(QtCore.QRectF(0,0,30,20),  "{}".format(self.num))
        painter.setFont(QtGui.QFont("Arial", 6))
        painter.drawText(QtCore.QRectF(0,20,60,10),  "L: {}   P: {}".format(len(self.listLieu),int(self.prix)))
        return pix


class LieuQ(LieuK, QTobjet):
    """classe de controle des lieux pour qt"""
    def __init__(self,mere):
        LieuK.__init__(self,mere)        
        QTobjet.__init__(self)


class AdresseQ(QTobjet,AdresseK):
    """classe de controle des adresses pour qt"""
    def __init__(self,mere): 
        AdresseK.__init__(self,mere)
        QTobjet.__init__(self)
        
        
class DepotQ(QTobjet,DepotK):
    """classe de controle des depots pour qt"""
    def __init__(self,mere):
        DepotK.__init__(self,mere)
        QTobjet.__init__(self)       
        
        
class ClientQ(QTobjet,ClientK):
    """classe de controle des clients pour qt"""
    def __init__(self,mere):
        ClientK.__init__(self,mere)       
        QTobjet.__init__(self)        
        self._pixmap=None
        
    @property
    def pixmap(self):
#        if not self._pixmap:self.dessinerPixmap()
#        return self._pixmap     
        return self.dessinerPixmap()
        
#     def nomChange(self):
#         self.objetChange.emit('Nom')
# 
#     def genreChange(self):
#         self.objetChange.emit('Genre')
#  
#     def surnomChange(self):
#         self.objetChange.emit('Surnom')
#         self.dessinerPixmap()
#         
    def dessinerPixmap(self):
        """dessinne son image"""
        lg_pix=len(self.surnom)*5+25
        pix=QtGui.QPixmap(lg_pix, 20)
        pix.fill(QtCore.Qt.transparent)
        painter=QtGui.QPainter(pix)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.red)
        painter.setBrush(QtCore.Qt.red)
        painter.drawEllipse(QtCore.QRect(5,5,lg_pix-10,10))
        painter.setPen(QtCore.Qt.black)
        font=QtGui.QFont("Arial", 10)
        font.setBold(True)
        font.setStretch(70)
        painter.setFont(font)
        painter.drawText(QtCore.QRectF(0,0,lg_pix,20), QtCore.Qt.AlignCenter, "{}".format(self.surnom))
        return pix
#        self.pixmapObjetChange.emit(self._pixmap)


class TourneeQ(QTobjet,TourneeK):
    """classe de controle des tournées pour qt"""
    def __init__(self, mere): 
        TourneeK.__init__(self,mere)       
        QTobjet.__init__(self) 
        
    @property
    def pixmap(self):
#        if not self._pixmap:self.dessinerPixmap()
#        return self._pixmap     
        return self.dessinerPixmap()
        
    def dessinerPixmap(self):
        """dessinne son image"""
        lg_pix=(int(self.dbid/10)+3)*5+50
        pix=QtGui.QPixmap(lg_pix,30)
        pix.fill(QtCore.Qt.transparent)
        painter=QtGui.QPainter(pix)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.lightGray)
        painter.setBrush(QtCore.Qt.lightGray)
        painter.drawEllipse(QtCore.QRect(5,5,lg_pix-8,12))
        painter.setPen(QtCore.Qt.yellow)
        painter.setBrush(QtCore.Qt.yellow)
        painter.drawEllipse(QtCore.QRect(7,7,lg_pix-12,8))
        painter.setPen(QtCore.Qt.black)
        painter.setFont(QtGui.QFont("Arial", 10))
        painter.drawText(QtCore.QRectF(0,0,lg_pix,20), QtCore.Qt.AlignCenter, "T-{}".format(self.dbid))

        painter.setFont(QtGui.QFont("Arial", 6))
        painter.drawText(QtCore.QRectF(0,20,60,10), "Nb : {}  L: {}   P: {}".format(len(self.listParcours), len(self.listLieuContrats),int(self.prix)))
        return pix
      
      
class ParcoursQ(QTobjet,ParcoursK):
    """classe de controle des parcours pour qt"""
    def __init__(self,mere): 
        ParcoursK.__init__(self,mere)
        QTobjet.__init__(self)
#         self._pixmap=None
 
    @property
    def pixmap(self):
#         if not self._pixmap:self.dessinerPixmap()
#         return self._pixmap  
        return self.dessinerPixmap()
        
    def dessinerPixmap(self):
        """dessinne son image"""
        lg_pix=(int(self.dbid/10)+3)*5+50
        pix=QtGui.QPixmap(lg_pix,30)
        pix.fill(QtCore.Qt.transparent)
        painter=QtGui.QPainter(pix)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.lightGray)
        painter.setBrush(QtCore.Qt.lightGray)
        painter.drawEllipse(QtCore.QRect(5,5,lg_pix-8,12))
        painter.setPen(QtCore.Qt.green)
        painter.setBrush(QtCore.Qt.green)
        painter.drawEllipse(QtCore.QRect(7,7,lg_pix-12,8))
        painter.setPen(QtCore.Qt.black)
        painter.setFont(QtGui.QFont("Arial", 10))
        painter.drawText(QtCore.QRectF(0,0,lg_pix,20), QtCore.Qt.AlignCenter, "P-{}".format(self.dbid))
        painter.setFont(QtGui.QFont("Arial", 6))
        painter.drawText(QtCore.QRectF(0,20,60,10), "L: {}   V: {}".format(len(self.listLieu),self.quantiteDepotTotal))
        return pix
        
class PedaleurQ(QTobjet,PedaleurK):
    """classe de controle des clients pour qt"""
    def __init__(self,mere):
        PedaleurK.__init__(self,mere)       
        QTobjet.__init__(self)        
        self._pixmap=None
        
    @property
    def pixmap(self):
#        if not self._pixmap:self.dessinerPixmap()
#        return self._pixmap     
        return self.dessinerPixmap()
               
    def dessinerPixmap(self):
        """dessinne son image"""
        lg_pix=len(self.surnom)*5+25
        pix=QtGui.QPixmap(lg_pix, 20)
        pix.fill(QtCore.Qt.transparent)
        painter=QtGui.QPainter(pix)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.blue)
        painter.setBrush(QtCore.Qt.blue)
        painter.drawEllipse(QtCore.QRect(1,1,lg_pix-4,16)) 
        painter.setPen(QtGui.QColor(self.couleur))
        painter.setBrush(QtGui.QColor(self.couleur))
        painter.drawEllipse(QtCore.QRect(2,2,lg_pix-6,14))   
        painter.setPen(QtCore.Qt.blue)
        painter.setBrush(QtCore.Qt.blue)
        painter.drawEllipse(QtCore.QRect(5,5,lg_pix-12,8))
        font=QtGui.QFont("Arial", 8)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QtCore.Qt.white)
        painter.setBrush(QtCore.Qt.white)
        painter.drawText(QtCore.QRectF(0,0,lg_pix,17), QtCore.Qt.AlignCenter, "{}".format(self.surnom))
        return pix
#        self.pixmapObjetChange.emit(self._pixmap)
