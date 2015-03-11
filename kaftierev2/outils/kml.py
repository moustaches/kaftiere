import simplekml as SK
import xml.etree.ElementTree as ET
from objets.objet_qt import PedaleurQ,ParcoursQ,AdresseQ,ClientQ,ContratQ,DepotQ,LieuQ,TourneeQ

class Kml():
    NS = {'loc':"http://www.opengis.net/kml/2.2" ,
          'gx':"http://www.google.com/kml/ext/2.2", 
          'kml':"http://www.opengis.net/kml/2.2", 
          'atom':"http://www.w3.org/2005/Atom"} 
          
    def __init__(self, racine=None, regle=None, mere=None, nom='', destination=None):
        self.racine=racine
        self.kml_racine=SK.Kml(name=nom)
        self.regle=regle
        self.mere=mere
        self.editerSchema()
        self.kmlConstructeur(self.racine,self.kml_racine)
        self.kml_racine.save(destination)
        
    def editerSchema(self):
        schema = self.kml_racine.newschema(name='Kaf')
        schema.newsimplefield(name='dbid', type='int', displayname='identifier')
        schema.newsimplefield(name='kaf_objet', type='str', displayname='type')

    def kmlConstructeur(self, objetQ, kml):
        if not self.regle:
            if isinstance(objetQ,ClientQ):
                kml_dossier=kml.newfolder(name='{}'.format(objetQ.nom))
                kml_dossier.extendeddata.schemadata.newsimpledata('kaf_objet', 'Client')
                kml_dossier.extendeddata.schemadata.newsimpledata('dbid', objetQ.dbid) 
            if isinstance(objetQ,ContratQ):
                kml_dossier=kml.newfolder(name='{} n°{}'.format(objetQ.client.nom, objetQ.num))
                kml_dossier.extendeddata.schemadata.newsimpledata('kaf_objet', 'Contrat')
                kml_dossier.extendeddata.schemadata.newsimpledata('dbid', objetQ.dbid) 
            if isinstance(objetQ,DepotQ):
                kml_dossier=kml.newfolder(name='{}'.format(objetQ.nom))
                kml_dossier.extendeddata.schemadata.newsimpledata('kaf_objet', 'Depot')
                kml_dossier.extendeddata.schemadata.newsimpledata('dbid', objetQ.dbid) 
            if isinstance(objetQ,ParcoursQ):
                kml_dossier=kml.newfolder(name='P{}'.format(objetQ.dbid))
                kml_dossier.extendeddata.schemadata.newsimpledata('kaf_objet', 'Parcours')
                kml_dossier.extendeddata.schemadata.newsimpledata('dbid', objetQ.dbid) 
            if isinstance(objetQ,TourneeQ):
                kml_dossier=kml.newfolder(name='Tournée {}'.format(objetQ.date_ouverture))
                kml_dossier.extendeddata.schemadata.newsimpledata('kaf_objet', 'Tournee')
                kml_dossier.extendeddata.schemadata.newsimpledata('dbid', objetQ.dbid) 

            if isinstance(objetQ,TourneeQ):
                kml_dossier_lieu=kml_dossier.newfolder(name='Lieux sans parcours')   
                for lieu in objetQ.listLieuSansParcours:
                    kml_lieu=kml_dossier_lieu.newpoint(name='{}'.format(lieu.nom),coords=[lieu.adresse.point.kmlCoordonnees])
                    kml_lieu.extendeddata.schemadata.newsimpledata('kaf_objet', 'Lieu')
                    kml_lieu.extendeddata.schemadata.newsimpledata('dbid', lieu.dbid)
                    
            if isinstance(objetQ,(ClientQ,ContratQ,DepotQ,ParcoursQ)):
                kml_dossier_lieu=kml_dossier.newfolder(name='Lieux')   
                for lieu in objetQ.listLieu:
                    kml_lieu=kml_dossier_lieu.newpoint(name='{}'.format(lieu.nom),coords=[lieu.adresse.point.kmlCoordonnees])
                    kml_lieu.extendeddata.schemadata.newsimpledata('kaf_objet', 'Lieu')
                    kml_lieu.extendeddata.schemadata.newsimpledata('dbid', lieu.dbid)                    
                    
            if isinstance(objetQ,(ParcoursQ)):
                if objetQ.chemin:
                    kml_chemin=kml_dossier.newlinestring(name='C {}'.format(objetQ.dbid),coords=objetQ.chemin.kmlCoordonnees)
                    kml_chemin.style.linestyle.width= 5
                    kml_chemin.extendeddata.schemadata.newsimpledata('kaf_objet', 'Chemin')
                    kml_chemin.extendeddata.schemadata.newsimpledata('dbid', objetQ.dbid)
            if isinstance(objetQ,(ParcoursQ)):
                if objetQ.shape:
                    kml_shape=kml_dossier.newpolygon(name='S {}'.format(objetQ.dbid),outerboundaryis=objetQ.shape.kmlCoordonnees)
                    kml_shape.style.polystyle.color='#80'+objetQ.pedaleur.couleur[1:]#ajout 50% transparence
                    kml_shape.extendeddata.schemadata.newsimpledata('kaf_objet', 'Shape')
                    kml_shape.extendeddata.schemadata.newsimpledata('dbid', objetQ.dbid)
                
            if isinstance(objetQ,TourneeQ):
                if objetQ.listContrat:
                    kml_dossier_contrats=kml.newfolder(name='Contrats')
                    for contrat in objetQ.listContrat :self.kmlConstructeur( contrat, kml_dossier_contrats)
                if objetQ.listParcours:
                    kml_dossier_parcours=kml.newfolder(name='Parcours')                
                    for parcours in objetQ.listParcours :self.kmlConstructeur(parcours, kml_dossier_parcours)


class KmlParser():
    NS = {'loc':"http://www.opengis.net/kml/2.2" ,
      'gx':"http://www.google.com/kml/ext/2.2", 
      'kml':"http://www.opengis.net/kml/2.2", 
      'atom':"http://www.w3.org/2005/Atom"} 
    
    def __init__(self, racine=None, regle=None, mere=None, source=None):
        self.racine=racine
        self.regle={
        'Shape':{'Changer coords':True, 'Deshaper':True},
        'Chemin':{'Changer coords':True, 'Cheminer':True},
        'Lieu':{'Changer nom':False,'Changer coords':False}, 
        'Dossier':{'Changer nom':False}
        }
        self.mere=mere
        self.listShape=[]
        kml_root=ET.parse(source).getroot()
        kml_document=kml_root.find('loc:Document',namespaces=KmlParser.NS)
        self.kobjetRoot=self.KmlToObjet(kml_document.find('loc:Folder',namespaces=KmlParser.NS))
        print(self.kobjetRoot)
        self.parser(kml_document)
        self.appliquer()
       
    def KmlToObjet(self, kml):
        """rend objetQ"""
        kml_schemadata=kml.findall('loc:ExtendedData/loc:SchemaData/loc:SimpleData',namespaces=KmlParser.NS) 
        if kml_schemadata:
            for schemadata in kml_schemadata:
                if schemadata.attrib['name']=='kaf_objet':schemadata_objet=schemadata.text
                if schemadata.attrib['name']=='dbid':schemadata_dbid=int(schemadata.text)
            objet=getattr(self.mere,schemadata_objet)(schemadata_dbid)
            return objet
        else: return None
    
    def lieuParser(self,kml_lieu):     
        lieu=self.KmlToObjet(kml_lieu)
        if lieu:
            if self.regle:
                if self.regle['Lieu']['Changer nom']:lieu.nom=kml_lieu.find('loc:name',namespaces=KmlParser.NS).text
                if self.regle['Lieu']['Changer coords']:lieu.kmlCoordonnees=kml_lieu.find("loc:Point/loc:coordinates",namespaces = KmlParser.NS).text 
            return lieu                 
        else: return None  
    
    def shapeParser(self,kml_shape):
        shape=self.KmlToObjet(kml_shape)
        if shape:
            if self.regle['Shape']['Changer coords']:
                shape.kmlCoordonnees= kml_shape.find('loc:Polygon/loc:outerBoundaryIs/loc:LinearRing/loc:coordinates',namespaces=KmlParser.NS).text           
            self.listShape.append(shape)
            return shape
        return None
        
    def cheminParser(self,kml_chemin):
        chemin=self.KmlToObjet(kml_chemin)
        if chemin:
            if self.regle['Chemin']['Changer coords']:
                chemin.kmlCoordonnees=kml_chemin.find('loc:LineString/loc:coordinates',namespaces=KmlParser.NS).text
                print("chemin "+str(chemin.parent.dbid))
                print(list(chemin.kmlCoordonnees))
            return chemin
        return None
        
    def dossierParser(self,kml_folder): 
        dossier=self.KmlToObjet(kml_folder)
        if dossier:
            if self.regle:
                if self.regle['Dossier']['Changer nom']:pass
            return dossier
        else :return None

    def parser(self,kml):
        kml_placemarks=kml.findall('loc:Placemark',namespaces=KmlParser.NS)
        for kml_placemark in kml_placemarks:
            if kml_placemark.find('loc:Point',namespaces=KmlParser.NS): self.lieuParser( kml_placemark)
            elif kml_placemark.find('loc:LineString',namespaces=KmlParser.NS): self.cheminParser(kml_placemark)
            elif kml_placemark.find('loc:Polygon',namespaces=KmlParser.NS) :self.shapeParser(kml_placemark)           
        kml_folders=kml.findall('loc:Folder',namespaces=KmlParser.NS)
        for kml_folder in kml_folders:
            self.dossierParser(kml_folder)
            self.parser(kml_folder)
            
    def appliquer(self):
        """applique changement selon regles"""
        if self.regle['Shape']['Deshaper']:
                if isinstance(self.kobjetRoot,TourneeQ):
                    for parcours in self.kobjetRoot.listParcours:parcours.Deshaper()
        if self.regle['Chemin']['Cheminer']:
                if isinstance(self.kobjetRoot,TourneeQ):
                    for parcours in self.kobjetRoot.listParcours:parcours.Cheminer()      







