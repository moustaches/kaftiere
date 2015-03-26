'''
Created on 8 mai 2013

@author: moustache
'''

from PyQt5 import QtCore, QtWidgets,QtGui

class Model(QtCore.QAbstractTableModel):
    def __init__(self,parent=None,mere=None,**arguments):
        super(Model, self).__init__(parent)    
        self.parent=parent
        self.mere=mere
        self._initNext(**arguments)
        
    def _initNext(self,**arguments):
        pass

    def headerData(self,section, orientation,role):
        if role == QtCore.Qt.DisplayRole: 
            if orientation == QtCore.Qt.Horizontal:
                return self.HEADERDATA[section]
            else: return None
        else:return None
 
    def columnCount(self, parent=None):
        return len(self.HEADERDATA) 
    
    def insertRows(self,row=0,count=0,index=QtCore.QModelIndex()):
        count=self.rowCount(self)
        self.beginInsertRows(index, count, count)
        self.endInsertRows()
        return True
        
    def insertColumns(self,column=0,count=0,index=QtCore.QModelIndex()):
        count=self.columnCount(self)
        self.beginInsertColumns(index, count, count)
        self.endInsertColumns()
        return True
        
class ModelListe(QtCore.QAbstractTableModel):
    def __init__(self,parent=None,mere=None,**arguments):
        super(ModelListe, self).__init__(parent)    
        self.parent=parent
        self.mere=mere
        self._initNext(**arguments)
        
    def _initNext(self,**arguments):
        pass
    
    def insertRows(self,row=0,count=0,index=QtCore.QModelIndex()):
        count=self.rowCount(self)
        self.beginInsertRows(index, count, count)
        self.endInsertRows()
        return True
        
    def insertColumns(self,column=0,count=0,index=QtCore.QModelIndex()):
        count=self.columnCount(self)
        self.beginInsertColumns(index, count, count)
        self.endInsertColumns()
        return True
        
        
class ModelLieuDB(Model):
    def _initNext(self):
        self.HEADERDATA=['N°','Lieux','Adresse Principale','Cp','Ville','Genre','Pertinence','Saturation','Latitude','Longitude']
        self.recherche_bas=True
        self.listLieu=[]
        self.initData()
        
    def _rechercher(self,texte):
        texte_user=texte.lower()
        for lieu in self.listLieu:
            num=lieu.nom.lower().find(texte_user)
            if num != -1: return self.listLieu.index(lieu),self.HEADERDATA.index('Lieux')
            num=lieu.adresse.adresse.lower().find(texte_user)
            if num != -1: return self.listLieu.index(lieu),self.HEADERDATA.index('Adresse Principale')
        return None
           
    def rechercher(self,texte):
        var = self._rechercher(texte)
        if var:
            ind=self.parent.modelProxyLieuDB.mapFromSource(self.createIndex(var[0],var[1]))
            self.parent.viewTableLieuDB.scrollTo(ind)
            self.parent.viewTableLieuDB.selectionModel().clear()
            self.parent.viewTableLieuDB.selectionModel().select(ind,QtWidgets.QItemSelectionModel.SelectCurrent)

    def initData(self):
        self.listLieu=[]
        for lieu in self.mere.dictLieu.values():
            self.ajouterLieu(lieu)

                
    def ajouterLieu(self,lieu=None):
        self.listLieu.append(lieu)
        self.insertRows()
        
    def nouvLieu(self):
        nouv_lieu=self.mere.nouvLieu(nom='Pute')
        self.ajouterLieu(lieu=nouv_lieu)

    def flags(self, index):
        if not index.isValid():
            return None
        if index.column()==0:return  QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable
        else:return  QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable
            
    def data(self, index, role): 
        if not index.isValid(): 
            return None
        colonne=index.column()
        row=index.row()
        if role == QtCore.Qt.DisplayRole:
            if colonne==0:return self.listLieu[row].dbid
            elif colonne==1:return self.listLieu[row].nom
            elif colonne==2:
                if hasattr(self.listLieu[row].adresse, 'adresse'): return self.listLieu[row].adresse.adresse
                else:return"pas adresse"
            elif colonne==3:
                if hasattr(self.listLieu[row].adresse, 'cp'): return self.listLieu[row].adresse.cp
                else:return"pas adresse"
            elif colonne==4:
                if hasattr(self.listLieu[row].adresse, 'ville'): return self.listLieu[row].adresse.ville
                else:return"pas adresse"               
            elif colonne==5:return self.listLieu[row].genre
            elif colonne==6:return self.listLieu[row].pertinence
            elif colonne==7:return 0
            elif colonne==8:return self.listLieu[row].adresse.latitude
            elif colonne==9:return self.listLieu[row].adresse.longitude
        elif role == QtCore.Qt.UserRole:
            return self.listLieu[row]
            
        return None       

    def setData(self, index, value, role):
        if not index.isValid(): 
            return None
        if role == QtCore.Qt.EditRole:
            if index.column()==1:self.listLieu[index.row()].nom=value
            print(value)
            return True 
        return None
    
    def rowCount(self, parent): 
        return len(self.listLieu) 
 

class ModelClient(Model):
    """Model pourla creation,edition et gestion des clients"""
    def _initNext(self,**arguments):
        self.HEADERDATA=['N°','Nom', 'Pixmap']
        self.listClient=[]
        self.initData()

    def initData(self):
        for client in self.mere.dictClient.values():
            self.ajouterClient(client)
            
    def ajouterClient(self,client):
        self.listClient.append(client)
        self.insertRows()
 
    def supprimerClient(self,client):
        self.listClient.remove(client)
        self.removeColumns()

    def flags(self, index):
        if not index.isValid():
            return None
        if index.column()==0:return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        elif index.column()==1:return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable 
        elif index.column()==2:return  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable| QtCore.Qt.ItemIsDragEnabled
        
    def data(self, index, role): 
        if not index.isValid(): 
            return None
        colonne=index.column()
        row=index.row()
        if role == QtCore.Qt.DisplayRole:
            if colonne==0:return self.listClient[row].dbid
            elif colonne==1:return self.listClient[row].nom
        if role == QtCore.Qt.DecorationRole:
            if colonne==2:return self.listClient[row].pixmap
        if role == QtCore.Qt.UserRole:
            return self.listClient[row]
        return None   
            
    def rowCount(self, parent): 
        return len(self.listClient)


class ModelParcoursTanponade(Model):
    """Model pour l  edition et gestion des tampons des parcours"""
    def _initNext(self,**arguments):
        self.HEADERDATA=['Pixmap', 'Num', 'Pedaleur']
        self.listParcours=[]
            
    def ajouterParcours(self,parcours):
        self.listParcours.append(parcours)
        self.insertRows()
 
    def supprimerParcours(self,parcours):
        self.listParcours.remove(parcours)
        self.removeColumns()

    def flags(self, index):
        if not index.isValid():
            return None
        if index.column()==0:return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        elif index.column()==1:return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable 
        elif index.column()==2:return  QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
    def data(self, index, role): 
        if not index.isValid(): 
            return None
        colonne=index.column()
        row=index.row()
        if role == QtCore.Qt.DisplayRole:
            if colonne==0:return self.listParcours[row].pedpaleur.nom
            elif colonne==1:return self.listParcours[row].dbid
        if role == QtCore.Qt.DecorationRole:
            if colonne==0:return self.listParcours[row].pixmap
        if role == QtCore.Qt.UserRole:
            return self.listParcours[row]
        return None   
            
    def rowCount(self, parent): 
        return len(self.listParcours)


class ModelContrat(Model):
    """Model pourla creation,edition et gestion des contrats"""
    def _initNext(self,**arguments):
        self.HEADERDATA=['dbid','Pixmap']
        self.listContrat=[]
        self._genreContrat=None
                
    def clientChanged(self):
        if self.parent.client:
            self.reset()
            for contrat in self.parent.client.listContrat:
                if contrat.genre==self._genreContrat:
                    self.ajouterContrat(contrat)                
        
    def ajouterContrat(self,contrat):
        self.listContrat.append(contrat)
        self.insertRows()
 
    def supprimerContrat(self,contrat):
        self.removeRows(self.listContrat.index(contrat),1)
        
    def reset(self):
        self.beginResetModel()
        self.listContrat=[]
        self.endResetModel()

    def flags(self, index):
        if not index.isValid():
            return None
        if index.column()==0:return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        elif index.column()==1:return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled
           
    def data(self, index, role): 
        if not index.isValid(): 
            return None
        colonne=index.column()
        row=index.row()
        if role == QtCore.Qt.DisplayRole:
            if colonne==0:return self.listContrat[row].dbid
        if role == QtCore.Qt.DecorationRole:
            if colonne==1:return self.listContrat[row].pixmap
        if role == QtCore.Qt.UserRole:
            return self.listContrat[row]
        return None   
            
    def rowCount(self, parent=None): 
        return len(self.listContrat)


class ModelTournee(Model):
    """Model pourla creation,edition et gestion des tournees"""
    def _initNext(self,**arguments):
        self.HEADERDATA=['N°','Ref Contrats']
        self.listTournee=[]
        self.initData()

    def initData(self):
        for tournee in self.mere.dictTournee.values():
            self.ajouterTournee(tournee)  
            
    def ajouterTournee(self,tournee):
        self.listTournee.append(tournee)
        self.insertRows()
        
    def supprimerTournee(self,tournee):
        self.listTournee.remove(tournee)
        self.removeRows()        
        
    def ajouterContrat(self, contrat , row, column):
        max=self.columnCount()
        tournee=self.listTournee[row]
        tournee.ajouterContrat(contrat, rang=column-1)
        if len(tournee.listContrat)>=max:
            self.insertColumns()

    def retirerContrat(self, contrat , row, column):
        max0=self.columnCount()
        tournee=self.listTournee[row]
        tournee.retirerContrat(contrat)
        max1=self.columnCount()
        if max0 !=max1: self.removeColumns()

    def flags(self, index):
        if not index.isValid():
            return None
        return  QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable| QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDragEnabled

    def data(self, index, role): 
        if not index.isValid(): 
            return None
        colonne=index.column()
        row=index.row()
        if role == QtCore.Qt.DecorationRole:
            if colonne==0:return self.listTournee[row].pixmap
            elif colonne>0:
                if colonne<=len(self.listTournee[row].listContrat):
                    return self.listTournee[row].listContrat[colonne-1].pixmap
        if role == QtCore.Qt.UserRole:
            if colonne==0:return self.listTournee[row]
            elif colonne>0:
                if colonne<=len(self.listTournee[row].listContrat):            
                    return self.listTournee[row].listContrat[colonne-1]
        return None   

    def setData(self, index, value, role):
        if not index.isValid(): 
            return None
        if role == QtCore.Qt.UserRole:
            if index.column()>0:
                self.ajouterContrat(value, index.row(), index.column())
                self.dataChanged.emit(self.createIndex(index.row(),0),self.createIndex(index.row(),self.columnCount()))
        if role == QtCore.Qt.UserRole+1:
            if index.column()>0:
                self.retirerContrat(value, index.row(), index.column())
                self.dataChanged.emit(self.createIndex(index.row(),0),self.createIndex(index.row(),self.columnCount()))
    def rowCount(self, parent=None): 
        return len(self.listTournee)
        
    def columnCount(self, parent=None):
        return max(len(tournee.listContrat) for tournee in self.listTournee) + 1

    def headerData(self,section, orientation,role):
        return None

    def insertColumns(self,column=0,count=0,index=QtCore.QModelIndex()):
        count=self.columnCount(self)
        self.beginInsertColumns(index,count, count)
        self.endInsertColumns()
        return True

    def removeColumns(self, position=0, rows=1,index=QtCore.QModelIndex()):
        self.beginRemoveColumns(index, position, position + rows - 1)
        self.endRemoveColumns()
        return True


class ModelParcours(Model):
    """Model pourla creation,edition et gestion des Parcours"""
    def _initNext(self,**arguments):
        self.HEADERDATA=['Parcours','Pedaleur', 'Nb Lieux', 'Nb Lieux Cheminer', 'Km', 'Poid', 'Volume', 'Prix']
        self.listParcours=[]

    def tourneeChanged(self):
        if self.parent.tournee:
            self.reset()
            for parcours in self.parent.tournee.listParcours:
                self.ajouterParcours(parcours)     
            
    def ajouterParcours(self,parcours):
        self.listParcours.append(parcours)
        self.insertColumns(self.listParcours.index(parcours)+1, 1)
        
    def supprimerParcours(self,parcours):
        if parcours in self.listParcours:
            self.removeColumns(self.listParcours.index(parcours)+1, 1)
            self.listParcours.remove(parcours)
            
    def reset(self):
        self.beginResetModel()
        self.listParcours=[]
        self.endResetModel()

    def flags(self, index):
        if not index.isValid():
            return None
        if index.column()==0:return QtCore.Qt.NoItemFlags
        elif index.row()==0:return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        elif index.row()==1:return  QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable| QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDragEnabled
        elif index.row()==2:return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        elif index.row()==3:return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        elif index.row()==4:return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        elif index.row()==5:return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        elif index.row()==6:return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        elif index.row()==7:return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else :return None
        
    def data(self, index, role): 
        if not index.isValid(): 
            return None
        colonne=index.column()
        row=index.row()        
        if role == QtCore.Qt.DecorationRole:
            if colonne ==0:return None
            elif row==0:return self.listParcours[colonne-1].pixmap
            elif row==1: 
                if self.listParcours[colonne-1].pedaleur:return self.listParcours[colonne-1].pedaleur.pixmap
                else :return None
        if role == QtCore.Qt.DisplayRole:
            if colonne ==0:
                if row==0:return "P0"
                elif row==1:return "Non associé"
                elif row==2: 
                    if self.parent.tournee :return len(self.parent.tournee.listLieuSansParcours)
                    else :return 0
                else:return 0
            elif row==2:
                if self.listParcours[colonne-1].list_dbid_lieu:return len(self.listParcours[colonne-1].list_dbid_lieu)
                else: return 0
            elif row==3:
                if self.listParcours[colonne-1].line:return len(self.listParcours[colonne-1].line)
                else: return 0
            elif row==4:
                if self.listParcours[colonne-1].chemin:return self.listParcours[colonne-1].chemin.longueur
                else: return 0
            elif row==5:
                if self.listParcours[colonne-1].list_dbid_lieu:return self.listParcours[colonne-1].poid
                else: return 0
            elif row==6:
                if self.listParcours[colonne-1].list_dbid_lieu:return self.listParcours[colonne-1].volume
                else: return 0
            elif row==7:
                if self.listParcours[colonne-1].list_dbid_lieu:return self.listParcours[colonne-1].prix
                else: return 0
        if role == QtCore.Qt.UserRole:
            return self.listParcours[colonne-1]
        return None   

    def setData(self, index, value, role):
        if not index.isValid(): 
            return None
        if role == QtCore.Qt.UserRole:
            if index.column()>0:self.listParcours[index.column()-1].pedaleur=value

    def rowCount(self, parent=None): 
        return len(self.HEADERDATA)
        
    def columnCount(self, parent=None):
        return len(self.listParcours)+1 

    def headerData(self,section, orientation,role):
        if role == QtCore.Qt.DisplayRole: 
            if orientation == QtCore.Qt.Vertical:
                return self.HEADERDATA[section]
            else: return None
        else:return None

    def insertColumns(self,column=0,count=0,index=QtCore.QModelIndex()):
        count=self.columnCount(self)
        self.beginInsertColumns(index,count, count)
        self.endInsertColumns()
        return True

    def removeColumns(self, position=0, rows=1,index=QtCore.QModelIndex()):
        self.beginRemoveColumns(index, position, position + rows - 1)
        self.endRemoveColumns()
        return True


class ModelLieuEditAdresse(Model):
    """Model pour importation de lieu, tableau d'edition des adresses des nouveaux lieux"""
    def _initNext(self,**arguments):
        self.HEADERDATA=['N°','Etat','Lieux','Adresse','         Cp         ','  Ville  ','latitude','longitude','GEO','           Resultat geoloc             ']
        self.listLieu=[]
        self.listLieuGeoCheck=[]
        
    def reset(self):
        self.beginResetModel()
        self.listLieu=[]
        self.endResetModel()
        
    def ajouterLieu(self,lieu):
        lieu._choixLieu=None
        self.listLieu.append(lieu)
        if lieu.dbid:self.listLieuGeoCheck.append(QtCore.Qt.Unchecked)
        else:self.listLieuGeoCheck.append(QtCore.Qt.Checked)
        self.insertRows()
    
    def flags(self, index):
        if not index.isValid():
            return None
        if index.column()==0:return  QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable
        elif index.column()==8:return QtCore.Qt.ItemIsUserCheckable| QtCore.Qt.ItemIsEnabled
        elif index.column()==9:return QtCore.Qt.ItemIsEnabled| QtCore.Qt.ItemIsEditable
        else: return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
           
    def data(self, index, role): 
        if not index.isValid(): 
            return None
        colonne=index.column()
        row=index.row()
        if role == QtCore.Qt.DisplayRole:
            if colonne==0:return self.listLieu[row].dbid
            elif colonne==1:return self.listLieu[row].etat
            elif colonne==2:return self.listLieu[row].nom
            elif colonne==3:return self.listLieu[row].adresseProvisoire.adresse
            elif colonne==4:return self.listLieu[row].adresseProvisoire.cp
            elif colonne==5:return self.listLieu[row].adresseProvisoire.ville
            elif colonne==6:return self.listLieu[row].adresseProvisoire.latitude
            elif colonne==7:return self.listLieu[row].adresseProvisoire.longitude
            elif colonne==9:return self.listLieu[index.row()].adresseProvisoire._choixResultatGeo
        elif role == QtCore.Qt.CheckStateRole:
            if colonne==8:return  self.listLieuGeoCheck[row]
        if role == QtCore.Qt.BackgroundRole:
            if self.listLieu[row].dbid:return QtWidgets.QBrush(QtCore.Qt.green) 
            elif self.listLieu[row].adresseProvisoire.latitude != 0:return QtWidgets.QBrush(QtCore.Qt.yellow)       
            return QtWidgets.QBrush(QtCore.Qt.red)
        if role == QtCore.Qt.UserRole:
            return self.listLieu[row]
        return None   
            
    def setData(self, index, value, role):
        if not index.isValid(): 
            return None
        if role == QtCore.Qt.EditRole:
            if index.column()==0:return self.listLieu[index.row()].dbid
            elif index.column()==1:self.listLieu[index.row()].etat=value
            elif index.column()==2:self.listLieu[index.row()].nom=value
            elif index.column()==3:self.listLieu[index.row()].adresseProvisoire.adresse=value
            elif index.column()==4:self.listLieu[index.row()].adresseProvisoire.cp=value                
            elif index.column()==5:self.listLieu[index.row()].adresseProvisoire.ville=value
            elif index.column()==6:self.listLieu[index.row()].adresseProvisoire.latitude=float(value)
            elif index.column()==7:self.listLieu[index.row()].adresseProvisoire.longitude=float(value)
            elif index.column()==9:
                self.listLieu[index.row()].adresseProvisoire._choixResultatGeo=value
                dict_res=self.listLieu[index.row()].adresseProvisoire._listResultatGeo[value]
                self.listLieu[index.row()].adresseProvisoire.adresse=dict_res['adresse']
                self.listLieu[index.row()].adresseProvisoire.cp=dict_res['cp']
                self.listLieu[index.row()].adresseProvisoire.ville=dict_res['ville']
                self.listLieu[index.row()].adresseProvisoire.latitude=dict_res['latitude']
                self.listLieu[index.row()].adresseProvisoire.longitude=dict_res['longitude']
            return True
        elif role == QtCore.Qt.CheckStateRole:
            if index.column()==8: self.listLieuGeoCheck[index.row()]=value
            self.dataChanged.emit(self.createIndex(index.row(),8),self.createIndex(index.row(),8))
        return None
            
    def rowCount(self, parent): 
        return len(self.listLieu)
 
    def geolocalisation(self,index=None):
        """geolocalise les lieux selectionnée dans listLieuGeoCheck"""
        tot=0
        for check in self.listLieuGeoCheck:
            if check == QtCore.Qt.Checked:tot+=1
        self.parent.progressBarGeoLieu.setValue(0)
        i=0
        for ind_check in range(len(self.listLieuGeoCheck)):
            if self.listLieuGeoCheck[ind_check] == QtCore.Qt.Checked:
                i+=1
                self.setData(self.createIndex(ind_check,9), self.listLieu[ind_check].adresseProvisoire.geocodage(),  QtCore.Qt.EditRole)
                self.dataChanged.emit(self.createIndex(ind_check,0),self.createIndex(ind_check,7))
                self.parent.progressBarGeoLieu.setValue(int((i*100)/tot))
                self.parent.progressBarGeoLieu.setFormat('{}/{} : géolocalisation de {}'.format(i,tot,self.listLieu[ind_check].nom))
       
class ModelMatchingLieu(Model):
    """Model pour importation de lieu, tableau d'edition des nouveaux lieux"""
    def _initNext(self,**arguments):
        self.HEADERDATA=['Type','N°','Lieux','Adresse','Cp','Ville','Distance']
        self.lieu=None
     
    def rafraichir(self):
        if self.lieu:
            self.reset()
            if self.lieu._listInfoLieuRes:
                for dict_lieu_reslt in self.lieu._listInfoLieuRes:
                    self.insertRows()
                    
    def reset(self):
        self.beginResetModel()
        self.endResetModel()
  
    def matching(self,lieu=None,distance=100):
        """need info """
        self.lieu=lieu
        self.lieu._listInfoLieuRes=[]
        self.reset()
        if not self.lieu.dbid:
            dict_info={'type':'Insert',
                              'adresse':self.lieu.adresseProvisoire,
                              'nom':self.lieu.nom,
                              'distance':0,
                              'check':QtCore.Qt.Unchecked}
            self.lieu._listInfoLieuRes.append(dict_info)
        else:
            dict_info={'type':'DB',
                       'adresse':self.mere.Lieu(self.lieu.dbid).adresse,
                       'nom':self.mere.Lieu(self.lieu.dbid).nom,
                       'distance':0,
                       'check':QtCore.Qt.Checked, 
                       'dbid':self.lieu.dbid}
            self.lieu._listInfoLieuRes.append(dict_info)
        for dict_match in self.lieu.adresseProvisoire._matchingGeolocalisation(distance):
            dict_info={'type':'Geoloc',
                       'adresse':self.mere.Adresse(dict_match['dbid']),
                       'nom':self.mere.Adresse(dict_match['dbid']).lieu.nom,
                       'distance':dict_match['terre_dist_plus(latitude, longitude,%s,%s)AS distance'],
                       'check':QtCore.Qt.Unchecked, 
                       'dbid':self.mere.Adresse(dict_match['dbid']).lieu.dbid}
            self.lieu._listInfoLieuRes.append(dict_info)
        
    def flags(self, index):
        if not index.isValid():
            return None
        if index.column()==0:return QtCore.Qt.ItemIsUserCheckable| QtCore.Qt.ItemIsEnabled
        else: return  QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable
           
    def data(self, index, role): 
        if not index.isValid(): 
            return None
        colonne=index.column()
        row=index.row()
        if role == QtCore.Qt.DisplayRole:
            if colonne==0:return self.lieu._listInfoLieuRes[row]['type']
            elif colonne==1:return self.lieu._listInfoLieuRes[row]['adresse'].dbid
            elif colonne==2:return self.lieu._listInfoLieuRes[row]['nom']
            elif colonne==3:return self.lieu._listInfoLieuRes[row]['adresse'].adresse
            elif colonne==4:return self.lieu._listInfoLieuRes[row]['adresse'].cp
            elif colonne==5:return self.lieu._listInfoLieuRes[row]['adresse'].ville
            elif colonne==6:return self.lieu._listInfoLieuRes[row]['distance']
        if role == QtCore.Qt.UserRole:
            return self.listInfoLieuRes[row]
        elif role == QtCore.Qt.CheckStateRole:
            if colonne==0:return  self.lieu._listInfoLieuRes[row]['check']
        return None   
            
    def setData(self, index, value, role):
        if not index.isValid(): 
            return None
        if role == QtCore.Qt.CheckStateRole:
            if index.column()==0:
                for dict_InfoLieuRes in self.lieu._listInfoLieuRes:dict_InfoLieuRes['check']=QtCore.Qt.Unchecked 
                if value==QtCore.Qt.Checked:self.lieu._listInfoLieuRes[index.row()]['check']=QtCore.Qt.Checked                  
                self.dataChanged.emit(self.createIndex(0,0),self.createIndex(self.rowCount(None)-1,0))
                return True
        return None    
            
    def rowCount(self, parent): 
        if self.lieu:
            if self.lieu._listInfoLieuRes:return len(self.lieu._listInfoLieuRes)
        else:return 0


class ModelImportListing(Model):
    """Model pour importation de listing"""
    def _initNext(self,**arguments):
        self.HEADERDATA=['Importer', 'Commentaire','N°','Etat','Pertinance','saturation','Lieux','Adresse','    Cp   ','  Ville  ','latitude','longitude','GEO','           Resultat geoloc             ']
        self.listLieu=[]
        self.listLieuGeoCheck=[]
 
    def reset(self):
        self.beginResetModel()
        self.endResetModel()
        
    def ajouterLieu(self,lieu):
        lieu._choixLieu=None
        self.listLieu.append(lieu)
        lieu.isAcceptable
        if lieu.dbid:self.listLieuGeoCheck.append(QtCore.Qt.Unchecked)
        else:self.listLieuGeoCheck.append(QtCore.Qt.Checked)
        self.insertRows()
        
    def flags(self, index):
        if not index.isValid():
            return None
        if index.column() in (0, 12):return QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled
        elif index.column() in (7, 8, 9, 10, 11, 13):return  QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable| QtCore.Qt.ItemIsEditable
        else: return QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable
           
    def data(self, index, role): 
        if not index.isValid(): 
            return None
        colonne=index.column()
        row=index.row()
        if role == QtCore.Qt.DisplayRole:
            if colonne==1:return self.listLieu[row].isAcceptable[1]
            elif colonne==2:return self.listLieu[row].dbid
            elif colonne==3:return self.listLieu[row].etat
            elif colonne==4:return self.listLieu[row].pertinence
            elif colonne==5:return self.listLieu[row].saturation_max
            elif colonne==6:return self.listLieu[row].nom
            elif colonne==7:return self.listLieu[row].adresse.adresse
            elif colonne==8:return self.listLieu[row].adresse.cp
            elif colonne==9:return self.listLieu[row].adresse.ville
            elif colonne==10:return self.listLieu[row].adresse.latitude
            elif colonne==11:return self.listLieu[row].adresse.longitude
            elif colonne==13:
                if self.listLieu[index.row()].adresse._listResultatGeo:
                    val= self.listLieu[index.row()].adresse._choixResultatGeo
                    a=val+1
                    b=len(self.listLieu[index.row()].adresse._listResultatGeo)
                    c=self.listLieu[index.row()].adresse._listResultatGeo[val]
                    return '({}/{}) -  {}'.format(a,b,c)
                else : return 'sans géolocalisation'
        elif role == QtCore.Qt.CheckStateRole:
            if colonne==0:
                if self.listLieu[row].isAcceptable[0] :return QtCore.Qt.Checked
                else:return QtCore.Qt.Unchecked
            if colonne==12:
                return  self.listLieuGeoCheck[row]
        if role == QtCore.Qt.BackgroundRole:
            if colonne==1:
                if self.listLieu[row].isAcceptable[0]:return QtGui.QBrush(QtCore.Qt.green)   
                return QtGui.QBrush(QtCore.Qt.red)
            return None
        if role == QtCore.Qt.UserRole:return self.listLieu[row]
        return None   
            
    def setData(self, index, value, role):
        if not index.isValid(): 
            return None
        if role == QtCore.Qt.EditRole:
            if index.column()==7:self.listLieu[index.row()].adresse.adresse=value
            elif index.column()==8:self.listLieu[index.row()].adresse.cp=value                
            elif index.column()==9:self.listLieu[index.row()].adresse.ville=value
            elif index.column()==10:self.listLieu[index.row()].adresse.latitude=float(value)
            elif index.column()==11:self.listLieu[index.row()].adresse.longitude=float(value)
            elif index.column()==13:
                self.listLieu[index.row()].adresse._choixResultatGeo=value
                dict_res=self.listLieu[index.row()].adresse._listResultatGeo[value]
                self.listLieu[index.row()].adresse.adresse=dict_res['adresse']
                self.listLieu[index.row()].adresse.cp=dict_res['cp']
                self.listLieu[index.row()].adresse.ville=dict_res['ville']
                self.listLieu[index.row()].adresse.latitude=dict_res['latitude']
                self.listLieu[index.row()].adresse.longitude=dict_res['longitude']
            return True
        elif role == QtCore.Qt.CheckStateRole:
            if index.column()==0:
                if value==QtCore.Qt.Checked:
                    self.listLieu[index.row()].isAcceptable=True
                    self.listLieuGeoCheck[index.row()]=QtCore.Qt.Unchecked
                else :
                    self.listLieu[index.row()].isAcceptable=False
            if index.column()==12: 
                if value==QtCore.Qt.Checked:
                    self.listLieuGeoCheck[index.row()]=value
                    self.listLieu[index.row()].isAcceptable=False
            self.dataChanged.emit(self.createIndex(index.row(),0),self.createIndex(index.row(),13))
            return True
        return None
            
    def rowCount(self, parent): 
        return len(self.listLieu)
 
    def geolocalisation(self,index=None):
        """geolocalise les lieux selectionnée dans listLieuGeoCheck"""
        tot=0
        reussi =0
        for check in self.listLieuGeoCheck:
            if check == QtCore.Qt.Checked:tot+=1
        self.parent.progressBarGeoLieu.setValue(0)
        i=0
        for ind_check in range(len(self.listLieuGeoCheck)):
            if self.listLieuGeoCheck[ind_check] == QtCore.Qt.Checked:
                i+=1
                self.listLieu[ind_check].adresse.geocodage()
                if self.listLieu[ind_check].adresse._choixResultatGeo==0:#a matcher avec une seule adresse
                    self.listLieuGeoCheck[ind_check] = QtCore.Qt.Unchecked 
                    reussi+=1
                    self.setData(self.createIndex(ind_check,13), 0, QtCore.Qt.EditRole)
                self.dataChanged.emit(self.createIndex(ind_check,0),self.createIndex(ind_check,13))
                self.parent.progressBarGeoLieu.setValue(int((i*100)/tot))
                self.parent.progressBarGeoLieu.setFormat('{}/{} ({} réussis)  -  géolocalisation de {}'.format(i,tot,reussi,self.listLieu[ind_check].nom))
       
       
class ModelMatchingListing(Model):
    """Model pour importation de lieu, tableau d'edition des nouveaux lieux"""
    def _initNext(self,**arguments):
        self.HEADERDATA=['Type','N°','Etat','Pertinence','Saturation','Nom','Adresse', 'Cp', 'Ville', 'Distance', 'Latitude', 'Longitude']
        self.lieu=None
        
    def reset(self):
        self.beginResetModel()
        self.endResetModel()
        
    def rafraichir(self):
        if self.lieu:
            self.reset()
            if self.lieu._listInfoLieuRes:
                for dict_lieu_reslt in self.lieu._listInfoLieuRes:
                    self.insertRows()
  
    def matching(self,lieu=None,distance=100, geolocalisation=True):
        """need info """
        self.lieu=lieu
        self.reset()
        self.lieu._listInfoLieuRes=self.lieu._listInfoLieuRes[0:1]
        if self.lieu._listInfoLieuRes[0]['dbid']:
            lieu_match=self.mere.Lieu(self.lieu._listInfoLieuRes[0]['dbid'])
            dict_info={'type':'DB',
                              'dbid':lieu_match.dbid, 
                              'adresse':lieu_match.adresse.adresse,
                              'latitude':lieu_match.adresse.latitude,
                              'longitude':lieu_match.adresse.longitude,
                              'cp':lieu_match.adresse.cp, 
                              'ville':lieu_match.adresse.ville,
                              'etat':lieu_match.etat, 
                              'pertinence':lieu_match.pertinence, 
                              'saturation_max':lieu_match.saturation_max, 
                              'nom':lieu_match.nom,
                              'distance':0}
            self.lieu._listInfoLieuRes.append(dict_info)
        if geolocalisation==True:
            for dict_match in self.lieu.adresse._matchingGeolocalisation(distance):
                adresse_match=self.mere.Adresse(dict_match['dbid'])
                dict_info={'type':'Geoloc',
                           'adresse':adresse_match.adresse,
                           'latitude':adresse_match.latitude,
                           'longitude':adresse_match.longitude,
                           'cp':adresse_match.cp, 
                           'ville':adresse_match.ville, 
                           'nom':adresse_match.lieu.nom,
                           'etat':adresse_match.lieu.etat, 
                           'pertinence':adresse_match.lieu.pertinence, 
                           'saturation_max':adresse_match.lieu.saturation_max, 
                           'distance':dict_match['terre_dist_plus(latitude, longitude,%s,%s)AS distance'],
                           'dbid':adresse_match.lieu.dbid}
                self.lieu._listInfoLieuRes.append(dict_info)
        #for a in self.lieu._listInfoLieuRes:print(a)
        
    def flags(self, index):
        if not index.isValid():
            return None
        if index.column()==0:return QtCore.Qt.ItemIsUserCheckable| QtCore.Qt.ItemIsEnabled
        else: return  QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable
           
    def data(self, index, role): 
        if not index.isValid(): 
            return None
        colonne=index.column()
        row=index.row()
        if role == QtCore.Qt.DisplayRole:
            if colonne==0:return self.lieu._listInfoLieuRes[row]['type']
            elif colonne==1:return self.lieu._listInfoLieuRes[row]['dbid']
            elif colonne==2:return self.lieu._listInfoLieuRes[row]['etat']
            elif colonne==3:return self.lieu._listInfoLieuRes[row]['pertinence']
            elif colonne==4:return self.lieu._listInfoLieuRes[row]['saturation_max']
            elif colonne==5:return self.lieu._listInfoLieuRes[row]['nom']
            elif colonne==6:return self.lieu._listInfoLieuRes[row]['adresse']
            elif colonne==7:return self.lieu._listInfoLieuRes[row]['cp']
            elif colonne==8:return self.lieu._listInfoLieuRes[row]['ville']
            elif colonne==9:return self.lieu._listInfoLieuRes[row]['distance']
            elif colonne==10:return self.lieu._listInfoLieuRes[row]['latitude']
            elif colonne==11:return self.lieu._listInfoLieuRes[row]['longitude']
        if role == QtCore.Qt.UserRole:return self.lieu._listInfoLieuRes[row]
            
    def rowCount(self, parent): 
        if self.lieu:
            if self.lieu._listInfoLieuRes:return len(self.lieu._listInfoLieuRes)
        else:return 0
        

class ModelDepotLieuQuantite(Model):
    """gere les depots et leurs quantitées"""
    def _initNext(self,**arguments):
        self.listLieu=[]
        self.listDepot=[]
        self.kobjet=None

    def ajouterObjet(self,kobjet):
#        if kobjet.estAjoutable():
#            self.kobjet=kobjet
        if True == True:
            self.kobjet=kobjet
            for depot in self.kobjet.listDepot:
                self.ajouterDepot(depot)        
        
    def ajouterDepot(self,depot):
        if depot not in self.listDepot:
            self.kobjet.ajouterDepot(depot)
            self.listDepot.append(depot)
            self.insertColumns()
            for lieu in depot.listLieu:
                self.ajouterLieu(lieu)
                
    def supprimerDepot(self,depot):
        if depot in self.listDepot:
            self.removeColumns(self.listDepot.index(depot), 1)
            self.listDepot.remove(depot)

    def ajouterLieu(self,lieu):
        if lieu not in self.listLieu:
            self.listLieu.append(lieu)
            self.insertRows()

    def flags(self, index):
        return  QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role): 
        if not index.isValid(): 
            return None
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter;
        elif role == QtCore.Qt.DisplayRole:
            lieu=self.listLieu[index.row()]
            depot=self.listDepot[index.column()]
            return depot.quantiteLieu(lieu)
        elif role == QtCore.Qt.UserRole:#pour info depot
            return self.listDepot[index.column()]
        else:return None
                        
    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            lieu=self.listLieu[index.row()]
            depot=self.listDepot[index.column()]
            if depot.setLieuQuantite(lieu,quantite=value):
                print('oui!')
                self.dataChanged.emit(index, index)
                return True
            else:
                return False
        else:return None
            
    def headerData(self,section, orientation,role):
        if role == QtCore.Qt.DisplayRole: 
            if orientation == QtCore.Qt.Horizontal:
                depot=self.listDepot[section]
                return "{}\ntotal: {}\ndiff: {}".format(depot.nom,depot.infoQuantiteDepot,depot.quantite-depot.infoQuantiteDepot)
            else: return self.listLieu[section].nom
        elif role == QtCore.Qt.UserRole:
            if orientation == QtCore.Qt.Horizontal:return self.listDepot[section]
            else: return self.listLieu[section]
        else:return None
            
    def rowCount(self, parent): 
        return len(self.listLieu) 
 
    def columnCount(self, parent): 
        return len(self.listDepot) 
    
    def insertColumns(self,column=0,count=0,index=QtCore.QModelIndex()):
        count=self.columnCount(self)
        self.beginInsertColumns(index,count, count)
        self.endInsertColumns()
        return True

    def removeColumns(self, position, rows=1,index=QtCore.QModelIndex()):
        self.beginRemoveColumns(index, position, position + rows - 1)
        self.endRemoveColumns()
        return True
        
        
class ModelPedaleur(ModelListe):
    """Model pourla creation,edition et gestion des pedaleur"""
    def _initNext(self,**arguments):
        self.listPedaleur=[]
        self.initData()

    def initData(self):
        for pedaleur in self.mere.dictPedaleur.values():
            self.ajouterPedaleur(pedaleur)
            
    def ajouterPedaleur(self,pedaleur):
        self.listPedaleur.append(pedaleur)
        self.insertColumn(0)
 
    def supprimerPedaleur(self,pedaleur):
        self.removeColumn( self.listPedaleur.index(pedaleur))
        self.listPedaleur.remove(pedaleur)

    def flags(self, index):
        if not index.isValid():
            return None
        else:return QtCore.Qt.ItemIsEnabled #| QtCore.Qt.ItemIsSelectable| QtCore.Qt.ItemIsDragEnabled
        
    def data(self, index, role): 
        if not index.isValid(): 
            return None
        colonne=index.column()
        if role == QtCore.Qt.DecorationRole:
            return self.listPedaleur[colonne].pixmap
        if role == QtCore.Qt.UserRole:
            return self.listPedaleur[colonne]
        return None   
            
    def rowCount(self, parent): 
        return 1
    
    def columnCount(self, parent): 
        return len(self.listPedaleur)
        
        
class ModelListeLieu(ModelListe):
    """Model pourla la gestion des listelieu"""
    def _initNext(self,**arguments):
        self.listListeLieu=[]     
        self.initData()

    def initData(self):
        for liste_lieu in self.mere.dictListeLieu.values():
            self.ajouterListeLieu(liste_lieu)
   
    def ajouterListeLieu(self,listelieu):
        self.listListeLieu.append(listelieu)
        self.insertColumns(self.listListeLieu.index(listelieu), 1)
        
    def supprimerListeLieu(self,listelieu):
        if listelieu in self.listListeLieu:
            self.removeColumns(self.listListeLieu.index(listelieu)+1, 1)
            self.listListeLieu.remove(listelieu)

    def flags(self, index):
        if not index.isValid():
            return None
        else :return QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable| QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsDragEnabled
        
    def data(self, index, role): 
        if not index.isValid(): 
            return None
        colonne=index.column()
        if role == QtCore.Qt.DecorationRole:
            return self.listListeLieu[colonne].pixmap
        if role == QtCore.Qt.UserRole:
            return self.listListeLieu[colonne]
        return None   
        
    def rowCount(self, parent): 
        return 1
    
    def columnCount(self, parent): 
        return len(self.listListeLieu)

#     def insertColumns(self,column=0,count=0,index=QtCore.QModelIndex()):
#         count=self.columnCount(self)
#         self.beginInsertColumns(index,count, count)
#         self.endInsertColumns()
#         return True
# 
#     def removeColumns(self, position=0, rows=1,index=QtCore.QModelIndex()):
#         self.beginRemoveColumns(index, position, position + rows - 1)
#         self.endRemoveColumns()
#         return True

