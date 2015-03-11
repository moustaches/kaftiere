'''
Created on 4 mai 2013

@author: moustache
'''
import urllib.request
from operator import attrgetter
import json

from objets.objet_sql import SqlPedaleurK,SqlParcoursK, SqlAdresseK,SqlClientK,SqlContratK,SqlDepotK,SqlLieuK,SqlTourneeK
from objets.objet_geo import ShapeK, CheminK, PointK
from outils.geocoding import geocoder

class ObjetK():
    """super classe de controle des objets"""
    def __init__(self,mere):
        self._mere=mere
        
    def _initObjetData(self,**arguments):
        pass
        
    def _loadComposantes(self,**arguments):
        pass        
        
    def load(self,dbid=None):
        """charge objet et ses composantes
        -->
        dbid: id(int)
        <--
        return self"""
        self.dbid=dbid
        self._sqlLoad(self.dbid)
        self._loadComposantes()
        return self


class ParcoursK(SqlParcoursK, ObjetK):
    '''ObjetK qui represente les parcours'''
    def __init__(self,mere):
        SqlParcoursK.__init__(self)
        ObjetK.__init__(self, mere)
        self._tournee=None
        self._pedaleur=None
        self._shape=None
        self._chemin=None
        
    def supprimer(self,composentes=True):
        """supression du parcours et de ses composantes"""
        if self.tournee:
            if self in self.tournee.listParcours:self.tournee.listParcours.remove(self)
        self.sqlDelete()
        
    @property
    def shape(self):
        if self._shape:return self._shape
        else:
            self._shape=ShapeK(parent=self, mere=self._mere)
            return self._shape
    @shape.setter
    def shape(self,shape):
        self._shape=shape 
 
    @property
    def chemin(self):
        if self._chemin:return self._chemin
        else:
            self._chemin=CheminK(parent=self, mere=self._mere)
            return self._chemin
    @chemin.setter
    def chemin(self,chemin):
        self._chemin=chemin  
        
    @property
    def tournee(self):
        return self._tournee
    @tournee.setter
    def tournee(self,tournee):
        self.dbid_tournee=tournee.dbid
        self._tournee=tournee

    @property
    def pedaleur(self):
        return self._pedaleur
    @pedaleur.setter
    def pedaleur(self,pedaleur):
        self.dbid_pedaleur=pedaleur.dbid
        self._pedaleur=pedaleur

    @property
    def listLieu(self):
        list_lieu=[]
        if self.list_dbid_lieu:
            for dbid_lieu in self.list_dbid_lieu:
                list_lieu.append(self._mere.Lieu(dbid_lieu))
        return list_lieu

    @property
    def listLieuOrdonne(self):
        """retourne list (lieu,son ordinal),list lieu sans cardinal"""
        list_lieu_ordonne=[]
        list_lieu_non_ordonne=[]
        i=0
        if self.line:
            for dbid_lieu in self.line:
                if dbid_lieu in self.list_dbid_lieu:
                    i+=1
                    list_lieu_ordonne.append((i, self._mere.Lieu(dbid_lieu)))
                else:print('listordonnéprob '+ str(dbid_lieu))
            for dbid_lieu in self.list_dbid_lieu:
                if dbid_lieu not in self.line:
                    list_lieu_non_ordonne.append( self._mere.Lieu(dbid_lieu))
        return list_lieu_ordonne, list_lieu_non_ordonne

    def quantiteDepot(self, depot):
        """returne la quantite du depot dans le parcours"""
        quantite_depot=0
        for lieu in self.listLieu:
            quantite_depot+=depot.quantiteLieu(lieu)
        return quantite_depot
        
    @property
    def quantiteDepotTotal(self):
        """returne le nombre de flyer totale"""
        quantite_depot=0
        for depot in self.tournee.listDepot:
            quantite_depot+=self.quantiteDepot(depot)
        return quantite_depot

    @property
    def volume(self):
        """returne volume"""
        volume=0
        for lieu in self.listLieu:
            for depot in self.tournee.listDepot:
                volume+=depot.quantiteLieu(lieu)*depot.volume
        return volume

    @property
    def poid(self):
        """returne poid"""
        poid=0
        for lieu in self.listLieu:
            for depot in self.tournee.listDepot:
                poid+=depot.quantiteLieu(lieu)*depot.poid
        return poid

    @property
    def prix(self):
        """returne prix"""
        prix=0
        for lieu in self.listLieu:
            for depot in self.tournee.listDepot:
                prix+=depot.quantiteLieu(lieu)*depot.prix_unite
        return prix

    def _loadComposantes(self):
        """charge les Pedaleurs,Tournee,shape,chemin"""
        if self.dbid_tournee:self._tournee=self._mere.Tournee(self.dbid_tournee)
        if self.dbid_pedaleur:self._pedaleur=self._mere.Pedaleur(self.dbid_pedaleur)

    def _kmlEditeur(self, kml=None,regle=None):
        klm_contrat=kml.newfolder(name='P{} - {}'.format(self.dbid, self.pedaleur.surnom))
        klm_contrat.extendeddata.schemadata.newsimpledata('objetK', 'ParcoursK')
        klm_contrat.extendeddata.schemadata.newsimpledata('dbid', self.dbid)
        return klm_contrat

    def ajouterLieu(self, lieu):
        if not lieu in self.listLieu:
            self.ajouterListDbidLieu(lieu)
            
    def retirerLieu(self, lieu):
        if lieu in self.listLieu:
            self.retirerListDbidLieu(lieu)
            
    def Deshaper(self):
        """deshape les lieux tournée aveec la shape associé au parcour """
        lieu_deshape=[]
        for lieu in self.tournee.listLieuContrats:
            if self.shape.deshaper0bjet(lieu.adresse.point):lieu_deshape.append(str(lieu.dbid))
        if lieu_deshape:self.list_dbid_lieu=lieu_deshape

    def Cheminer(self):
        """Cheminer les lieux associé aveec le chemin associé au parcour """
        lieu_deshape=[]
        for lieu in self.tournee.listLieuContrats:
            if self.shape.deshaper0bjet(lieu.adresse.point):lieu_deshape.append(str(lieu.dbid))
        if lieu_deshape:self.list_dbid_lieu=lieu_deshape
 
 
class TourneeK(SqlTourneeK, ObjetK):
    '''ObjetK qui regroupe les contrats dans le temps'''
    def __init__(self, mere):
        ObjetK.__init__(self, mere)
        SqlTourneeK.__init__(self)  
        self.listContrat=[]
        self.listParcours=[]

    @property
    def listDepot(self):
        list_depot=[]
        for contrat in self.listContrat:
            for depot in contrat.listDepot:
                if not depot in list_depot:
                    list_depot.append(depot)
        return sorted(list_depot,key=attrgetter('surnom'))

    @property
    def listClient(self):
        list_client=[]
        for contrat in self.listContrat:
            if not contrat.client in list_client:
                list_client.append(contrat.client)
        return sorted(list_client, key=attrgetter('surnom'))

    @property
    def listLieuContrats(self):
        """list lieu issue des contrats"""
        list_lieu=[]
        for contrat in self.listContrat:
            for lieu in contrat.listLieu:
                if not lieu in list_lieu:
                    list_lieu.append(lieu)
        return list_lieu  

    @property
    def listLieuParcours(self):
        """list lieu integrer dans parcours"""
        list_lieu=[]
        for parcours in self.listParcours:
            for lieu in parcours.listLieu:
                list_lieu.append(lieu)
        return list_lieu

    @property
    def listLieuSansParcours(self):
        """list lieu sans integrer dans parcours"""
        list_lieu=[]
        list_lieu_parcours=self.listLieuParcours
        for lieu in self.listLieuContrats:
            if lieu not in list_lieu_parcours:
                    list_lieu.append(lieu)
        return list_lieu

    @property
    def prix(self):
        prix=0
        for contrat in self.listContrat:
            prix+=contrat.prix
        return prix

    @property
    def listPedaleur(self):
        """list des pedaleurs de la tournee"""
        list_pedaleur=[]
        for parcours in self.listParcours:
                if not parcours.pedaleur in list_pedaleur:
                    list_pedaleur.append(parcours.pedaleur)
        return  sorted(list_pedaleur, key=attrgetter('surnom'))

    def ajouterContrat(self,contrat, rang=None):
        if not contrat in self.listContrat:
            if not rang:self.listContrat.append(contrat)
            else:self.listContrat.insert(rang, contrat)
            contrat.tournee=self

    def retirerContrat(self,contrat):
        if contrat in self.listContrat:
            self.listContrat.remove(contrat)
            if contrat.tournee == self:
                contrat.tournee = None

    def ajouterParcours(self, parcours=None):
        if not parcours in self.listParcours:
            self.listParcours.append(parcours)
            parcours.tournee=self

    def retirerParcours(self, parcours=None):
        if parcours in self.listParcours:
            self.listParcours.remouve(parcours)
            parcours.tournee=None

    def _loadComposantes(self):
        """charge les contrats"""
        list_dbid_contrats=self._selectDbidContrat()
        if list_dbid_contrats:
            for dbid_contrat in list_dbid_contrats:
                contrat=self._mere.Contrat(dbid_contrat['dbid'])
                self.listContrat.append(contrat)
        list_dbid_parcours=self._selectDbidParcours()
        if list_dbid_parcours:
            for dbid_parcours in list_dbid_parcours:
                parcours=self._mere.Parcours(dbid_parcours['dbid'])
                self.listParcours.append(parcours)
        return True


class ContratK(SqlContratK, ObjetK):
    '''ObjetK qui represente les contrats (lieux/depots)'''
    def __init__(self,mere):
        SqlLieuK.__init__(self)
        ObjetK.__init__(self,mere)
        self.listDepot=[]
        self._client=None
        self._tournee=None
 
#    @property
#    def listDepot(self):
#        return  sorted(self._listDepot, key=attrgetter('surnom'))
#    @listDepot.setter
#    def listDepot(self,listDepot):
#        self._listDepot=listDepot

    @property
    def client(self):
        return self._client
    @client.setter
    def client(self,client):
        self.dbid_client=client.dbid
        self._client=client

    @property
    def tournee(self):
        return self._tournee
    @tournee.setter
    def tournee(self,tournee):
        self.dbid_tournee=tournee.dbid
        self._tournee=tournee

    @property
    def listLieu(self):
        listLieu=[]
        for depot in self.listDepot:
            for lieu in depot.listLieu:
                if not lieu in listLieu:
                    listLieu.append(lieu)
        return listLieu
 
    @property
    def prix(self):
        prix_v=0
        for depot in self.listDepot:prix_v+=depot.prix
        prix_v+=len(self.listLieu)*2
        prix_v-=self.remise
        return prix_v
 
    def ajouterDepot(self,depot):
        if not depot in  self.listDepot:
            depot.contrat=self
            self.listDepot.append(depot)
 
    def supprimerDepot(self,depot):
        if depot in self.listDepot:
            self.listDepot.remove(depot)
            depot.supprimer()

    def _loadComposantes(self):
        """charge client et charge les depots"""
        if self.dbid_tournee:self._tournee = self._mere.Tournee(self.dbid_tournee)
        if self.dbid_client:self._client = self._mere.Client(self.dbid_client)
        list_dbid_depots=self._selectDbidDepot()
        if list_dbid_depots:
            for dbid_depot in list_dbid_depots:
                depot=self._mere.Depot(dbid_depot['dbid'])
                self.listDepot.append(depot)
            return True
        return False
        
    def switchContrat(self,genre):
        """change le genre du contrat et lui donne le bon numerau"""
        self.genre=genre
        self.num=self._nouvNum()


class ClientK(SqlClientK, ObjetK):
    '''ObjetK qui represente les clients'''
    def __init__(self,mere):
        SqlClientK.__init__(self)
        ObjetK.__init__(self, mere) 
        self.listContrat=[]

    def _loadComposantes(self):
        """charge les contrats"""
        list_dbid_contrats=self._selectDbidContrat()
        if list_dbid_contrats:
            for dbid_contrat in list_dbid_contrats:
                contrat=self._mere.Contrat(dbid_contrat['dbid'])
                self.listContrat.append(contrat)
            return True
        return False

    def listContratDepuisTournee(self, tournee):
        """contratd du client de la tournee"""
        list_contrat=[]
        for contrat in tournee.listContrat:
            if contrat.client==self:list_contrat.append(contrat)
        return list_contrat
                
    def ajouterContrat(self,contrat):
        self.listContrat.append(contrat)
        contrat.client=self
#            self.pixmapObjetChange.connect(contrat.clientChange)
    
     
class AdresseK(SqlAdresseK, ObjetK):
    '''ObjetK qui represente une adresse'''
    def __init__(self,mere): 
        SqlAdresseK.__init__(self)
        ObjetK.__init__(self,mere) 
        self._lieu=None
        self._listResultatGeo=None #list de dict json des geolocs
        self._choixResultatGeo=None
    
    @property
    def point(self):
        return PointK(longitude=self.longitude, latitude=self.latitude,hauteur=self.hauteur, parent=self)   

    @property
    def lieu(self):
        return self._lieu
    @lieu.setter
    def lieu(self,lieu):
        self.dbid_lieu=lieu.dbid
        self._lieu=lieu

    def geocodage_s(self):
        """interroge google et recupe du DictK
        --> list de dict resultat (list(dict))"""
        add="{0},{1}+{2},FRANCE".format(self.adresse,self.ville,self.cp)
        url="http://maps.googleapis.com/maps/api/geocode/json?address={0}&components=country:FR&sensor=false".format(urllib.request.quote(add))
        data = urllib.request.urlopen(url).read()
        print(url)
        print(data)
        dictGeo=json.loads(data.decode())
        self._choixResultatGeo=None
        self._listResultatGeo=None
        list_resultat,i=[{'type':'Original','i':0,'adresse':self.adresse,'longitude':self.longitude,'latitude':self.latitude,'cp':self.cp,'ville':self.ville,'nom':self.lieu.nom}],0
        for lieuxGeo in dictGeo['results']:
            i+=1
            N,Rue,cp,ville,nom='','',0,'',''
            for adresseGeo in lieuxGeo['address_components']:
                if 'point_of_interest' in adresseGeo['types'] or 'establishment' in adresseGeo['types']:nom=adresseGeo['long_name']
                elif 'street_number' in adresseGeo['types']:N=adresseGeo['long_name']
                elif 'route' in adresseGeo['types']:Rue=adresseGeo['long_name']
                elif 'postal_code' in adresseGeo['types']:cp=int(adresseGeo['long_name'])
                elif 'locality' in adresseGeo['types']:ville=adresseGeo['long_name']
            latitude=float(lieuxGeo['geometry']['location']['lat'])
            longitude=float(lieuxGeo['geometry']['location']['lng'])
            adresse="{0} {1}".format(N,Rue)
            list_resultat.append({'type':'Geocodage','i':i,'adresse':adresse,'longitude':longitude,'latitude':latitude,'cp':cp,'ville':ville,'nom':nom})
        self._listResultatGeo=list_resultat
        if i==1:return 1
        else:return 0

    def geocodage(self):
        """interroge geocodeur et recupe du list deDict d''adresse geoloc
        --> list de dict resultat (list(dict))"""
        self._choixResultatGeo=None
        self._listResultatGeo=geocoder(adresse=self)
        if self._listResultatGeo:
            if len(self._listResultatGeo)>0: 
                self._choixResultatGeo=0
            return True 
        else: return False
        
    def _loadComposantes(self):
        """charge le lieu"""
        if self.dbid_lieu:self._lieu=self._mere.Lieu(self.dbid_lieu)
        
    def _matchingGeolocalisation(self,distance=1000):
        return self._selectDbidGeoloc(distance)


class LieuK(SqlLieuK, ObjetK):
    '''ObjetK qui represente un lieu
        .listAdresse : liste des adresses associées (list[Adresse])
        ._dictLieuCandida : dict lieux candidat
        '''
    def __init__(self,mere):
        SqlLieuK.__init__(self)
        ObjetK.__init__(self,mere)
        self.listAdresse=[]
        self._dictLieuCandidat={}
        self._adresseProvisoire=None #renvois l'adresse en edition
        self._listInfoLieuRes=[]#pour geoloc list de dict info lieu resultat matching
        self._infoLieuRes=None#pour geoloc type
        self._valueMatching=None#valeur de matching pour geoloc
        self._isAcceptable=None#importe ou n'importe pas lieux d'un listing dans Kaf (bool , comment)
        
    def _initObjetData(self,**arguments):
        """initialise lieux 
        en ajoutant une adresse"""
        adresse=self._mere.nouvAdresse(**arguments)
        self.adresse=adresse
        
    def _loadComposantes(self):
        """charge les adresses"""
        list_dbid_adresses=self._selectDbidAdresses()
        if list_dbid_adresses:
            for dbid_adresse in list_dbid_adresses:
                adresse=self._mere.Adresse(dbid_adresse['dbid'])
                self.listAdresse.append(adresse)
            return True
        return False

    @property
    def adresse(self):
        """renvoie la premiere adresse principale"""
        for adresse in self.listAdresse:
            if adresse.principale==1:return adresse
    @adresse.setter
    def adresse(self,adresse):
        """ajoute une adresse et la fixe comme principale"""
        for old_adresse in self.listAdresse:old_adresse.principale=0
        adresse.principale=1
        self.ajouterAdresse(adresse)

    def ajouterAdresse(self,adresse):
        """ajoute dans adresse et fixe les dbid"""
        adresse.lieu=self
        adresse.dbid_lieu=self.dbid
        self.listAdresse.append(adresse)
 
    @property
    def adresseProvisoire(self):
        """renvoie l'adresse provisoire et la cree s'il n'y en a pas"""
        if not self._adresseProvisoire:
            self._adresseProvisoire=self._mere.nouvAdresse(insert=False)
            self._adresseProvisoire.lieu=self
        return self._adresseProvisoire
    @adresseProvisoire.setter
    def adresseProvisoire(self,adresseProvisoire):
        self._adresseProvisoire= adresseProvisoire 
        self._adresseProvisoire.lieu=self

    @property
    def isAcceptable(self):
        """si le lieu est accpetable pour integration à la kaftiere
        return   : bool,comment"""
        if not self._isAcceptable:
            if self.adresse.longitude == 0 or self.adresse.latitude == 0 : self._isAcceptable = (False, 'non localisé')
            elif self.etat != 'ouvert': self._isAcceptable = (False, self.etat)
            elif self.isSature : self._isAcceptable = (False, 'est saturé')
            else:self._isAcceptable = (True, 'Ok')
        return self._isAcceptable
    @isAcceptable.setter
    def isAcceptable(self,boolean):
        if boolean: self._isAcceptable = (True, 'Ok')
        else:
            if self.adresse.longitude == 0 or self.adresse.latitude == 0 : self._isAcceptable = (False, 'non localisé')
            elif self.etat != 'ouvert': self._isAcceptable = (False, self.etat)
            elif self.isSature : self._isAcceptable = (False, 'est saturé')
            else: self._isAcceptable = (False, 'refus')

    @property
    def isSature(self):
        """si le lieu est saturé"""
        return False
 
    def dictDepotTournee(self, tournee):
        """rend un dict {client0:{depo0:num0,depo1:num1,...};client1:{depo0:num0,depo1:num1,...}...}"""
        dict_depot_tournee={}
        for contrat in tournee.listContrat:
            for depot in contrat.listDepot:
                quantite_lieu=depot.quantiteLieu(self)
                if quantite_lieu != 0 :
                    if dict_depot_tournee.get(contrat) : dict_depot_tournee[contrat][depot]=quantite_lieu
                    else : dict_depot_tournee[contrat]={depot:quantite_lieu}
        return dict_depot_tournee

    def setLieuRes(self, lieuRes):
        """applique un lieu/adresse matching lieuRes au lieu self"""
        self._infoLieuRes=lieuRes['type']
        self.dbid=lieuRes['dbid']
        self.nom=lieuRes['nom']
        self.adresse.adresse=lieuRes['adresse']
        self.adresse.cp=lieuRes['cp']
        #self.adresse.ville=lieuRes['ville']
        self.adresse.latitude=lieuRes['latitude']
        self.adresse.longitude=lieuRes['longitude']
        self.etat=lieuRes['etat']
        self.saturation_max=lieuRes['saturation_max']
        self.pertinence=lieuRes['pertinence']
  
    def rechercherLieuCandidats(self):
        """recherche dans la db les lieux qui corresponde géographiquement et nominalement au lieu"""
        self.adresse._matchingGeolocalisation()


class DepotK(ObjetK,SqlDepotK):
    '''ObjetK qui represente un Depot'''
    def __init__(self,mere):
        ObjetK.__init__(self,mere)
        SqlDepotK.__init__(self)
        self.dictLieuQuantite={}#dict sur les lieux des depot et leurs quantitées
        self._contrat=None
    
    @property
    def listLieu(self):
        return self.dictLieuQuantite.keys()

    @property
    def prix(self):
        prix_v=0
        for quantite in self.dictLieuQuantite.values():prix_v+= quantite*self.prix_unite
        return prix_v

    @property
    def contrat(self):
        return self._contrat     
    @contrat.setter
    def contrat(self,contrat):
        self.dbid_contrat=contrat.dbid
        self._contrat=contrat
               
    def quantiteLieu(self, lieu):
        """renvoie la quantite du depot pour le lieu"""
        return self.dictLieuQuantite.get(lieu, 0)
   
    def _loadComposantes(self):
        """charge contrat et les lieux/quantite"""
        if hasattr(self, 'dbid_contrat'):self._contrat=self._mere.Contrat(self.dbid_contrat)
        list_dbid_lieu_quantite=self._selectDbidLieuQuantite()
        if list_dbid_lieu_quantite:
            for dbid_lieu_quantite in list_dbid_lieu_quantite:
                lieu=self._mere.Lieu(dbid_lieu_quantite['dbid_lieu'])
                quantite=dbid_lieu_quantite['quantite']
                self.dictLieuQuantite[lieu]=quantite 
            return True
        return False 

    @property
    def infoQuantiteDepot(self):
        """nb de depot deja affecté"""
        quantite=0
        for quantite_lieu in self.dictLieuQuantite.values():
            quantite+=quantite_lieu
        return quantite
    
    def ajouterLieu(self,lieu,quantite=0):
        if not self.dictLieuQuantite.get(lieu):
            self.dictLieuQuantite[lieu]=int(quantite)       
            if self._insLieuQuantite(dbid_lieu=lieu.dbid,quantite=int(quantite)):return True
        return False
    
    def retirerLieu(self,lieu):
        if self._delLieu(lieu.dbid):
            del self.dictLieuQuantite[lieu]
            return True
        return False
    
    def upgradeLieu(self,lieu,quantite):
        """upgrade lieu avec quantite"""
        if self._upLieuQuantite(lieu.dbid,int(quantite)):
            self.dictLieuQuantite[lieu]=int(quantite)
            return True
        return False
         
    def setLieuQuantite(self,lieu,quantite=0):
        """gere lieu avec quantite"""
        if not self.dictLieuQuantite.get(lieu):
            if self.ajouterLieu(lieu,quantite):return True
        else:
            if quantite=='0' or quantite=='':
                if self.retirerLieu(lieu):return True
            elif int(quantite)>0:
                if self.upgradeLieu(lieu,quantite): return True
        return False


class PedaleurK(SqlPedaleurK, ObjetK):
    '''ObjetK qui represente les pedaleurs'''
    def __init__(self,mere):
        SqlPedaleurK.__init__(self)
        ObjetK.__init__(self, mere)
        
    def listParcoursDepuisTournee(self, tournee):
        """retourne les parcours du pedaleur dans la tournée"""
        list_parcours=[]
        for parcours in tournee.listParcours:
            if parcours.pedaleur==self:list_parcours.append(parcours)
        return list_parcours





