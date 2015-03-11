'''
Created on 7 mai 2013

@author: moustache
'''
import os.path as path
import csv

class DocDepotK():
    NOM=0
    SURNOM=1
    GENRE=2
    QUANTITE=3
    VOLUME=4
    NB_CARTON=5
    REMARQUE=6
    POID=7
    NB_PAQUET=8
    PRIX_UNITE=9
    
    def __init__(self,parent,col):
        self.parent=parent
        self.col=col

    @property
    def nom(self):
        return self.parent[DocDepotK.NOM][self.col]
    @nom.setter
    def nom(self,nom):
        self.parent[DocDepotK.NOM][self.col]=nom
    @property
    def surnom(self):
        return self.parent[DocDepotK.SURNOM][self.col]
    @surnom.setter
    def surnom(self,surnom):
        self.parent[DocDepotK.SURNOM][self.col]=surnom
    @property
    def genre(self):
        if self.parent[DocDepotK.GENRE][self.col]=='Flyer':return 1
        elif self.parent[DocDepotK.GENRE][self.col]=='Dépliant':return 2
        elif self.parent[DocDepotK.GENRE][self.col]=='Brochure':return 3
        elif self.parent[DocDepotK.GENRE][self.col]=='Affiche':return 4
        else: return 5
    @genre.setter
    def genre(self,genre):
        self.parent[DocDepotK.GENRE][self.col]=genre
    @property
    def quantite(self):
        return self.parent[DocDepotK.QUANTITE][self.col]
    @quantite.setter
    def quantite(self,quantite):
        self.parent[DocDepotK.QUANTITE][self.col]=quantite
    @property
    def volume(self):
        return self.parent[DocDepotK.VOLUME][self.col]
    @volume.setter
    def volume(self,volume):
        self.parent[DocDepotK.VOLUME][self.col]=volume
    @property
    def nb_carton(self):
        return self.parent[DocDepotK.NB_CARTON][self.col]
    @nb_carton.setter
    def nb_carton(self,nb_carton):
        self.parent[DocDepotK.NB_CARTON][self.col]=nb_carton
    @property
    def remarque(self):
        return self.parent[DocDepotK.REMARQUE][self.col]
    @remarque.setter
    def remarque(self,remarque):
        self.parent[DocDepotK.REMARQUE][self.col]=remarque   
    @property
    def poid(self):
        return self.parent[DocDepotK.POID][self.col]
    @poid.setter
    def poid(self,poid):
        self.parent[DocDepotK.POID][self.col]=poid 
    @property
    def prix_unite(self):
        return self.parent[DocDepotK.PRIX_UNITE][self.col]
    @prix_unite.setter
    def prix_unite(self,prix_unite):
        self.parent[DocDepotK.PRIX_UNITE][self.col]=prix_unite
    @property
    def nb_paquet(self):
        return self.parent[DocDepotK.NB_PAQUET][self.col]
    @nb_paquet.setter
    def nb_paquet(self,nb_paquet):
        self.parent[DocDepotK.NB_PAQUET][self.col]=nb_paquet

    def quantiteLieu(self,lig_doc):
        return self.parent[DocK.LIGNE_PREMIER_LIEU+lig_doc][self.col]  

    def setQuantiteLieu(self, lig_doc, quantite):
        self.parent[DocK.LIGNE_PREMIER_LIEU+lig_doc][self.col]=quantite

class DocLieuK():
    INFO_DEVIS=0
    INFO_KAF=1
    REF=2
    NOM=3
    ADRESSE=4
    CP=5
    VILLE=6
    INFO_LIEU=7
    DESTINATAIRE=8
    PRIX=9
    
    def __init__(self,parent=None,lig=None):
        self.parent=parent
        self.lig=lig

    def dockerLieuK(self,doc_ligne,lieu):
        self.lig=doc_ligne+DocK.LIGNE_PREMIER_LIEU
        self.ref=lieu.dbid
    @property
    def info_kaf(self):
        return self.parent[self.lig][DocLieuK.INFO_KAF]
    @info_kaf.setter
    def info_kaf(self,info_kaf):
        self.parent[self.lig][DocLieuK.INFO_KAF]=info_kaf
    @property
    def info_devis(self):
        return self.parent[self.lig][DocLieuK.INFO_DEVIS]
    @info_devis.setter
    def info_devis(self,info_devis):
        self.parent[self.lig][DocLieuK.INFO_DEVIS]=info_devis
    @property
    def ref(self):
        return self.parent[self.lig][DocLieuK.REF]
    @ref.setter
    def ref(self,ref):
        self.parent[self.lig][DocLieuK.REF]=ref
    @property
    def nom(self):
        return self.parent[self.lig][DocLieuK.NOM]
    @nom.setter
    def nom(self,nom):
        self.parent[self.lig][DocLieuK.NOM]=nom
    @property
    def adresse(self):
        return self.parent[self.lig][DocLieuK.ADRESSE]
    @adresse.setter
    def adresse(self,adresse):
        self.parent[self.lig][DocLieuK.ADRESSE]=adresse
    @property
    def cp(self):
        return self.parent[self.lig][DocLieuK.CP]
    @cp.setter
    def cp(self,cp):
        self.parent[self.lig][DocLieuK.CP]=cp
    @property
    def ville(self):
        return self.parent[self.lig][DocLieuK.VILLE]
    @ville.setter
    def ville(self,ville):
        self.parent[self.lig][DocLieuK.VILLE]=ville
    @property
    def info_lieu(self):
        return self.parent[self.lig][DocLieuK.INFO_LIEU]
    @info_lieu.setter
    def info_lieu(self,info_lieu):
        self.parent[self.lig][DocLieuK.INFO_LIEU]=info_lieu
    @property
    def destinataire(self):
        return self.parent[self.lig][DocLieuK.DESTINATAIRE]
    @destinataire.setter
    def destinataire(self,destinataire):
        self.parent[self.lig][DocLieuK.DESTINATAIRE]=destinataire
    @property
    def prix(self):
        return self.parent[self.lig][DocLieuK.PRIX]
    @prix.setter
    def prix(self,prix):
        self.parent[self.lig][DocLieuK.PRIX]=prix

        
       
class DocK(list):    
    COLONNE_PREMIER_DEPOT=10
    LIGNE_PREMIER_LIEU=11
    
    def __init__(self,parent=None,mere=None):  
        self.mere=mere
        self.parent=parent
        self.source=None
        self.listLieu=[]
        self.listDepot=[]
        
    def legendeDepot(self):
        """definit la legende Depot"""
        self[DocDepotK.NOM][DocK.COLONNE_PREMIER_DEPOT-1]="DEPOT NOM : >"
        self[DocDepotK.SURNOM][DocK.COLONNE_PREMIER_DEPOT-1]="DEPOT SURNOM : >"
        self[DocDepotK.GENRE][DocK.COLONNE_PREMIER_DEPOT-1]="DEPOT TYPE : >"
        self[DocDepotK.QUANTITE][DocK.COLONNE_PREMIER_DEPOT-1]="DEPOT QUANTITEE : >"
        self[DocDepotK.VOLUME][DocK.COLONNE_PREMIER_DEPOT-1]="DEPOT VOLUME : >"
        self[DocDepotK.NB_CARTON][DocK.COLONNE_PREMIER_DEPOT-1]="DEPOT CARTONS : >"
        self[DocDepotK.REMARQUE][DocK.COLONNE_PREMIER_DEPOT-1]="DEPOT REMARQUE : >"
        self[DocDepotK.POID][DocK.COLONNE_PREMIER_DEPOT-1]="DEPOT POID CARTONS : >"
        self[DocDepotK.NB_PAQUET][DocK.COLONNE_PREMIER_DEPOT-1]="DEPOT NB PAQUET : >"
        self[DocDepotK.PRIX_UNITE][DocK.COLONNE_PREMIER_DEPOT-1]="DEPOT PRIX : >"

    def legendeLieu(self):
        """definit la legende Lieu"""
        self[DocK.LIGNE_PREMIER_LIEU-1][DocLieuK.INFO_DEVIS]="INFO DEVIS : |"
        self[DocK.LIGNE_PREMIER_LIEU-1][DocLieuK.INFO_KAF]="INFO KAF : |"
        self[DocK.LIGNE_PREMIER_LIEU-1][DocLieuK.REF]="REF : |"
        self[DocK.LIGNE_PREMIER_LIEU-1][DocLieuK.NOM]="NOM  : |"
        self[DocK.LIGNE_PREMIER_LIEU-1][DocLieuK.ADRESSE]="ADRESSE : |"
        self[DocK.LIGNE_PREMIER_LIEU-1][DocLieuK.CP]="CP : |"
        self[DocK.LIGNE_PREMIER_LIEU-1][DocLieuK.VILLE]="VILLE : |"
        self[DocK.LIGNE_PREMIER_LIEU-1][DocLieuK.INFO_LIEU]="INFORMATION LIEU : |"
        self[DocK.LIGNE_PREMIER_LIEU-1][DocLieuK.DESTINATAIRE]="DESTINATAIRE : |"
        self[DocK.LIGNE_PREMIER_LIEU-1][DocLieuK.PRIX]="LIEU PRIX : |"

    def col_depot(self, depot):
        if depot in self.listDepot:return self.listDepot.index(depot)
        else :return None

    def lig_lieu(self, lieu):
        if lieu in self.listLieu:return self.listLieu.index(lieu)
        else :return None
        
    def depot(self,colDepot=0):
        col=DocK.COLONNE_PREMIER_DEPOT+colDepot
        depot=DocDepotK(self, col)
        return depot

    def lieu(self,ligLieu=0):
        lig=DocK.LIGNE_PREMIER_LIEU+ligLieu
        lieu=DocLieuK(self, lig)
        return lieu
    
    def updateLieu(self,doc_ligne,lieuK):
        dclieu=DocLieuK(parent=self)
        dclieu.dockerLieuK(doc_ligne,lieuK)
        
    def isDepot(self,colDepot):
        col=DocK.COLONNE_PREMIER_DEPOT+colDepot
        if len(self[0])>col:
            return True
        else:
            print('Depot ({0}) inexistant dans fichier CSV ({1})'.format(colDepot,self.source))
            return False

    def isLieu(self,lig_lieu=0):
        lig=DocK.LIGNE_PREMIER_LIEU+lig_lieu
        if len(self)>lig:
            return True
        else:
            print('Lieu ({0}) inexistant dans fichier CSV ({1})'.format(lig_lieu,self.source))
            return False
                 
    def ouvrir(self,source=None):
        if path.isfile(source):
            self.source=source 
            with open(path.join(self.source), newline='') as DOK:
                if source.endswith('.csv'):
                    self.chargerCsv(DOK)
                    ligLieu=0
                    while self.importLieu(ligLieu):
                        ligLieu+=1
                    colDepot=0
                    while self.importDepot(colDepot):
                        colDepot+=1
            return True
        else :
            print('Fichier CSV inexistant ({})'.format(source))
            return False
    
    def chargerCsv(self,DOK):
        lecteur=csv.reader(DOK, delimiter=';')
        for case in lecteur:
            self.append(case)
    
    def sauver(self,destination=None):
        writer=csv.writer(open((path.join(destination)),'w',encoding='utf8'), delimiter=';')
        for row in self:
            writer.writerow(row)
        return True
    
    def importLieu(self,ligLieu):
        if self.isLieu(ligLieu):
            dict_info={'type':'Dock',
            'dbid':None, 
            'nom':None,
            'adresse':None, 
            'cp':None,
            'ville':None,
            'latitude':0, 
            'longitude':0, 
            'etat':'inconnu', 
            'pertinence':None, 
            'saturation_max':10, 
            'distance':0}
            lieu=self.mere.nouvLieu(insert=False)
            lieu._updatable=False
            lieu.adresse._updatable=False
            lieu._lig_doc=ligLieu
            if self.lieu(ligLieu).ref != '' :dict_info['dbid']=int(self.lieu(ligLieu).ref)
            if self.lieu(ligLieu).nom != '' :dict_info['nom']=self.lieu(ligLieu).nom
            if self.lieu(ligLieu).cp != '' : dict_info['cp']=int(self.lieu(ligLieu).cp)
            if self.lieu(ligLieu).adresse != '' :dict_info['adresse']=self.lieu(ligLieu).adresse
            if self.lieu(ligLieu).ville != '' :dict_info['ville']=self.lieu(ligLieu).ville
            #if self.lieu(ligLieu).info_kaf != '' : lieu_kwargs['info_kaf']=self.lieu(ligLieu).info_kaf
            #if self.lieu(ligLieu).info_lieu != '' : lieu_kwargs['info_lieu']=self.lieu(ligLieu).info_lieu
            #if self.lieu(ligLieu).destinataire != '' : lieu_kwargs['destinataire']=self.lieu(ligLieu).destinataire
            #if self.lieu(ligLieu).prix != '' : lieu_kwargs['prix']=self.lieu(ligLieu).prix  
            #if self.lieu(ligLieu).ville != '' : lieu_kwargs['ville']=self.lieu(ligLieu).ville
            lieu._listInfoLieuRes.append(dict_info)
            self.listLieu.append(lieu)
            return True
        return False

    def importDepot(self,colDepot):
        if self.isDepot(colDepot):
            nouv_depot=self.mere.nouvDepot(insert=False)
            nouv_depot._col_doc=colDepot
            if self.depot(colDepot).nom != '' : nouv_depot.nom=self.depot(colDepot).nom
            if self.depot(colDepot).surnom != '' : nouv_depot.surnom=self.depot(colDepot).surnom
            if self.depot(colDepot).genre != '' : nouv_depot.genre=int(self.depot(colDepot).genre)
            if self.depot(colDepot).quantite != '' : nouv_depot.quantite=int(self.depot(colDepot).quantite)
            if self.depot(colDepot).volume != '' : nouv_depot.volume=float(self.depot(colDepot).volume)
            if self.depot(colDepot).nb_carton != '' : nouv_depot.nb_carton=int(self.depot(colDepot).nb_carton)
            if self.depot(colDepot).remarque != '' : nouv_depot.remarque=self.depot(colDepot).remarque
            if self.depot(colDepot).poid != '' :nouv_depot.poid=float(self.depot(colDepot).poid)
            if self.depot(colDepot).prix_unite != '' : nouv_depot.prix_unite=float(self.depot(colDepot).prix_unite)
            self.listDepot.append(nouv_depot)
            return  True
        return False     
 
    def importAssociationLieuDepot(self, depot, lieu):
        """associe le depot avec le lieu"""
        val=self.depot(depot._col_doc).quantiteLieu(lieu._lig_doc)
        if val !='':
            if int(val)>0:depot.ajouterLieu(lieu, int(val))
                    
    def exporter(self, association_lieu_quantite=True):
        ligLieu=0
        colDepot=0
        
        for x in range(len(self.listLieu)+DocK.COLONNE_PREMIER_DEPOT+1):
            list_ligne=[]
            for y in range(len(self.listDepot)+DocK.LIGNE_PREMIER_LIEU+1): list_ligne.append(None)
            self.append( list_ligne)
        
        self.legendeLieu()
        self.legendeDepot()

        for lieu in self.listLieu:
            self.exportLieu(lieu, ligLieu)
            ligLieu+=1
        for depot in self.listDepot:
            self.exportDepot(depot, colDepot, association_lieu_quantite=association_lieu_quantite)
            colDepot+=1
        
    def exportLieu(self,lieu, ligne):
        """ecrit le lieu dans le Doc"""
        self.lieu(ligne).ref = lieu.dbid
        self.lieu(ligne).info_kaf =lieu.etat
        self.lieu(ligne).info_devis=lieu.isAcceptable[1]
        self.lieu(ligne).nom =lieu.nom
        #self.lieu(ligLieu).info_lieu =lieu.info_lieu
        #self.lieu(ligne).destinataire =lieu.destinataire
        #self.lieu(ligne).prix=lieu.prix  
        self.lieu(ligne).cp =lieu.adresse.cp
        self.lieu(ligne).ville=lieu.adresse.ville
        self.lieu(ligne).adresse=lieu.adresse.adresse

        
    def exportDepot(self,depot, colonne, association_lieu_quantite=True):
        """ecrit le depot dans le Doc"""
        self.depot(colonne).nom = depot.nom + " PUTE"
        self.depot(colonne).surnom = depot.surnom
        self.depot(colonne).genre = depot.genre
        self.depot(colonne).quantite =depot.quantite
        self.depot(colonne).volume =depot.volume
        self.depot(colonne).nb_carton =depot.nb_carton
        self.depot(colonne).remarque =depot.remarque
        self.depot(colonne).poid =depot.poid
        self.depot(colonne).prix=depot.prix
        if association_lieu_quantite:
            lig_lieu=0
            for lieu in self.listLieu:
                d=self.depot(colonne)
                q=depot.dictLieuQuantite[lieu]
                d.setQuantiteLieu(lig_lieu, q)
                lig_lieu+=1
#                self.depot(colonne).set_lieu_quantite(lieu, depot.quantite(lieu))

    def cleanDock(self):
        for lieu in self.listLieu:delattr(lieu, '_lig_doc')
        for depot in self.listDepot:delattr(depot, '_col_doc')
        
