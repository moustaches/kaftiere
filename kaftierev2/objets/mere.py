
import time
from objets.objet_sql import connectionDBPostgres,sql_select,SqlTable
from objets.objet_qt import PedaleurQ,ParcoursQ,AdresseQ,ClientQ,ContratQ,DepotQ,LieuQ,TourneeQ 
from outils.geocoding import connectionGeocodeur

class Mere(object):
    """Class mere qui centralise, organise, charge et initialise les objets"""
    def __init__(self,verbose=False,fenetre=None):
        self._verbose=verbose
        self._fenetre=fenetre
        self._chargement=0
        self.dictContrat={}
        self.dictClient={}
        self.dictAdresse={}
        self.dictTournee={}
        self.dictLieu={}
        self.dictDepot={}
        self.dictTournee={}
        self.dictParcours={}
        self.dictPedaleur={}
        self.dictShape={}
        self.dictChemin={}
        
    def initData(self):
        """initialise les datas en chargant les K-objets"""
        if connectionDBPostgres():
            self.chargerTable()
            self.chargerObjetK()
        if connectionGeocodeur("Nominatim"):print("connection geolocolisation")
        
    def chargerTable(self):
        """charge les table fixe"""
        self.etatslieux_tb=SqlTable('etatslieux_tb',['dbid','etat'],self._verbose)
        self.genreslieux_tb=SqlTable('genreslieux_tb',['dbid','genre'],self._verbose)
        self.genresdepots_tb=SqlTable('genresdepots_tb',['dbid','genre'],self._verbose)
        self.genresclients_tb=SqlTable('genresclients_tb',['dbid','genre'],self._verbose)
        self.genrescontrats_tb=SqlTable('genrescontrats_tb',['dbid','genre'],self._verbose)
        self.cpvilles_tb=SqlTable('cp_villes_tb',['dbid','cp','ville'],self._verbose)
        
    def chargerObjetK(self):
        """charge les objets-K
        informe _fenetre de l'avancement
        charge la kaftiere"""
        DICT_OBJK=[{'nom':'Lieux','table':'lieux_tb','fonct':self.Lieu}, 
                   {'nom':'Clients','table':'clients_tb','fonct':self.Client}, 
                   {'nom':'Contrats','table':'contrats_tb','fonct':self.Contrat}, 
                   {'nom':'Depots','table':'depots_tb','fonct':self.Depot}, 
                   {'nom':'Tournees','table':'tournees_tb','fonct':self.Tournee},
                   {'nom':'Pedaleurs','table':'pedaleurs_tb','fonct':self.Pedaleur}, 
                   {'nom':'Parcours','table':'parcours_tb','fonct':self.Parcours}
                   ]
        tt0=time.time()
        for obj_k in DICT_OBJK:
            i=0
            t0=time.time()
            list_sel_dbid=sql_select(obj_k['table'], ['dbid'],None, None, self._verbose)
            i_tot=len(list_sel_dbid)
            if self._fenetre:
                self._fenetre._actualisation(label=obj_k['nom'])
                for dict_dbid in list_sel_dbid:
                    i+=1
                    obj_k['fonct'](dict_dbid['dbid'])
                    val=  int((i*100)/i_tot)
                    if not val == self._chargement :
                        self._fenetre._actualisation(val_prog_bar=val)
                        self._chargement=val
                t1=time.time()
                time_var=t1-t0        
                self._fenetre._actualisation(i_tot=i_tot,label=obj_k['nom'],val_time=time_var)   
            else:
                for dict_dbid in list_sel_dbid:
                    obj_k['fonct'](dict_dbid['dbid'])
        self._fenetre._actualisation(i_tot=-1,label='Chargement total',val_time=t1-tt0)

            
    def Contrat(self,dbid):
        objet=self.dictContrat.get(dbid)
        if not objet:
            objet=ContratQ(self)
            self.dictContrat[dbid]=objet
            objet.load(dbid)
            return objet
        return objet
    
    def nouvContrat(self,**arguments):
        objet=ContratQ(self)
        objet._initData(**arguments)
        if arguments.get('insert'):
            objet.sqlInsert()         
        return objet
    
    def Lieu(self,dbid):
        objet=self.dictLieu.get(dbid)
        if not objet:
            objet=LieuQ(self)
            self.dictLieu[dbid]=objet
            objet.load(dbid)
            return objet
        return objet
    
    def nouvLieu(self,**arguments):
        objet=LieuQ(self)
        objet._initData(**arguments)
        if arguments.get('insert'):
            objet.sqlInsert()         
        return objet
    
    def Adresse(self,dbid):
        objet=self.dictAdresse.get(dbid)
        if not objet:
            objet=AdresseQ(self)
            self.dictAdresse[dbid]=objet
            objet.load(dbid)
            return objet
        return objet
    
    def nouvAdresse(self,**arguments):
        objet=AdresseQ(self)
        objet._initData(**arguments)
        if arguments.get('insert'):
            objet.sqlInsert()
        return objet
    
    def Depot(self,dbid):
        objet=self.dictDepot.get(dbid)
        if not objet:
            objet=DepotQ(self)
            self.dictDepot[dbid]=objet
            objet.load(dbid)
            return objet
        return objet
    
    def nouvDepot(self,**arguments):
        objet=DepotQ(self)
        objet._initData(**arguments)
        if arguments.get('insert'):
            objet.sqlInsert()
        return objet    
    
    def Tournee(self,dbid):
        objet=self.dictTournee.get(dbid)
        if not objet:
            objet=TourneeQ(self)
            self.dictTournee[dbid]=objet
            objet.load(dbid)
            return objet
        return objet
    
    def nouvTournee(self,**arguments):
        objet=TourneeQ(self)
        objet._initData(**arguments)
        if arguments.get('insert'):
            objet.sqlInsert()
        return objet   

    def Parcours(self,dbid):
        objet=self.dictParcours.get(dbid)
        if not objet:
            objet=ParcoursQ(self)
            self.dictParcours[dbid]=objet
            objet.load(dbid)
            return objet
        return objet
    
    def nouvParcours(self,**arguments):
        objet=ParcoursQ(self)
        objet._initData(**arguments)
        if arguments.get('insert'):
            objet.sqlInsert()
        return objet  

    def Client(self,dbid):
        objet=self.dictClient.get(dbid)
        if not objet:
            objet=ClientQ(self)
            self.dictClient[dbid]=objet
            objet.load(dbid)
            return objet
        return objet
    
    def nouvClient(self,**arguments):
        objet=ClientQ(self)
        objet._initData(**arguments)
        if arguments.get('insert'):
            objet.sqlInsert()         
        return objet

    def Pedaleur(self,dbid):
        objet=self.dictPedaleur.get(dbid)
        if not objet:
            objet=PedaleurQ(self)
            self.dictPedaleur[dbid]=objet
            objet.load(dbid)
            return objet
        return objet
    
    def nouvPedaleur(self,**arguments):
        objet=PedaleurQ(self)
        objet._initData(**arguments)
        if arguments.get('insert'):
            objet.sqlInsert()
        return objet   
        
    def Chemin(self,dbid):
        return self.dictChemin.get(dbid)
        
    def Shape(self,dbid):
        return self.dictShape.get(dbid)      
        
        
