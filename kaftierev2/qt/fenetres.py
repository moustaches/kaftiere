'''
Created on 8 mai 2013

@author: moustache
'''
import datetime

import os
from PySide import QtCore,QtGui
from objets.mere import Mere
from outils.dock import DocK
from qt.modelview.view import ViewPedaleur,ViewParcours,ViewLieuDB,ViewLieuEditAdresse,ViewMatchingLieu,ViewClient,ViewContrat, ViewTournee, ViewImportListing, ViewMatchingListing, ViewDepotLieuQuantite
from qt.modelview.model import ModelPedaleur, ModelParcours,ModelLieuDB,ModelLieuEditAdresse,ModelMatchingLieu,ModelClient, ModelContrat, ModelTournee, ModelImportListing, ModelMatchingListing, ModelDepotLieuQuantite
from outils.kml import Kml, KmlParser
from qt.widget.widgets import KLabelPixmap, KComboBoxCouleur


class Fenetre(QtGui.QWidget):
    """super class fenetre
    --> parent: fenetre dont elle est logiquement issue
    --> mere: super class de gestion des K-objets
    """
    FONT={'table':QtGui.QFont("Ubuntu", 7)}
    def __init__(self,parent=None,mere=None,**arguments):
        super(Fenetre, self).__init__(parent)
        self.mere=mere   
        self.parent=parent
        self.createFenetre()
        self.createModel()
        self.createAction()
        self.createConnection()
        self._initNext(**arguments)

    def createAction(self):
        pass
    def createFenetre(self):
        pass
    def createModel(self):
        pass
    def createConnection(self):
        pass
    def _initNext(self):
        pass
    
class InitFenetre(Fenetre):
    """fenetre d'initialisation"""
    def createFenetre(self):
        self.setWindowTitle('Chargement')
        self.resize(395, 460)
        self.okButton = QtGui.QPushButton("Ok", parent=self)
        self.okButton.setGeometry(QtCore.QRect(10, 250, 361, 41))
        self.progressBar = QtGui.QProgressBar(parent=self)
        self.progressBar.setGeometry(QtCore.QRect(10, 200, 361, 31))
        self.progressBar.setValue(0)
        self.label = QtGui.QLabel(parent=self)
        self.label.setGeometry(QtCore.QRect(10, 230, 361, 17))
        self.label_2 = QtGui.QLabel(parent=self)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 341, 171))
        self.label_2.setPixmap(QtGui.QPixmap("{}/DIV/logo.jpeg".format(os.getcwd())))
        self.text=QtGui.QTextEdit(parent=self)
        self.text.setGeometry(QtCore.QRect(10, 300, 360, 150))
        
    def createConnection(self):
        self.okButton.clicked.connect(self.closeAction)

    def closeAction(self):
        self.mere._fenetre=None
        self.parent.mere=self.mere
        self.parent._initNext()
        self.parent.show()
        self.close()
       
    def initAction(self):
        self.mere=Mere(fenetre=self)
        self.mere.initData()
        self.text.append("Ok !")
        
    def _actualisation(self,val_prog_bar=None,i_tot=None,label=None,val_time=None):
        """fonction d'acces pour la mere a la fenetre"""
        if val_prog_bar:self.progressBar.setValue(val_prog_bar)
        if label:self.label.setText(label)
        if i_tot:self.text.append("Les {} {} chargé en {}s".format(i_tot,label,val_time))
          
class MainFenetre(QtGui.QMainWindow):
    """fenetre main kaftiere"""
    def __init__(self,parent=None):
        super(MainFenetre, self).__init__()
        self.initFenetre=InitFenetre(parent=self)
        self.initFenetre.setWindowFlags(QtCore.Qt.Window)
        self.initFenetre.show()
        self.mere=self.initFenetre.initAction()
        
    def _initNext(self):
        self.createAction()
        self.createFenetre()
        self.createConnection()
        #self.createModel()

#     def createModel(self):        
#         self.modelSelectRail=selectRailModel(parent=self,mere=self.mere)
#         self.listViewSelect.setModel(self.modelSelectRail)
    
    def createConnection(self):
        self.ongletClientContratPedaleur.currentChanged.connect(self.refreshToolBarClientContratPedaleur)
        self.ongletTourneeParcours.currentChanged.connect(self.refreshToolBarTourneeParcours)
        
    def refreshToolBarClientContratPedaleur(self,ind):
        if ind==0:self.fenetreClient.refreshToolBar()
        elif ind==1:self.fenetreContrat.refreshToolBar()
        else : self.fenetrePedaleur.refreshToolBar()

    def refreshToolBarTourneeParcours(self,ind):
        if ind==0:self.fenetreTournee.refreshToolBar()
        else : self.fenetreParcours.refreshToolBar()    
    
    def createAction(self):
        self.exitAction = QtGui.QAction('Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(self.close)

        self.fenetreOutilKmlAction= QtGui.QAction('Kml', self)
        self.fenetreOutilKmlAction.setShortcut('Ctrl+K')
        self.fenetreOutilKmlAction.triggered.connect(self.outilKmlAction)

        self.fenetreOutilTamponadeAction= QtGui.QAction('Tamponade', self)
        self.fenetreOutilTamponadeAction.setShortcut('Ctrl+T')
        self.fenetreOutilTamponadeAction.triggered.connect(self.outilTamponadeAction)

        self.fenetreOutilLieuDBAction= QtGui.QAction('DB Lieu', self)
        self.fenetreOutilLieuDBAction.setShortcut('Ctrl+L')
        self.fenetreOutilLieuDBAction.triggered.connect(self.outilLieuDBAction)

    def outilKmlAction(self):
        fenetreKml=FenetreKml(parent=self, mere=self.mere)
        fenetreKml.setWindowFlags(QtCore.Qt.Window)
        fenetreKml.show()     

    def outilLieuDBAction(self):
        fenetreLieuDB=FenetreLieuDB(parent=self, mere=self.mere)
        fenetreLieuDB.setWindowFlags(QtCore.Qt.Window)
        fenetreLieuDB.show()

    def outilTamponadeAction(self):
        fenetreTamponade=FenetreTamponade(parent=self, mere=self.mere)
        fenetreTamponade.setWindowFlags(QtCore.Qt.Window)
        fenetreTamponade.show() 

    def createFenetre(self):
        self.toolBar = self.addToolBar('Exit')
        self.toolBar.addAction(self.exitAction)    
      
        self.menuBarK =self.menuBar()
        self.menuFentreOutils =QtGui.QMenu( 'Outils', self.menuBarK)
        self.menuFentreOutils.addAction(self.fenetreOutilLieuDBAction)
        self.menuFentreOutils.addAction(self.fenetreOutilKmlAction)        
        self.menuFentreOutils.addAction(self.fenetreOutilTamponadeAction)
        self.menuFentreOutils.addAction(self.exitAction)
        self.menuBarK.addAction(self.menuFentreOutils.menuAction())

        centralwidget = QtGui.QWidget(self)
        self.setCentralWidget(centralwidget)

        self.fenetreClient=FenetreClient(parent=self,mere=self.mere)
        self.fenetreContrat=FenetreContrat(parent=self,mere=self.mere)
        self.fenetrePedaleur=FenetrePedaleur(parent=self,mere=self.mere)

        self.ongletClientContratPedaleur=QtGui.QTabWidget()
        self.ongletClientContratPedaleur.addTab(self.fenetreClient,"Client")
        self.fenetreClient.parentTab=self.ongletClientContratPedaleur
        self.ongletClientContratPedaleur.addTab(self.fenetreContrat,"Contrat")
        self.fenetreContrat.parentTab=self.ongletClientContratPedaleur
        self.ongletClientContratPedaleur.addTab(self.fenetrePedaleur,"Pedaleur")
        self.fenetreContrat.parentTab=self.ongletClientContratPedaleur
        
        self.dockWidgetClientContratPedaleur=QtGui.QDockWidget('Client - Contrat - Pedaleur', parent=self)
        self.dockWidgetClientContratPedaleur.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.dockWidgetClientContratPedaleur.setWidget(self.ongletClientContratPedaleur)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidgetClientContratPedaleur)

        self.fenetreTournee=FenetreTournee(parent=self,mere=self.mere)
        self.fenetreParcours=FenetreParcours(parent=self,mere=self.mere)
        
        self.ongletTourneeParcours=QtGui.QTabWidget()
        self.ongletTourneeParcours.addTab(self.fenetreTournee,"Tournee")
        self.fenetreTournee.parentTab=self.ongletTourneeParcours
        self.ongletTourneeParcours.addTab(self.fenetreParcours,"Parcours")
        self.fenetreParcours.parentTab=self.ongletTourneeParcours

        self.dockWidgetTourneeParcours=QtGui.QDockWidget('Tournee - Parcours', parent=self)
        self.dockWidgetTourneeParcours.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self.dockWidgetTourneeParcours.setWidget(self.ongletTourneeParcours)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockWidgetTourneeParcours)
        
#        self.wOnglet2=QtGui.QTabWidget()
#        self.wOnglet2.addTab(self.fenetreLieuDB,"Lieux DataBase")
#        self.wOnglet2.addTab(self.fenetreSelectLieu,"Lieux")
#
#        self.dockWidgetClientContrat2=QtGui.QDockWidget('Lieux qui lieullent', parent=self)
#        self.dockWidgetClientContrat2.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
#        self.dockWidgetClientContrat2.setWidget(self.wOnglet2)
#        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidgetClientContrat2)

        self.setWindowTitle('KAFTIERE')
        self.statusBar()
        self.resize(1000,500)
        
 
class FenetreTournee(Fenetre):       
    """fenetre Tournee"""
    
    def createModel(self):
        self.modelTournee=ModelTournee(parent=self,mere=self.mere)
        self.viewTournee.setModel(self.modelTournee)
        self.selectModelTournee=self.viewTournee.selectionModel()
         
    def createFenetre(self):
        self.viewTournee=ViewTournee(parent=self,mere=self.mere)
        layTourneeTable = QtGui.QGridLayout()
        layTourneeTable.addWidget(self.viewTournee,0,0,8,4)      
        self.setLayout(layTourneeTable)   

    def _initNext(self, **arguments):
        self.selectedTournee=None
        
    def createConnection(self):
        self.viewTournee.doubleClicked.connect(self.actionVoirParcours.trigger)
        selModelTournee=self.viewTournee.selectionModel()
        selModelTournee.currentChanged.connect(lambda :self.selTourneeChanged(tournee=self.modelTournee.data(self.viewTournee.currentIndex(),QtCore.Qt.UserRole)))

    def createAction(self):
        self.actionNouvelleTournee = QtGui.QAction('Nouvelle tournee', self)
        self.actionNouvelleTournee.setShortcut('Ctrl+N')
        self.actionNouvelleTournee.setStatusTip('Creer une nouvelle tournee (Ctrl+N)')
        self.actionNouvelleTournee.triggered.connect(self.nouvelleTournee)
        self.actionSupprimerTournee = QtGui.QAction('Supprimer tournee', self)
        self.actionSupprimerTournee.setShortcut('Ctrl+S')
        self.actionSupprimerTournee.setStatusTip('Supprimer la tournee (Ctrl+S)')
        self.actionSupprimerTournee.triggered.connect(lambda : self.supprimerTournee(self.selectedTournee))
        self.actionVoirParcours = QtGui.QAction('Voir parcours', self)
        self.actionVoirParcours.setShortcut('Ctrl+O')
        self.actionVoirParcours.setStatusTip('Voir les parcours de la tournee (Ctrl+O)')
        self.actionVoirParcours.triggered.connect(lambda : self.voirParcours(self.selectedTournee))
        self.actionExporterKml = QtGui.QAction('Exporter Kml', self)
        self.actionExporterKml.setShortcut('Ctrl+K')
        self.actionExporterKml.setStatusTip('Exporter la tournee Kml pour visualiser avec google map (Ctrl+K)')
        self.actionExporterKml.triggered.connect(lambda : self.exporterKml(self.selectedTournee)) 

    def selTourneeChanged(self, tournee):
        '''la selection du tournee a changee
        modification des actions toolbar'''
        self.selectedTournee=tournee
        self.refreshToolBar()  

    def refreshToolBar(self):
        '''modification des actions toolbar'''
        self.parent.toolBar.clear()
        self.parent.toolBar.addAction(self.actionNouvelleTournee)
        if self.selectedTournee:
            self.parent.toolBar.addAction(self.actionSupprimerTournee)
            self.parent.toolBar.addAction(self.actionVoirParcours)
            self.parent.toolBar.addAction(self.actionExporterKml)

    def voirParcours(self, tournee):    
        self.parent.fenetreParcours.tournee=tournee
        self.parent.fenetreParcours.modelParcours.tourneeChanged()
        self.parentTab.setCurrentIndex(1)
        self.parent.fenetreParcours._initAction()
        
    def nouvelleTournee(self):
        """ajoute un nouveau tournee vierge"""
        nouv_tournee=self.mere.nouvTournee(insert=True)
        self.modelTournee.ajouterTournee(nouv_tournee)
        
    def supprimerTournee(self, tournee):
        """Editer Tournee"""
        pass
 
    def exporterKml(self, tournee):
        Kml(racine=tournee, nom='truc.kml')
        

class FenetreParcours(Fenetre):
    """fenetre Parcours"""
    
    def createModel(self):
         self.modelParcours=ModelParcours(parent=self,mere=self.mere)
         self.viewParcours.setModel(self.modelParcours)
         
    def createFenetre(self):
         self.viewParcours=ViewParcours(parent=self,mere=self.mere)   
         layContratTable = QtGui.QGridLayout()
         layContratTable.addWidget(self.viewParcours,0,0,2,4) 
         self.setLayout(layContratTable)
         
    def _initNext(self, **arguments):
        self.tournee=arguments.get('tournee')
        self.selectedParcours=None

    def _initAction(self):
        self.parent.toolBar.clear()
        self.parent.toolBar.addAction(self.actionNouveauParcours)
        self.parent.toolBar.addAction(self.actionSupprimerParcours)
        
    def createConnection(self):
        selModelParcours=self.viewParcours.selectionModel()
        selModelParcours.currentChanged.connect(lambda :self.selParcoursChanged(parcours=self.modelParcours.data(self.viewParcours.currentIndex(),QtCore.Qt.UserRole)))

    def createAction(self):
        self.actionNouveauParcours = QtGui.QAction('Nouveau parcours', self)
        self.actionNouveauParcours.setShortcut('Ctrl+N')
        self.actionNouveauParcours.setStatusTip('Creer un nouveau parcours (Ctrl+N)')
        self.actionNouveauParcours.triggered.connect(self.nouveauParcours)
        self.actionSupprimerParcours = QtGui.QAction('Supprimer parcours', self)
        self.actionSupprimerParcours.setShortcut('Ctrl+S')
        self.actionSupprimerParcours.setStatusTip('Supprimer parcours (Ctrl+S)')
        self.actionSupprimerParcours.triggered.connect(lambda : self.supprimerParcours(self.selectedParcours))

    def refreshToolBar(self):
        '''modification des actions toolbar'''
        self.parent.toolBar.clear()
        self.parent.toolBar.addAction(self.actionNouveauParcours)
        if self.selectedParcours:
            self.parent.toolBar.addAction(self.actionSupprimerParcours)

    def selParcoursChanged(self, parcours):
        '''la selection du Parcours a changee
        modification des actions toolbar'''
        self.selectedParcours=parcours
        self.refreshToolBar() 

    def nouveauParcours(self):
        nouv_parcours=self.mere.nouvParcours(insert=True)
        self.tournee.ajouterParcours(nouv_parcours)
        self.modelParcours.ajouterParcours(nouv_parcours)
                
    def supprimerParcours(self, parcours):
        self.modelParcours.supprimerParcours(parcours)
        parcours.supprimer() 
         
class FenetreDepotLieuQuantite(Fenetre):
    """fenetre Edition des quantités DepotLieu"""

    def _initNext(self,**arguments):
        self.kobjet=arguments.get('kobjet')
        if self.kobjet:self.modelDepotLieuQuantite.ajouterObjet(self.kobjet)        
    
    def createFenetre(self):
        self.viewDepotLieuQuantite=ViewDepotLieuQuantite(parent=self,mere=self.mere)       
        self.boutSuppDepot= QtGui.QPushButton("Supprimer", parent=self)
        self.boutNouvDepot= QtGui.QPushButton("Nouveau", parent=self)
        layTable = QtGui.QGridLayout()
        layTable.addWidget(self.boutNouvDepot,0,0,1,1)
        layTable.addWidget(self.boutSuppDepot,0,1,1,1)
        layTable.addWidget(self.viewDepotLieuQuantite,1,0,5,3)  
#        layEditContrat.setStretchFactor(layTable, 2)                        
        self.setLayout(layTable)

    def createModel(self):
        self.modelDepotLieuQuantite=ModelDepotLieuQuantite(parent=self,mere=self.mere)
        self.viewDepotLieuQuantite.setModel(self.modelDepotLieuQuantite) 
        
    def createConnection(self):
        self.viewDepotLieuQuantite.horizontalHeader().sectionDoubleClicked.connect(self.editDepot)
        self.boutNouvDepot.clicked.connect(self.nouvDepot)
        self.boutSuppDepot.clicked.connect(self.suppDepot)
          
    def editDepot(self,index_colonne):
        if index_colonne != -1:
            depot=self.modelDepotLieuQuantite.listDepot[index_colonne]
            fenetreEditDepot=FenetreEditDepot(parent=self,mere=self.mere,depot=depot)
            fenetreEditDepot.setWindowFlags(QtCore.Qt.Window)
            fenetreEditDepot.show()
                            
    def nouvDepot(self):
        nouv_depot=self.mere.nouvDepot(insert=False)
        self.modelDepotLieuQuantite.ajouterDepot(nouv_depot)
        fenetreEditDepot=FenetreEditDepot(parent=self,mere=self.mere,depot=nouv_depot)
        fenetreEditDepot.setWindowFlags(QtCore.Qt.Window)
        fenetreEditDepot.show()
            
    def suppDepot(self):
        if self.selectedDepot:
            self.modelQuantiteDepotLieu.retirerDepot(self.selectedDepot)
            self.modelQuantiteDepotLieu.contrat.supprimerDepot(self.selectedDepot)
        
 
 
  
class FenetreEditDepot(Fenetre):
    """fenetre Edition Depot"""
         
    def _initNext(self,**arguments):
        self.depot=arguments.get('depot')
        if self.depot:self.initDepot()
        
    def initDepot(self, depot=None):
        if depot:self.depot=depot
        self.labelDbid.setText(str(self.depot.dbid))
        self.textNom.setText(self.depot.nom)
        self.textSurnom.setText(self.depot.surnom)
        self.spinQuantite.setValue(self.depot.quantite)
        self.spinVolume.setValue(self.depot.volume)
        self.spinPoid.setValue(self.depot.poid)
        self.spinPrix.setValue(self.depot.prix)
        self.textRemarque.setText(self.depot.remarque)
        self.spinNbCarton.setValue(self.depot.nb_carton)
        self.spinNbPaquet.setValue(self.depot.nb_paquet)

        for genre in self.mere.genresdepots_tb.data_arg['genre']:
            self.comboGenre.addItem(genre)
        self.comboGenre.setEditText(self.depot.genre)
          
    def createFenetre(self):       
        self.boutOkDepot= QtGui.QPushButton("Ok", parent=self)
        self.boutAnnDepot= QtGui.QPushButton("Annuler", parent=self)
        self.labelDbid=QtGui.QLabel('Dbid')
        self.labelNom=QtGui.QLabel('Nom')
        self.labelSurnom=QtGui.QLabel('Surnom')
        self.labelVolume=QtGui.QLabel('Volume')
        self.labelPoid=QtGui.QLabel('Poid')
        self.labelPrix=QtGui.QLabel('Prix')
        self.labelRemarque=QtGui.QLabel('Remarque')
        self.labelNbCarton=QtGui.QLabel('Nb carton')
        self.labelNbPaquet=QtGui.QLabel('Nb paquet')
        self.labelGenre=QtGui.QLabel('Genre')
        self.labelQuantite=QtGui.QLabel('Quantite')
        self.label2Dbid=QtGui.QLabel()
        self.textNom=QtGui.QLineEdit()
        self.textSurnom=QtGui.QLineEdit()
        self.spinQuantite=QtGui.QSpinBox()
        self.spinVolume=QtGui.QDoubleSpinBox()
        self.spinPoid=QtGui.QDoubleSpinBox()
        self.spinPrix=QtGui.QDoubleSpinBox()
        self.textRemarque=QtGui.QLineEdit()
        self.spinNbCarton=QtGui.QSpinBox()
        self.spinNbPaquet=QtGui.QSpinBox()
        self.comboGenre=QtGui.QComboBox()        
        self.labelDbid.setBuddy(self.label2Dbid)
        self.labelNom.setBuddy(self.textNom)
        self.labelSurnom.setBuddy(self.textSurnom)
        self.labelQuantite.setBuddy(self.spinQuantite)
        self.labelVolume.setBuddy(self.spinVolume)
        self.labelPoid.setBuddy(self.spinPoid)
        self.labelPrix.setBuddy(self.spinPrix)
        self.labelRemarque.setBuddy(self.textRemarque)
        self.labelNbCarton.setBuddy(self.spinNbCarton)
        self.labelNbPaquet.setBuddy( self.spinNbPaquet)
        self.labelGenre.setBuddy( self.comboGenre)
        layDepot = QtGui.QGridLayout()
        layDepot.addWidget(self.labelDbid,0,0,1,1)
        layDepot.addWidget(self.labelNom,1,0,1,1)
        layDepot.addWidget(self.labelSurnom,2,0,1,1)
        layDepot.addWidget(self.labelQuantite,3,0,1,1)
        layDepot.addWidget(self.labelVolume,4,0,1,1)
        layDepot.addWidget(self.labelPoid,5,0,1,1)
        layDepot.addWidget(self.labelPrix,6,0,1,1)
        layDepot.addWidget(self.labelRemarque,7,0,1,1)
        layDepot.addWidget(self.labelNbCarton,8,0,1,1)
        layDepot.addWidget(self.labelNbPaquet,9,0,1,1)
        layDepot.addWidget(self.labelGenre,11,0,1,1)
        layDepot.addWidget(self.label2Dbid,0,1,1,1)
        layDepot.addWidget(self.textNom,1,1,1,1)
        layDepot.addWidget(self.textSurnom,2,1,1,1)
        layDepot.addWidget(self.spinQuantite,3,1,1,1)
        layDepot.addWidget(self.spinVolume,4,1,1,1)
        layDepot.addWidget(self.spinPoid,5,1,1,1)
        layDepot.addWidget(self.spinPrix,6,1,1,1)
        layDepot.addWidget(self.textRemarque,7,1,1,1)
        layDepot.addWidget(self.spinNbCarton,8,1,1,1)
        layDepot.addWidget(self.spinNbPaquet,9,1,1,1)
        layDepot.addWidget(self.comboGenre,11,1,1,1)
        layDepot.addWidget(self.boutOkDepot,12,0,1,1)
        layDepot.addWidget(self.boutAnnDepot,12,1,1,1)
        self.setLayout(layDepot)
          
    def createConnection(self):
        self.boutAnnDepot.clicked.connect(self.annDepot) 
        self.boutOkDepot.clicked.connect(self.okDepot)
          
    def annDepot(self):
        self.close()
          
    def okDepot(self):
        if not self.depot.dbid:
            self.depot.sqlInsert()
        self.depot.nom=self.textNom.text()
        self.depot.surnom=self.textSurnom.text()
        self.depot.volume=self.spinVolume.value()
        self.depot.quantite=self.spinQuantite.value()
        self.depot.poid=self.spinPoid.value()
        self.depot.prix_unite=self.spinPrix.value()
        self.depot.remarque=self.textRemarque.text()
        self.depot.nb_carton=self.spinNbCarton.value()
        self.depot.nb_paquet=self.spinNbPaquet.value()
        self.depot.genre=self.comboGenre.currentText()
        ind=self.parent.modelDepotLieuQuantite.listDepot.index(self.depot)
        self.parent.modelDepotLieuQuantite.headerDataChanged.emit(QtCore.Qt.Horizontal,ind,ind)
        self.close()
         
        
class FenetreSelectLieu(Fenetre):
    """fenetre de selection des lieux"""
#     def createModel(self):
#         self.modelSelectLieu1=selectLieuModel(parent=self,mere=self.mere)
#         self.tableSelectLieu1.setModel(self.modelSelectLieu1)
#         self.modelSelectLieu2=selectLieuModel(parent=self,mere=self.mere)
#         self.tableSelectLieu2.setModel(self.modelSelectLieu2)      
#            
#     def createFenetre(self):
#         self.tableSelectLieu1=selectLieuView(parent=self,mere=self.mere)
#         self.tableSelectLieu2=selectLieuView(parent=self,mere=self.mere)
#          
#         self.boutAjouterGD= QtGui.QPushButton("-->", parent=self)
#         self.boutAjouterDG= QtGui.QPushButton("<--", parent=self)
#         self.boutDesafecter= QtGui.QPushButton("Desafecter", parent=self)
#          
#         lay = QtGui.QGridLayout()
#         lay.addWidget(self.tableSelectLieu1,0,0,8,5)
#         lay.addWidget(self.tableSelectLieu2,0,7,8,5)
#         lay.addWidget(self.boutAjouterGD,3,6,1,1)
#         lay.addWidget(self.boutAjouterDG,4,6,1,1)
#         lay.addWidget(self.boutDesafecter,5,6,1,1)
#         self.setLayout(lay)
    
class FenetreEditLieuDB(Fenetre):
    """fenetre edition lieux data-base"""    
    
    def _initNext(self,**arguments):
        self.lieu=arguments.get('lieu',self.mere.nouvLieu(insert=False,adresse="Nouvelle adresse",cp=75000))
        self.textNom.setText(self.lieu.nom)
        self.textPertinence.setText(str(self.lieu.pertinence))
        self.textComment.setText(self.lieu.commentaire)
        for genre in self.mere.genreslieux_tb.data_arg['genre']:
            if isinstance(genre,int):genre=str(genre)
            self.comboGenre.addItem(genre)
        self.comboGenre.setEditText(self.lieu.genre)
        self.comboGenre.model().sort(0,QtCore.Qt.AscendingOrder)
        self.initComboAdresse()

    def createFenetre(self):
        self.labelNom=QtGui.QLabel("Nom",parent=self)
        self.textNom=QtGui.QLineEdit("Sans Nom",parent=self)
        self.labelNom.setBuddy( self.textNom)     
        
        self.labelAdresse=QtGui.QLabel("Adresse",parent=self)
        self.comboAdresse=QtGui.QComboBox(parent=self)
        self.labelAdresse.setBuddy(self.comboAdresse)  
        
        self.checkPricipal=QtGui.QCheckBox("Principale", parent=self)
        self.boutNouv= QtGui.QPushButton("Nouveau",parent=self)
        self.boutSupp= QtGui.QPushButton("Supprimer",parent=self)
        self.boutEdit= QtGui.QPushButton("Editer",parent=self)  
      
        self.labelGenre=QtGui.QLabel("Genre",parent=self)
        self.comboGenre=QtGui.QComboBox(parent=self)
        self.labelGenre.setBuddy(self.comboGenre)       
        
        self.labelPertinence=QtGui.QLabel("Pertinence",parent=self)
        self.textPertinence=QtGui.QLineEdit("0",parent=self)
        self.labelPertinence.setBuddy( self.textPertinence)
        
        self.labelComment=QtGui.QLabel("Commentaire",parent=self)
        self.textComment=QtGui.QTextEdit("Sans commentaire",parent=self)
        self.labelComment.setBuddy(self.textComment)
         
        self.boutOk= QtGui.QPushButton("Ok",parent=self)
        self.boutAnn= QtGui.QPushButton("Annuler",parent=self)
        lay = QtGui.QGridLayout()
        lay.addWidget(self.labelNom,0,0,1,1)
        lay.addWidget(self.textNom,0,1,1,1)
        lay.addWidget(self.labelAdresse,1, 0,1,1)
        lay.addWidget(self.comboAdresse, 1,1,1,2)
        lay.addWidget(self.checkPricipal, 1,5,1,1)
        lay.addWidget(self.boutNouv,1,6,1,1)
        lay.addWidget(self.boutSupp,1,7,1,1)        
        lay.addWidget(self.boutEdit,1,8,1,1)         
        lay.addWidget(self.labelGenre,2,0,1,1)
        lay.addWidget(self.comboGenre, 2,1,1,1)
        lay.addWidget(self.labelPertinence,3,0,1,1)
        lay.addWidget(self.textPertinence,3,1,1,1)        
        lay.addWidget(self.labelComment,4,0,1,1)
        lay.addWidget(self.textComment,4,1,2,1)
        lay.addWidget(self.boutOk,7,6,1,1)
        lay.addWidget(self.boutAnn,7,7,1,1)
        self.setLayout(lay)  

    def comboAdresseChanged(self, index):
        self.lieu.adresseProvisoire=self.lieu.listAdresse[index]
        if self.lieu.adresseProvisoire.principale==1:
            self.checkPricipal.setChecked(True)
        else:self.checkPricipal.setChecked(False)
            
    def checkPricipalChanged(self, state):
        if state==QtCore.Qt.Checked:
            for adresse in self.lieu.listAdresse:adresse.principale=0
            self.lieu.adresseProvisoire.principale=1
        else:
            self.lieu.adresseProvisoire.principale=0
            self.lieu.listAdresse[0].principale=1
            
    def createConnection(self):
        self.boutOk.clicked.connect(self.ok)
        self.boutEdit.clicked.connect(self.editAdresse)
        self.boutNouv.clicked.connect(self.nouvAdresse)
        self.boutAnn.clicked.connect(self.ann)
        self.comboAdresse.currentIndexChanged.connect(self.comboAdresseChanged)
        self.checkPricipal.stateChanged.connect(self.checkPricipalChanged)

    def initComboAdresse(self):
        self.comboAdresse.clear()
        for adresse in self.lieu.listAdresse:
            self.comboAdresse.addItem("{} - {} - {}".format(adresse.adresse, adresse.cp, adresse.ville))
     
    def nouvAdresse(self):
        add=self.mere.nouvAdresse()
        self.lieu.adresse=add
        self.initComboAdresse()

    def editAdresse(self):
        if self.lieu.adresse:
            self.fenetreEditAdresse=FenetreEditAdresseDB(parent=self,mere=self.mere,lieu=[self.lieu])
            self.fenetreEditAdresse.setWindowFlags(QtCore.Qt.Window)
            if self.fenetreEditAdresse.show():print("well")

    def ok(self):
        self.lieu.nom=self.textNom.text()
        self.lieu.pertinence=self.textPertinence.text()
        self.lieu.commentaire=self.textComment.toPlainText()
        self.lieu.genre=self.comboGenre.currentText()
        self.lieu.sqlInsert()
        self.close()
        
    def ann(self):
        self.close()

    
class FenetreLieuDB(Fenetre):
    """fenetre lieux data-base"""
    def _initNext(self,**arguments):
        self._selectionLieu=None
    
    def createModel(self):
        self.modelLieuDB=ModelLieuDB(parent=self,mere=self.mere)
        self.modelProxyLieuDB=QtGui.QSortFilterProxyModel(parent=self)
        self.modelProxyLieuDB.setSourceModel(self.modelLieuDB)
        self.modelProxyLieuDB.setDynamicSortFilter(True)
        self.viewTableLieuDB.setModel(self.modelProxyLieuDB)  
        self.selectModelProxyLieuDB=self.viewTableLieuDB.selectionModel()
  
    def createFenetre(self):
        self.viewTableLieuDB=ViewLieuDB(parent=self,mere=self.mere)
        self.boutNouv= QtGui.QPushButton("Nouveau",parent=self)
        self.boutEdit= QtGui.QPushButton("Editer",parent=self)
        self.boutSupp= QtGui.QPushButton("Supprimer",parent=self)
        self.boutFusion= QtGui.QPushButton("Fusionner",parent=self)
        self.labelRechecher=QtGui.QLabel("Rechercher",parent=self)
        self.textRechercher=QtGui.QLineEdit()
        self.labelRechecher.setBuddy(self.textRechercher)
        self.labelComment=QtGui.QLabel("Commentaire", parent=self)
        lay = QtGui.QGridLayout()
        lay.addWidget(self.viewTableLieuDB,0,0,8,8)
        lay.addWidget(self.boutNouv,9,4,1,1)
        lay.addWidget(self.boutEdit,9,5,1,1)        
        lay.addWidget(self.boutSupp,9,6,1,1)
        lay.addWidget(self.boutFusion, 9,7,1,1)
        lay.addWidget(self.labelRechecher,9,0,1,1)
        lay.addWidget(self.textRechercher,9,1,1,2)
        lay.addWidget(self.labelComment,10,0,2,8)
        self.setLayout(lay)
          
    def createConnection(self):
        self.boutNouv.clicked.connect(self.nouvLieu)
        self.boutEdit.clicked.connect(self.editLieu)
        self.textRechercher.textChanged.connect(self.rechercher)
        self.selectModelProxyLieuDB.currentChanged.connect(self.selectLieu)

        
    def selectLieu(self, a, b):
        #self._selectionLieu= self.modelLieuDB.data(self.modelProxyLieuDB.mapToSource(a), QtCore.Qt.UserRole)
        self._selectionLieu=self.modelProxyLieuDB.data(a,QtCore.Qt.UserRole)
        print(self._selectionLieu)
        
          
    def nouvLieu(self):
        self.fenetreEditLieu=FenetreEditLieuDB(parent=self,mere=self.mere,lieu=self.mere.nouvLieu(insert=False,adresse="Nouvelle adresse",cp=75000))
        self.fenetreEditLieu.setWindowFlags(QtCore.Qt.Window)
        if self.fenetreEditLieu.show():
            self.modelLieuDB.ajouterLieu()

    def editLieu(self):
        self.fenetreEditLieu=FenetreEditLieuDB(parent=self,mere=self.mere,lieu=self._selectionLieu)
        self.fenetreEditLieu.setWindowFlags(QtCore.Qt.Window)
        self.fenetreEditLieu.show()

    def suppLieu(self):
        pass
          
    def rechercher(self,texte):
        texte_user=texte.lower()
        self.modelLieuDB.rechercher(texte=texte_user)
 
         
class FenetreClient(Fenetre):
    """fenetre Client"""
    
    def createModel(self):
        self.modelClient=ModelClient(parent=self,mere=self.mere)
        self.viewClient.setModel(self.modelClient)
        self.selectModelClient=self.viewClient.selectionModel()
         
    def createFenetre(self):
        self.viewClient=ViewClient(parent=self,mere=self.mere)
        layClientTable = QtGui.QGridLayout()
        layClientTable.addWidget(self.viewClient,0,0,8,4)      
        self.setLayout(layClientTable)   

    def _initNext(self, **arguments):
        self.selectedClient=None
        
    def createConnection(self):
        self.viewClient.doubleClicked.connect(self.actionVoirContrat.trigger)
        selModelClient=self.viewClient.selectionModel()
        selModelClient.currentChanged.connect(lambda :self.selClientChanged(client=self.modelClient.data(self.viewClient.currentIndex(),QtCore.Qt.UserRole)))

    def createAction(self):
        self.actionNouveauClient = QtGui.QAction('Nouveau client', self)
        self.actionNouveauClient.setShortcut('Ctrl+N')
        self.actionNouveauClient.setStatusTip('Creer un nouveau client (Ctrl+N)')
        self.actionNouveauClient.triggered.connect(self.nouveauClient)
        self.actionEditerClient = QtGui.QAction('Editer client', self)
        self.actionEditerClient.setShortcut('Ctrl+E')
        self.actionEditerClient.setStatusTip('Editer client (Ctrl+E)')
        self.actionEditerClient.triggered.connect(lambda : self.editerClient(self.selectedClient))
        self.actionSupprimerClient = QtGui.QAction('Supprimer client', self)
        self.actionSupprimerClient.setShortcut('Ctrl+S')
        self.actionSupprimerClient.setStatusTip('Supprimer client (Ctrl+S)')
        self.actionSupprimerClient.triggered.connect(lambda : self.supprimerClient(self.selectedClient))
        self.actionVoirContrat = QtGui.QAction('Voir contrats', self)
        self.actionVoirContrat.setShortcut('Ctrl+O')
        self.actionVoirContrat.setStatusTip('Voir les contrats du client (Ctrl+O)')
        self.actionVoirContrat.triggered.connect(lambda : self.voirContrat(self.selectedClient))

    def selClientChanged(self, client):
        '''la selection du client a changee'''
        self.selectedClient=client
        self.refreshToolBar()

    def refreshToolBar(self):
        '''modification des actions toolbar'''
        self.parent.toolBar.clear()
        self.parent.toolBar.addAction(self.actionNouveauClient)
        if self.selectedClient:
            self.parent.toolBar.addAction(self.actionEditerClient)
            self.parent.toolBar.addAction(self.actionSupprimerClient)
            self.parent.toolBar.addAction(self.actionVoirContrat)

    def voirContrat(self, client):    
        self.parent.fenetreContrat.client=client
        self.parent.fenetreContrat.modelContrat.clientChanged()
        self.parentTab.setCurrentIndex(1)
        self.parent.fenetreContrat._initAction()
        
    def nouveauClient(self):
        """ajoute un nouveau client vierge"""
        nouv_client=self.mere.nouvClient(insert=False)
        self.editerClient(nouv_client)
        
    def editerClient(self, client):
        """Editer Client"""
        self.fenetreEditClient=FenetreEditClient(parent=self,mere=self.mere,client=client)
        self.fenetreEditClient.setWindowFlags(QtCore.Qt.Window)
        self.fenetreEditClient.show()
        
    def supprimerClient(self, client):
        """Editer Client"""
        pass


class FenetreEditClient(Fenetre):
    """fenetre Edition Client"""
    
    def _initNext(self,**arguments):
        self.client=arguments.get('client',self.mere.nouvClient(insert=False))
        self.textNom.setText(self.client.nom)
        self.textSurnom.setText(self.client.surnom)
        for genre in self.mere.genresclients_tb.data_arg['genre']:
            if isinstance(genre,int):genre=str(genre)
            self.comboGenre.addItem(genre)
        self.comboGenre.setEditText(self.client.genre)
        self.comboGenre.model().sort(0,QtCore.Qt.AscendingOrder)

    def createFenetre(self):
        self.labelNom=QtGui.QLabel("Nom",parent=self)
        self.textNom=QtGui.QLineEdit("Sans Nom",parent=self)
        self.labelNom.setBuddy( self.textNom)     
        self.labelSurnom=QtGui.QLabel("Surnom",parent=self)
        self.textSurnom=QtGui.QLineEdit("Sans Surnom",parent=self)
        self.labelSurnom.setBuddy( self.textSurnom)  
        self.labelGenre=QtGui.QLabel("Genre",parent=self)
        self.comboGenre=QtGui.QComboBox(parent=self)
        self.labelGenre.setBuddy(self.comboGenre)    
        self.boutOk= QtGui.QPushButton("Ok",parent=self)
        self.boutAnn= QtGui.QPushButton("Annuler",parent=self)
        lay = QtGui.QGridLayout()
        lay.addWidget(self.labelNom,0,0,1,1)
        lay.addWidget(self.textNom,0,1,1,1)
        lay.addWidget(self.labelSurnom,1, 0,1,1)
        lay.addWidget(self.textSurnom, 1,1,1,2)      
        lay.addWidget(self.labelGenre,2,0,1,1)
        lay.addWidget(self.comboGenre, 2,1,1,1)
        lay.addWidget(self.boutOk,4,1,1,1)
        lay.addWidget(self.boutAnn,4,2,1,1)
        self.setLayout(lay)  
            
    def createConnection(self):
        self.boutOk.clicked.connect(self.ok)
        self.boutAnn.clicked.connect(self.ann)

    def ok(self):
        self.client.nom=self.textNom.text()
        self.client.surnom=self.textSurnom.text()
        self.client.genre=self.comboGenre.currentText()
        if self.client.sqlInsert():
            self.parent.modelClient.ajouterClient(self.client)
        self.close()
        
    def ann(self):
        self.close()


class FenetreEditPedaleur(Fenetre):
    """fenetre Edition Pedaleur"""
    
    def _initNext(self,**arguments):
        self.pedaleur=arguments.get('pedaleur',self.mere.nouvPedaleur(insert=False))
        self.textNom.setText(self.pedaleur.nom)
        self.textSurnom.setText(self.pedaleur.surnom)
        self.textPrenom.setText(self.pedaleur.prenom)
        self.comboCouleur.setCurrentIndex(self.comboCouleur.color_list.index(self.pedaleur.couleur))

    def createFenetre(self):
        self.labelNom=QtGui.QLabel("Nom",parent=self)
        self.textNom=QtGui.QLineEdit("Sans Nom",parent=self)
        self.labelNom.setBuddy( self.textNom)     
        self.labelPrenom=QtGui.QLabel("Prenom",parent=self)
        self.textPrenom=QtGui.QLineEdit("Sans Prenom",parent=self)
        self.labelPrenom.setBuddy( self.textPrenom) 
        self.labelSurnom=QtGui.QLabel("Surnom",parent=self)
        self.textSurnom=QtGui.QLineEdit("Sans Surnom",parent=self)
        self.labelSurnom.setBuddy( self.textSurnom)          
        self.labelCouleur=QtGui.QLabel("Couleur",parent=self)
        self.comboCouleur=KComboBoxCouleur(parent=self)
        self.labelCouleur.setBuddy(self.comboCouleur)    
        self.boutOk= QtGui.QPushButton("Ok",parent=self)
        self.boutAnn= QtGui.QPushButton("Annuler",parent=self)
        lay = QtGui.QGridLayout()
        lay.addWidget(self.labelNom,0,0,1,1)
        lay.addWidget(self.textNom,0,1,1,1)
        lay.addWidget(self.labelPrenom,1, 0,1,1)
        lay.addWidget(self.textPrenom, 1,1,1,2)         
        lay.addWidget(self.labelSurnom,2, 0,1,1)
        lay.addWidget(self.textSurnom, 2,1,1,2)      
        lay.addWidget(self.labelCouleur,3,0,1,1)
        lay.addWidget(self.comboCouleur, 3,1,1,1)
        lay.addWidget(self.boutOk,5,1,1,1)
        lay.addWidget(self.boutAnn,5,2,1,1)
        self.setLayout(lay)  
            
    def createConnection(self):
        self.boutOk.clicked.connect(self.ok)
        self.boutAnn.clicked.connect(self.ann)

    def ok(self):
        self.pedaleur.nom=self.textNom.text()
        self.pedaleur.prenom=self.textPrenom.text()
        self.pedaleur.surnom=self.textSurnom.text()
        self.pedaleur.couleur= self.comboCouleur.color_list[self.comboCouleur.currentIndex()]
        if self.pedaleur.sqlInsert():
            self.parent.modelPedaleur.ajouterPedaleur(self.pedaleur)
            print("insertion pedaleur")
        self.close()
        
    def ann(self):
        self.close()


class FenetreContrat(Fenetre):
    """fenetre Contrat"""
    
    def createModel(self):
        self.modelContrat=ModelContrat(parent=self,mere=self.mere)
        self.viewContrat.setModel(self.modelContrat)
         
    def createFenetre(self):
        self.viewContrat=ViewContrat(parent=self,mere=self.mere)
        self.comboGenre=QtGui.QComboBox(parent=self)      
        layContratTable = QtGui.QGridLayout()
        layContratTable.addWidget(self.comboGenre,0,0,1,1)
        layContratTable.addWidget(self.viewContrat,1,0,2,4) 
        self.setLayout(layContratTable)
         
    def _initNext(self, **arguments):
        self.client=arguments.get('client')
        self.selectedContrat=None
        for genre in self.mere.genrescontrats_tb.data_arg['genre']:
            if isinstance(genre,int):genre=str(genre)
            self.comboGenre.addItem(genre)
          
    def _initAction(self):
        self.parent.toolBar.clear()
        self.parent.toolBar.addAction(self.actionNouveauContrat)
    
    def createConnection(self):
        self.comboGenre.currentIndexChanged.connect(self.genreContratChanged)
        selModelContrat=self.viewContrat.selectionModel()
        selModelContrat.currentChanged.connect(lambda :self.selContratChanged(contrat=self.modelContrat.data(self.viewContrat.currentIndex(),QtCore.Qt.UserRole)))

    def createAction(self):
        self.actionNouveauContrat = QtGui.QAction('Nouveau contrat', self)
        self.actionNouveauContrat.setShortcut('Ctrl+N')
        self.actionNouveauContrat.setStatusTip('Creer un nouveau contrat (Ctrl+N)')
        self.actionNouveauContrat.triggered.connect(self.nouveauContrat)
        self.actionEditerContrat = QtGui.QAction('Editer contrat', self)
        self.actionEditerContrat.setShortcut('Ctrl+E')
        self.actionEditerContrat.setStatusTip('Editer contrat (Ctrl+E)')
        self.actionEditerContrat.triggered.connect(lambda : self.editerContrat(self.selectedContrat))
        self.actionSupprimerContrat = QtGui.QAction('Supprimer contrat', self)
        self.actionSupprimerContrat.setShortcut('Ctrl+S')
        self.actionSupprimerContrat.setStatusTip('Supprimer contrat (Ctrl+S)')
        self.actionSupprimerContrat.triggered.connect(lambda : self.supprimerContrat(self.selectedContrat))
        self.actionEditerDepotLieu = QtGui.QAction('Editer Depot/Lieu', self)
        self.actionEditerDepotLieu.setShortcut('Ctrl+D')
        self.actionEditerDepotLieu.setStatusTip('Editer les depots et les lieux du contrat (Ctrl+D)')
        self.actionEditerDepotLieu.triggered.connect(lambda : self.editerDepotQuantite(self.selectedContrat))
        self.actionExporterKml = QtGui.QAction('Exporter Kml', self)
        self.actionExporterKml.setShortcut('Ctrl+K')
        self.actionExporterKml.setStatusTip('Exporter le contrat Kml pour visualiser avec google map (Ctrl+K)')
        self.actionExporterKml.triggered.connect(lambda : self.exporterKml(self.selectedContrat))        
        self.actionImporterCVS = QtGui.QAction('Importer CVS', self)
        self.actionImporterCVS.setShortcut('Ctrl+O')
        self.actionImporterCVS.setStatusTip('Importer un fichier CSV (Ctrl+O)')
        self.actionImporterCVS.triggered.connect(lambda : self.importListing(self.selectedContrat))

    def selContratChanged(self, contrat):
        '''la selection du contrat a changee'''
        self.selectedContrat=contrat
        self.refreshToolBar()
                
    def refreshToolBar(self):
        '''modification des actions toolbar'''
        self.parent.toolBar.clear()
        self.parent.toolBar.addAction(self.actionNouveauContrat)
        if self.selectedContrat:
            self.parent.toolBar.addAction(self.actionEditerContrat)
            self.parent.toolBar.addAction(self.actionSupprimerContrat)
            if self.selectedContrat.listDepot:
                self.parent.toolBar.addAction(self.actionEditerDepotLieu)
                self.parent.toolBar.addAction(self.actionExporterKml)
            else: 
                self.parent.toolBar.addAction(self.actionImporterCVS)
       
    def genreContratChanged(self):
        genre=self.comboGenre.currentText()
        self.modelContrat._genreContrat=genre
        self.modelContrat.clientChanged() 

    def nouveauContrat(self):
        nouv_contrat=self.mere.nouvContrat(insert=False)
        nouv_contrat.switchContrat(genre=self.comboGenre.currentText())
        self.editerContrat(nouv_contrat)
         
    def editerContrat(self, contrat):
        self.fenetreEditContrat=FenetreEditContrat(parent=self,mere=self.mere,contrat=contrat)
        self.fenetreEditContrat.setWindowFlags(QtCore.Qt.Window)
        self.fenetreEditContrat.show()        

    def importListing(self, contrat):
        """import listing Dock CSV"""
        self.fenetreImportListing=FenetreImportListing(parent=self,mere=self.mere,contrat=contrat)
        self.fenetreImportListing.setWindowFlags(QtCore.Qt.Window)
        self.fenetreImportListing.show()
             
    def editerDepotQuantite(self, contrat):
        """lancement fenetre edition depot lieux quantitee"""
        self.fenetreDepotLieuQuantite=FenetreDepotLieuQuantite(parent=self,mere=self.mere,kobjet=contrat)
        self.fenetreDepotLieuQuantite.setWindowFlags(QtCore.Qt.Window)
        self.fenetreDepotLieuQuantite.show()        

    def exporterKml(self, contrat):
        contrat.kmlConstructeur()
        
        
class FenetrePedaleur(Fenetre):
    """fenetre Pedaleur"""
    
    def createModel(self):
        self.modelPedaleur=ModelPedaleur(parent=self,mere=self.mere)
        self.viewPedaleur.setModel(self.modelPedaleur)

    def createFenetre(self):
        self.viewPedaleur=ViewPedaleur(parent=self,mere=self.mere)
        layPedaleurTable = QtGui.QGridLayout()
        layPedaleurTable.addWidget(self.viewPedaleur,0,0,8,4)      
        self.setLayout(layPedaleurTable)   

    def _initNext(self, **arguments):
        self.selectedPedaleur=None
        
    def createConnection(self):
        selModelPedaleur=self.viewPedaleur.selectionModel()
        selModelPedaleur.currentChanged.connect(lambda :self.selPedaleurChanged(pedaleur=self.modelPedaleur.data(self.viewPedaleur.currentIndex(),QtCore.Qt.UserRole)))

    def createAction(self):
        self.actionNouveauPedaleur = QtGui.QAction('Nouveau pedaleur', self)
        self.actionNouveauPedaleur.setShortcut('Ctrl+N')
        self.actionNouveauPedaleur.setStatusTip('Creer un nouveau pedaleur (Ctrl+N)')
        self.actionNouveauPedaleur.triggered.connect(self.nouveauPedaleur)
        self.actionEditerPedaleur = QtGui.QAction('Editer pedaleur', self)
        self.actionEditerPedaleur.setShortcut('Ctrl+E')
        self.actionEditerPedaleur.setStatusTip('Editer pedaleur (Ctrl+E)')
        self.actionEditerPedaleur.triggered.connect(lambda : self.editerPedaleur(self.selectedPedaleur))
        self.actionSupprimerPedaleur = QtGui.QAction('Supprimer pedaleur', self)
        self.actionSupprimerPedaleur.setShortcut('Ctrl+S')
        self.actionSupprimerPedaleur.setStatusTip('Supprimer pedaleur (Ctrl+S)')
        self.actionSupprimerPedaleur.triggered.connect(lambda : self.supprimerPedaleur(self.selectedPedaleur))

    def selPedaleurChanged(self, pedaleur):
        '''la selection du Pedaleur a changee
        modification des actions toolbar'''
        self.selectedPedaleur=pedaleur
        self.refreshToolBar()     

    def refreshToolBar(self):
        '''modification des actions toolbar'''
        self.parent.toolBar.clear()
        self.parent.toolBar.addAction(self.actionNouveauPedaleur)
        if self.selectedPedaleur:
            self.parent.toolBar.addAction(self.actionEditerPedaleur)
            self.parent.toolBar.addAction(self.actionSupprimerPedaleur)
        
    def nouveauPedaleur(self):
        """ajoute un nouveau Pedaleur vierge"""
        nouv_pedaleur=self.mere.nouvPedaleur(insert=False)
        self.editerPedaleur(nouv_pedaleur)
        
    def editerPedaleur(self, pedaleur):
        """Editer Pedaleur"""
        self.fenetreEditPedaleur=FenetreEditPedaleur(parent=self,mere=self.mere,pedaleur=pedaleur)
        self.fenetreEditPedaleur.setWindowFlags(QtCore.Qt.Window)
        self.fenetreEditPedaleur.show()
        
    def supprimerPedaleur(self, pedaleur):
        """Editer Pedaleur"""
        pass


class FenetreEditContrat(Fenetre):
    """Fenetre Edition contrat"""
    
    def _initNext(self,**arguments):
        self.contrat=arguments.get('contrat',self.mere.nouvContrat(insert=False))
        self.dateEditOuverture.setDate(self.contrat.date_ouverture)
        self.dateEditCloture.setDate(self.contrat.date_cloture)
        self.textRemise.setText(str(self.contrat.remise))
        for genre in self.mere.genrescontrats_tb.data_arg['genre']:
            if isinstance(genre,int):genre=str(genre)
            self.comboGenre.addItem(genre)
        self.comboGenre.setEditText(self.contrat.genre)
        self.comboGenre.model().sort(0,QtCore.Qt.AscendingOrder)


    def createFenetre(self):
        self.labelRemise=QtGui.QLabel("Remise",parent=self)
        self.textRemise=QtGui.QLineEdit("0",parent=self)
        self.labelRemise.setBuddy( self.textRemise)  
        self.labelGenre=QtGui.QLabel("Genre",parent=self)
        self.comboGenre=QtGui.QComboBox(parent=self)
        self.labelGenre.setBuddy(self.comboGenre)     
        self.labelOuverture=QtGui.QLabel("date ouverture",parent=self)
        self.dateEditOuverture=QtGui.QDateEdit(parent=self)
        self.dateEditOuverture.setCalendarPopup(True)
        self.labelOuverture.setBuddy(self.dateEditOuverture)   
        self.labelCloture=QtGui.QLabel("date cloture",parent=self)
        self.dateEditCloture=QtGui.QDateEdit(parent=self)
        self.dateEditCloture.setCalendarPopup(True)
        self.labelCloture.setBuddy(self.dateEditCloture) 
#        self.labelDebutPrestation=QtGui.QLabel("date debut de prestation",parent=self)
#        self.dateEditDebutPrestation=KDateComboBox(parent=self)
#        self.labelDebutPrestation.setBuddy(self.dateKDEDebutPrestation) 
#        self.labelFinPrestation=QtGui.QLabel("date fin prestation",parent=self)
#        self.dateKDEFinPrestation=KDateComboBox(parent=self)
#        self.labelFinPrestation.setBuddy(self.dateKDEFinPrestation)    
        self.boutOk= QtGui.QPushButton("Ok",parent=self)
        self.boutAnn= QtGui.QPushButton("Annuler",parent=self)
        
        lay = QtGui.QGridLayout()         
        lay.addWidget(self.labelGenre,0,0,1,1)
        lay.addWidget(self.comboGenre, 0,1,1,1)
        lay.addWidget(self.labelRemise,1,0,1,1)
        lay.addWidget(self.textRemise,1,1,1,1)        
        lay.addWidget(self.labelOuverture,2,0,1,1)
        lay.addWidget(self.dateEditOuverture,2,1,2,1)
        lay.addWidget(self.labelCloture,4,0,1,1)
        lay.addWidget(self.dateEditCloture,4,1,2,1)
        lay.addWidget(self.boutOk,6,1,1,1)
        lay.addWidget(self.boutAnn,6,2,1,1)
        self.setLayout(lay)  
            
    def createConnection(self):
        self.boutOk.clicked.connect(self.ok)
        self.boutAnn.clicked.connect(self.ann)

    def ok(self):
        self.contrat.remise=float(self.textRemise.text())
        self.contrat.date_ouverture=datetime.date(self.dateEditOuverture.date().year(), self.dateEditOuverture.date().month(), self.dateEditOuverture.date().day())
        self.contrat.date_cloture=datetime.date(self.dateEditCloture.date().year(), self.dateEditCloture.date().month(), self.dateEditCloture.date().day())
        self.contrat.genre=self.comboGenre.currentText()
        if self.contrat.sqlInsert():
            self.parent.client.ajouterContrat(self.contrat)
            self.parent.modelContrat.ajouterContrat(self.contrat)
        self.close()
        
    def ann(self):
        self.close()
    
    
#class FenetreImport(Fenetre):
#    """fenetre d'importatio, de geolocalisation et de matching des nouveau lieux"""
#    def _initNext(self,**arguments):
#        self.listLieu=arguments.get('list_lieu',[self.mere.nouvLieu(insert=False,adresse='16 cité bauer',cp=75014)])
#        self.initData()
#        
#    def initData(self):
#        for lieu in self.listLieu:
#            self.modelImportUserLieu.ajouterLieu(lieu)
#    
#    def createModel(self):
#        self.modelImportUserLieu=ModelImportUserLieu(parent=self,mere=self.mere)
#        self.viewImportUserLieu.setModel(self.modelImportUserLieu)
#        self.modelMatchingLieu=ModelMatchingLieu(parent=self,mere=self.mere)
#        self.viewMatchingLieu.setModel(self.modelMatchingLieu)        
#            
#    def createFenetre(self):
#        self.resize(1000, 600)
#        self.viewImportUserLieu=ViewImportUserLieu(parent=self,mere=self.mere)
#        self.viewMatchingLieu=ViewMatchingLieu(parent=self,mere=self.mere)
#        self.boutAjoutLieu= QtGui.QPushButton("Ajouter", parent=self)
#        self.boutSuppLieu= QtGui.QPushButton("Supprimer", parent=self)
#        self.boutGeoLieu= QtGui.QPushButton("Geoloc", parent=self)
#        self.boutImporter= QtGui.QPushButton("Importer", parent=self)
#        self.boutOk= QtGui.QPushButton("Ok", parent=self)
#        self.boutAnnule= QtGui.QPushButton("Annulé", parent=self)
#        self.progressBarGeoLieu = QtGui.QProgressBar(parent=self)
#        self.progressBarGeoLieu.setValue(0)
#        self.sliderMatching = QtGui.QSlider(QtCore.Qt.Horizontal,parent=self)
#        self.sliderMatching.setMaximum(100)
#        self.sliderMatching.setMinimum(0)
#        self.sliderMatching.setValue(10)
#        self.labelSliderMatching=QtGui.QLabel(parent=self)
#        lay = QtGui.QGridLayout()
#        lay.addWidget(self.viewImportUserLieu,0,0,8,10)
#        lay.addWidget(self.viewMatchingLieu,0,10,8,10)
#        lay.addWidget(self.boutAjoutLieu,8,0,1,2)
#        lay.addWidget(self.boutGeoLieu,8,4,1,2)
#        lay.addWidget(self.boutSuppLieu,8,2,1,2)
#        lay.addWidget(self.boutImporter,8,6,1,2)
#        lay.addWidget(self.boutOk,10,10,1,2)
#        lay.addWidget(self.boutAnnule,10,12,1,2)
#        lay.addWidget(self.progressBarGeoLieu,9,0,1,10)
#        lay.addWidget(self.labelSliderMatching,9,20,1,1)
#        lay.addWidget(self.sliderMatching,9,10,1,10)
#        self.setLayout(lay)
#
#    def createConnection(self):
#        self.boutGeoLieu.clicked.connect(self.geolocalisation)
#        self.boutAjoutLieu.clicked.connect(self.nouvLieu)
#        self.boutImporter.clicked.connect(self.importerDock)
#        selModel=self.viewImportUserLieu.selectionModel()
#        selModel.currentChanged.connect(self._rafraichirMatching)
#        self.sliderMatching.valueChanged.connect(self._rafraichirMatching)
#        self.boutOk.clicked.connect(self.validation)
#        
#    def validation(self):
#        """valide les choix d'importation"""
#        for lieu in self.modelImportUserLieu.listLieu:
#            for dict_info in lieu._listInfoLieuRes:
#                if dict_info['check']==QtCore.Qt.Checked:
#                    if dict_info['type']=='Insert':lieu.sqlInsert()
#                    elif dict_info['type']=='DB':lieu=self.mere.Lieu(dict_info['dbid'])
#                    elif dict_info['type']=='Geoloc':lieu=self.mere.Lieu(dict_info['dbid'])
#        self.modelImportUserLieu.reset()
#        
#    def geolocalisation(self):
#        """geolocalise tous les lieux"""
#        self.modelImportUserLieu.geolocalisation()
#
#    def _rafraichirMatching(self,*index):
#        if index:
#            if isinstance(index[0],int):distance=index[0]
#            elif index[0].row()==index[1].row():return False
#            distance=self.sliderMatching.value()
#            self.labelSliderMatching.setText(str(distance))
#        lieu=self.modelImportUserLieu.data(self.viewImportUserLieu.currentIndex(),QtCore.Qt.UserRole)
#        self.modelMatchingLieu.matching(lieu=lieu,distance=distance)
#    
#    def nouvLieu(self):
#        """ajoute un nouveau lieux vierge"""
#        nouv_lieu=self.mere.nouvLieu(insert=False)
#        self.modelImportUserLieu.ajouterLieu(nouv_lieu)
#        
#    def importerDock(self):
#        """importer un document cvs pour matcher et geocoder"""
#        fichier_csv = QtGui.QFileDialog.getOpenFileName(self,"Ouvrir un CVS","/home/moustache/prog/workspace/KAFTIERE_2.0.1/CSV/")
#        if fichier_csv:
#            self.fichier =fichier_csv[0] 
#            self.dock=DocK(parent=self,mere=self.mere)
#            if self.dock.ouvrir(source=self.fichier):
#                self.modelImportUserLieu.reset()
#                for lieu in self.dock.listLieuDock:
#                    self.modelImportUserLieu.ajouterLieu(lieu)


class FenetreEditAdresseDB(Fenetre):
    """fenetre d'edition et gestion d adresse"""
    def _initNext(self,**arguments):
        self.lieu=arguments.get('lieu', [])
        self.contrat=arguments.get('contrat')
        self.initData()
        
    def initData(self):
        for adresse in self.lieu:
            self.modelLieuEditAdresse.ajouterLieu(adresse)
    
    def createModel(self):
        self.modelLieuEditAdresse=ModelLieuEditAdresse(parent=self,mere=self.mere)
        self.viewLieuEditAdresse.setModel(self.modelLieuEditAdresse)    
        self.modelMatchingLieu=ModelMatchingLieu(parent=self,mere=self.mere)
        self.viewMatchingLieu.setModel(self.modelMatchingLieu)    
        
    def createFenetre(self):
        self.resize(1000, 600)
        self.viewLieuEditAdresse=ViewLieuEditAdresse(parent=self,mere=self.mere)
        self.viewMatchingLieu=ViewMatchingLieu(parent=self,mere=self.mere)
        self.boutAjoutLieu= QtGui.QPushButton("Ajouter", parent=self)
        self.boutSuppLieu= QtGui.QPushButton("Supprimer", parent=self)
        self.boutGeoLieu= QtGui.QPushButton("Geoloc", parent=self)
        self.boutImporter= QtGui.QPushButton("Importer", parent=self)
        self.boutOk= QtGui.QPushButton("Ok", parent=self)
        self.boutAnnule= QtGui.QPushButton("Annulé", parent=self)
        self.progressBarGeoLieu = QtGui.QProgressBar(parent=self)
        self.progressBarGeoLieu.setValue(0)
        self.sliderMatching = QtGui.QSlider(QtCore.Qt.Horizontal,parent=self)
        self.sliderMatching.setMaximum(100)
        self.sliderMatching.setMinimum(0)
        self.sliderMatching.setValue(0)
        self.labelSliderMatching=QtGui.QLabel( parent=self)
        lay = QtGui.QGridLayout()
        lay.addWidget(self.viewLieuEditAdresse,0,0,8,10)
        lay.addWidget(self.viewMatchingLieu,0,10,8,10)
        lay.addWidget(self.boutAjoutLieu,8,0,1,2)
        lay.addWidget(self.boutGeoLieu,8,4,1,2)
        lay.addWidget(self.boutSuppLieu,8,2,1,2)
        lay.addWidget(self.boutImporter,8,6,1,2)
        lay.addWidget(self.boutOk,10,10,1,2)
        lay.addWidget(self.boutAnnule,10,12,1,2)
        lay.addWidget(self.progressBarGeoLieu,9,0,1,10)    
        lay.addWidget(self.sliderMatching,9,10,1,9)
        lay.addWidget(self.labelSliderMatching,9,19,1,1)
        self.setLayout(lay)

    def createConnection(self):
        self.boutGeoLieu.clicked.connect(self.geolocalisation)
        self.boutAjoutLieu.clicked.connect(self.nouvLieu)
        self.boutImporter.clicked.connect(self.importerDock)
        selModel=self.viewLieuEditAdresse.selectionModel()
        selModel.currentChanged.connect(self.lieuEditAdresseChanged)
        self.sliderMatching.valueChanged.connect(self._rafraichirMatching)
        self.boutOk.clicked.connect(self.validation)
        
    def lieuEditAdresseChanged(self):
        lieu=self.modelLieuEditAdresse.data(self.viewLieuEditAdresse.currentIndex(),QtCore.Qt.UserRole)
        self.modelMatchingLieu.lieu=lieu
        if lieu._valueMatching:self.sliderMatching.setValue(lieu._valueMatching)
        self.modelMatchingLieu.rafraichir()
             
    def validation(self):
        """valide les choix d'importation"""
        for lieu in self.modelLieuEditAdresse.listLieu:
            for dict_info in lieu._listInfoLieuRes:
                if dict_info['check']==QtCore.Qt.Checked:
                    if dict_info['type']=='Insert':lieu.sqlInsert()
                    elif dict_info['type']=='DB':lieu=self.mere.Lieu(dict_info['dbid'])
                    elif dict_info['type']=='Geoloc':lieu=self.mere.Lieu(dict_info['dbid'])
        self.close()
        
    def geolocalisation(self):
        """geolocalise tous les lieux"""
        self.modelLieuEditAdresse.geolocalisation()
        for lieu in self.modelLieuEditAdresse.listLieu:
            lieu._valueMatching=10
            self.modelMatchingLieu.matching(lieu=lieu,distance=lieu._valueMatching)   
 

    def _rafraichirMatching(self,*index):
        if index:
            if isinstance(index[0],int):distance=index[0]
            elif index[0].row()==index[1].row():return False
            distance=self.sliderMatching.value()
            self.labelSliderMatching.setText(str(distance))
        lieu=self.modelLieuEditAdresse.data(self.viewLieuEditAdresse.currentIndex(),QtCore.Qt.UserRole)
        lieu._valueMatching=distance
        self.modelMatchingLieu.matching(lieu=lieu,distance=distance)
    
    def nouvLieu(self):
        """ajoute un nouveau lieux vierge"""
        nouv_lieu=self.mere.nouvLieu(insert=False)
        self.modelLieuEditAdresse.ajouterLieu(nouv_lieu)
        
    def importerDock(self):
        """importer un document cvs pour matcher et geocoder"""
        fichier_csv = QtGui.QFileDialog.getOpenFileName(self,"Ouvrir un CVS","{}/CSV/".format(os.getcwd()))
        if fichier_csv:
            self.fichier =fichier_csv[0] 
            self.dock=DocK(parent=self,mere=self.mere)
            if self.dock.ouvrir(source=self.fichier):
                self.modelLieuEditAdresse.reset()
                for lieu in self.dock.listLieuDock:
                    self.modelLieuEditAdresse.ajouterLieu(lieu)


    def closeEvent(self, event):
        if hasattr(self.parent,"comboAdresse"):self.parent.initComboAdresse()
        event.accept() 


class FenetreImportListing(Fenetre):
    """fenetre d'importation listing client de lieu. Matching et retour en csv"""
    def _initNext(self,**arguments):
        self.lieu=arguments.get('lieu', [])
        self.contrat=arguments.get('contrat')
        self.initData()
        
    def initData(self):
        for adresse in self.lieu:
            self.modelImportListing.ajouterLieu(adresse)
    
    def createModel(self):
        self.modelImportListing=ModelImportListing(parent=self,mere=self.mere)
        self.viewImportListing.setModel(self.modelImportListing)    
        self.modelMatchingListing=ModelMatchingListing(parent=self,mere=self.mere)
        self.viewMatchingListing.setModel(self.modelMatchingListing)    
        
    def createFenetre(self):
        self.resize(1000, 600)
        self.viewImportListing=ViewImportListing(parent=self,mere=self.mere)
        self.viewMatchingListing=ViewMatchingListing(parent=self,mere=self.mere)
        self.boutGeoLieu= QtGui.QPushButton("Geoloc", parent=self)
        self.boutImporter= QtGui.QPushButton("Importer", parent=self)
        self.boutExporter=QtGui.QPushButton("Exporter", parent=self)
        self.boutOk= QtGui.QPushButton("Ok", parent=self)
        self.boutAnnule= QtGui.QPushButton("Annulé", parent=self)
        self.progressBarGeoLieu = QtGui.QProgressBar(parent=self)
        self.progressBarGeoLieu.setValue(0)
        self.sliderMatching = QtGui.QSlider(QtCore.Qt.Horizontal,parent=self)
        self.sliderMatching.setMaximum(100)
        self.sliderMatching.setMinimum(0)
        self.sliderMatching.setValue(0)
        self.labelSliderMatching=QtGui.QLabel( parent=self)
        
        layListingTable = QtGui.QGridLayout()
        layListingTable.addWidget(self.viewImportListing,0,0,8,10)
        layListingTable.addWidget(self.boutGeoLieu,8,4,1,2)
        layListingTable.addWidget(self.boutImporter,8,6,1,2)
        layListingTable.addWidget(self.boutExporter,8,8,1,2)
        
        layMatchingTable = QtGui.QGridLayout()
        layMatchingTable.addWidget(self.viewMatchingListing,0,0,8,10)
        layMatchingTable.addWidget(self.progressBarGeoLieu,10,0,1,10)    
        layMatchingTable.addWidget(self.sliderMatching,9,0,1,9)
        layMatchingTable.addWidget(self.labelSliderMatching,9,9,1,1)

        layValidation = QtGui.QGridLayout()
        layValidation.addWidget(self.boutOk,0,10,1,2)
        layValidation.addWidget(self.boutAnnule,0,12,1,2)

        lay=QtGui.QVBoxLayout()
        lay.addLayout(layListingTable)
        lay.addLayout(layMatchingTable)
        lay.addLayout(layValidation)
        self.setLayout(lay)
         
    def createConnection(self):
        self.boutGeoLieu.clicked.connect(self.geolocalisation)
        self.boutImporter.clicked.connect(self.importerDock)
        self.boutExporter.clicked.connect(self.exporterDock)
        selModel=self.viewImportListing.selectionModel()
        selModel.currentChanged.connect(self.lieuImportChanged)
        self.viewMatchingListing.doubleClicked.connect(self.lieuMatchingDoubleClicked)
        self.sliderMatching.valueChanged.connect(self._rafraichirMatching)
        self.boutOk.clicked.connect(self.validation)
        
    def lieuImportChanged(self):
        lieu=self.modelImportListing.data(self.viewImportListing.currentIndex(),QtCore.Qt.UserRole)
        self.modelMatchingListing.lieu=lieu
        if lieu._valueMatching:self.sliderMatching.setValue(lieu._valueMatching)
        self.modelMatchingListing.rafraichir()
        
    def lieuMatchingDoubleClicked(self):
        self.modelMatchingListing.lieu.setLieuRes(self.modelMatchingListing.data(self.viewMatchingListing.currentIndex(),QtCore.Qt.UserRole))
        self.modelMatchingListing.lieu._isAcceptable=None
        row=self.viewImportListing.currentIndex().row()
        self.modelImportListing.dataChanged.emit(self.modelImportListing.createIndex(row,0),self.modelImportListing.createIndex(row,13))
            
    def validation(self):
        """valide les choix d'importation et les associes aux depots"""
        list_lieu_choisi=[]
        list_lieu_refuse=[]
        for depot in self.listDepot:
            depot.sqlInsert()
            self.contrat.ajouterDepot(depot)
        for lieu in self.listLieu:
            if lieu._isAcceptable[0]:
                if lieu._infoLieuRes =='Dock':
                    lieu._updatable=True
                    lieu.sqlInsert()
                    list_lieu_choisi.append(lieu)
                    for depot in self.listDepot:
                        self.dock.importAssociationLieuDepot(depot, lieu)  
                else:
                    lieu_db=self.mere.Lieu(lieu.dbid)
                    lieu_db._infoLieuRes=lieu._infoLieuRes
                    lieu_db._lig_doc=lieu._lig_doc
                    list_lieu_choisi.append(lieu_db)
                    for depot in self.listDepot:
                        self.dock.importAssociationLieuDepot(depot, lieu_db)  
            else:list_lieu_refuse.append(lieu)
        self.close()
        
    def geolocalisation(self):
        """geolocalise tous les lieux"""
        self.modelImportListing.geolocalisation()
        for lieu in self.modelImportListing.listLieu:
            lieu._valueMatching=10
            self.modelMatchingListing.matching(lieu=lieu,distance=lieu._valueMatching)   

    def _rafraichirMatching(self,*index):
        if index:
            if isinstance(index[0],int):distance=index[0]
            elif index[0].row()==index[1].row():return False
            distance=self.sliderMatching.value()
            self.labelSliderMatching.setText(str(distance))
        lieu=self.modelImportListing.data(self.viewImportListing.currentIndex(),QtCore.Qt.UserRole)
        lieu._valueMatching=distance
        self.modelMatchingListing.matching(lieu=lieu,distance=distance)
        
    def importerDock(self):
        """importer un document cvs pour matcher et geocoder"""
        fichier_csv = QtGui.QFileDialog.getOpenFileName(self,"Ouvrir un CVS","{}/CSV".format(os.getcwd()))
        if fichier_csv:
            self.fichier =fichier_csv[0] 
            self.dock=DocK(parent=self,mere=self.mere)
            if self.dock.ouvrir(source=self.fichier):
                self.listDepot=self.dock.listDepot
                self.listLieu =self.dock.listLieu              
                self.modelImportListing.reset()
                for lieu in self.listLieu:
                    self.modelMatchingListing.matching(lieu, geolocalisation=False)
                    if len(lieu._listInfoLieuRes)==2:
                        if lieu._listInfoLieuRes[1]['type']=='DB':lieu.setLieuRes(lieu._listInfoLieuRes[1])
                        else:lieu.setLieuRes(lieu._listInfoLieuRes[0])
                    else:lieu.setLieuRes(lieu._listInfoLieuRes[0])
                    self.modelImportListing.ajouterLieu(lieu)

    def exporterDock(self):
        fichier_cible_csv = QtGui.QFileDialog.getSaveFileName(self,"Expoter un CVS",self.dock.source[:-4]+"_DEVIS_LISTING.csv")
        if fichier_cible_csv:
            dock_export=DocK(parent=self,mere=self.mere)
            dock_export.listDepot=self.listDepot
            dock_export.listLieu=self.listLieu
            dock_export.exporter(association_lieu_quantite=False)
            if dock_export.sauver(destination=fichier_cible_csv[0]):QtGui.QFileDialog(self, "Exportation du CVS a Réussit !")
            else :QtGui.QFileDialog(self, "Exportation du CVS a Echoué !")
                
    def closeEvent(self, event):
        if hasattr(self.parent,"comboAdresse"):self.parent.initComboAdresse()
        event.accept() 


class FenetreKml(Fenetre):
    """fenetre Kml"""
    def _initNext(self, **arguments):
        self.objetK=None
        
    def createFenetre(self):
        self.labelObjetK=KLabelPixmap(parent=self, mere=self.mere)
        self.textCheminFichier=QtGui.QLineEdit(parent=self)
        self.textEditKlmInfo=QtGui.QTextEdit(parent=self)
        self.boutExporter= QtGui.QPushButton("Exporter Kml",parent=self)
        self.boutActualiser= QtGui.QPushButton("Actualiser",parent=self)

        lay = QtGui.QGridLayout()
        lay.addWidget(self.labelObjetK,0,0,1,1)
        lay.addWidget(self.boutExporter,1,0,1,1)
        lay.addWidget(self.textCheminFichier,1,1,1,2)
        lay.addWidget(self.boutActualiser,1,4,1,1)                         
        lay.addWidget(self.textEditKlmInfo,2,0,4,6) 
        self.setLayout(lay)

    def objetKInserer(self):
        self.textEditKlmInfo.setText(self.kmlInfo())

    def kmlInfo(self):
        sting_info="Tournée dbid:{} du {} au {}\n".format(self.objetK.dbid, self.objetK.date_ouverture, self.objetK.date_cloture)
        sting_info+="   Nombre de lieux total:{}  Nombre non associé a un parcours:{}".format(len(self.objetK.listLieuContrats), len(self.objetK.listLieuSansParcours))
        for parcours in self.objetK.listParcours:
            sting_info+="\n\nParcours n°{} Pedaleur {}:".format(parcours.dbid,parcours.pedaleur.surnom)
            list_lieu_ordonne= parcours.listLieuOrdonne[0]
            if list_lieu_ordonne:
                sting_info+="\n   Lieux ordonnés:\n    "
                for (card, lieu) in list_lieu_ordonne:sting_info+= "{}:{}  ".format(card, lieu.nom)
            list_lieu_non_ordonne= parcours.listLieuOrdonne[1]
            if list_lieu_non_ordonne:
                sting_info+="\n   Attention ! Lieux non ordonnés:\n    "
                for lieu in list_lieu_non_ordonne:sting_info+= "{}  ".format(lieu.nom)
        return sting_info

    def createConnection(self):
        self.boutExporter.clicked.connect(self.exporterCheminFichier)
        self.boutActualiser.clicked.connect(self.actualiserFichier)
    
    def actualiserFichier(self):
        KmlParser(mere=self.mere, source=self.textCheminFichier.text())
        self.textEditKlmInfo.setText(self.kmlInfo())
    
    def exporterCheminFichier(self):
        chemin=QtGui.QFileDialog.getSaveFileName(self,"Expoter un KML","{}/KML/".format(os.getcwd())+self.objetK.__class__.__name__+str(self.objetK.dbid)+".kml")
        if chemin:
            Kml(racine=self.objetK, nom=self.objetK.__class__.__name__+str(self.objetK.dbid), destination=chemin[0])
            self.textCheminFichier.setText(chemin[0])


class FenetreTamponade(Fenetre):
    """fenetre edition tamponnade"""
    def _initNext(self, **arguments):
        self.objetK=None
        
    def createFenetre(self):
        self.labelObjetK=KLabelPixmap(parent=self, mere=self.mere)
        
        self.textCheminFichier=QtGui.QLineEdit(parent=self)
        self.labelTamponade=QtGui.QTextEdit("", parent=self)
        self.boutOuvrir= QtGui.QPushButton("Ouvrir",parent=self)
        self.boutTamponner= QtGui.QPushButton("Tamponner",parent=self)
        self.boutImporter= QtGui.QPushButton("Importer",parent=self)

#        self.modelLieuTamponade=ModelTamponade(parent=self,mere=self.mere)
#        self.viewTableTamponade.setModel(self.modelTamponade)  

        lay = QtGui.QGridLayout()
        lay.addWidget(self.labelObjetK,0,0,1,1)
        lay.addWidget(self.boutOuvrir,1,0,1,1)
        lay.addWidget(self.textCheminFichier,1,1,1,2)
        lay.addWidget(self.boutTamponner,1,3,1,1)
        lay.addWidget(self.boutImporter,1,4,1,1)  
        lay.addWidget(self.labelTamponade,2,0,4,6) 
        self.setLayout(lay)

    def objetKInserer(self):
        self.labelTamponade.setText(self.infoTamponade())

    def infoTamponade(self):
        sting_info="Tournée dbid:{} du {} au {}\n".format(self.objetK.dbid, self.objetK.date_ouverture, self.objetK.date_cloture)
        sting_info+="   Nombre de lieux total:{}  Nombre non associé a un parcours:{}".format(len(self.objetK.listLieuContrats), len(self.objetK.listLieuSansParcours))
        for parcours in self.objetK.listParcours:
            sting_info+="\n\nParcours n°{} Pedaleur {}:".format(parcours.dbid,parcours.pedaleur.surnom)
            list_lieu_ordonne= parcours.listLieuOrdonne[0]
            if list_lieu_ordonne:
                sting_info+="\n   Lieux ordonnés:\n    "
                for (card, lieu) in list_lieu_ordonne:
                    sting_info+= "{}:{}  \n".format(card, lieu.nom)
                    for contrat in self.objetK.listContrat:
                        str_depot=""
                        for depot in contrat.listDepot:
                            quantite_lieu=depot.quantiteLieu(lieu)
                            if quantite_lieu != 0 :str_depot+= "{}-{}  |".format(quantite_lieu, depot.surnom)
                        if str_depot!="":sting_info+="      {} {}\n".format(contrat.client.surnom, str_depot)
            list_lieu_non_ordonne= parcours.listLieuOrdonne[1]
            if list_lieu_non_ordonne:
                sting_info+="\n   Attention ! Lieux non ordonnés:\n    "
                for lieu in list_lieu_non_ordonne:sting_info+= "{}  ".format(lieu.nom)
        return sting_info

    def createConnection(self):
        self.boutOuvrir.clicked.connect(self.ouvrirCheminFichier)
        self.boutTamponner.clicked.connect(self.tamponnerFichier)
    
    def tamponnerFichier(self):
        from outils.libreoffice import acction
        acction(tournee=self.objetK)
    
    def ouvrirCheminFichier(self):
        chemin=QtGui.QFileDialog.getSaveFileName(self,"Expoter un KML","{}/KML/".format(os.getcwd())+self.objetK.__class__.__name__+str(self.objetK.dbid)+".kml")
        if chemin:
            Kml(racine=self.objetK, nom=self.objetK.__class__.__name__+str(self.objetK.dbid), destination="{}/KML/".format(os.getcwd())+self.objetK.__class__.__name__+str(self.objetK.dbid)+".kml")
            self.textCheminFichier.setText(chemin[0])


