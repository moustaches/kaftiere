import math

class PointK():
    """class point"""
    def __init__(self, longitude=0, latitude=0,hauteur=0, parent=None):
        self.parent=parent
        self.longitude=longitude
        self.latitude=latitude
        self.hauteur=hauteur
        
    def distance(self, point):
        return math.sqrt(pow(self.longitude - point.longitude, 2) + pow(self.latitude - point.latitude, 2))
        
    def matchingLieu(self, listLieu=None):
        """retourn le lieu le plus proche"""
        matching_lieu, matching_dist=None, 1000
        for lieu in listLieu:
            dist=self.distance(lieu.adresse.point)
            if matching_dist>dist:
                matching_lieu=lieu
                matching_dist=dist
        return matching_lieu,  matching_dist

    @property
    def kmlCoordonnees(self):
        return (self.longitude,self.latitude,self.hauteur)
    @kmlCoordonnees.setter
    def kmlCoordonnees(self,coords):
        coords=coords.split(",")
        self.latitude=float(coords[1])
        self.longitude=float(coords[0])
        self.hauteur=float(coords[2])        
        
        
class ShapeK():
    """class shape"""
    def __init__(self, shape=None,str_polygon=None,parent=None, mere=None):
        self.parent=parent
        self._mere=mere
        self._mere.dictShape[parent.dbid]=self
        self._shape=(PointK(longitude=2.2923,latitude=48.8578, parent=self),
        PointK(longitude=2.2951, latitude=48.8596, parent=self),
        PointK(longitude=2.2969,latitude=48.8565, parent=self)) #chaine fermé de poink
        if shape:self.shape=shape
        elif str_polygon:self.shape=shape
        elif parent:
            if parent.polygon:self._shape=self.formatStrToKaf(parent.polygon)
            
    @property
    def shape(self):
        return self._shape
    @shape.setter
    def shape(self,shape):
        if isinstance(shape, list):
            self._shape=shape
            if self.parent:self.parent.polygon=self.formatKaftoStr(shape)
        elif isinstance(shape, str):
            self._shape=self.formatStrToKaf(shape)
            if self.parent:self.parent.polygon=shape

    @property
    def kmlCoordonnees(self):
        return map(lambda poink: poink.kmlCoordonnees,self._shape)
    @kmlCoordonnees.setter
    def kmlCoordonnees(self,kml_coordonnees):
        kml_coordonnees=kml_coordonnees.strip()
        list_str_point=kml_coordonnees.split(' ')        
        kaf_polygon=[]
        for str_point in list_str_point:
            str_lat_long=str_point.split(',')
            lon=float(str_lat_long[0])
            lat=float(str_lat_long[1])        
            point=PointK(longitude=lon,latitude=lat,parent=self)
            kaf_polygon.append(point)
        self.shape=kaf_polygon
        
    def formatStrToKaf(self, str_polygon):
        list_str_point= str_polygon[2:-2]
        list_str_point=list_str_point.split('),(')
        kaf_polygon=[]
        for str_point in list_str_point:
            str_lat_long=str_point.split(',')
            lon=float(str_lat_long[0])
            lat=float(str_lat_long[1])
            point=PointK(longitude=lon,latitude=lat,parent=self)
            kaf_polygon.append(point)
        return kaf_polygon

    def formatKaftoStr(self, kaf_polygon):
        list_str_point=''
        for point in kaf_polygon:
            str_point=",({},{})".format(point.longitude,point.latitude)
            list_str_point+=str_point
        str_polygon= "("+list_str_point[1:]+")"
        return str_polygon

    def deshaper0bjet(self,objet_geo=None):
        """
        prend objet contenant .latitude et .longitude
        et rend true ou false s'il appartient a la shape
        """      
        i=0      
        point0=self.shape[0]    
        for point1 in self.shape[1:]:
            if (objet_geo.longitude < point0.longitude and objet_geo.longitude > point1.longitude) or (objet_geo.longitude > point0.longitude and objet_geo.longitude < point1.longitude):
                if not objet_geo.latitude < min(point0.latitude,point1.latitude):
                    if ((point0.latitude-point1.latitude)/(point0.longitude-point1.longitude)*(objet_geo.longitude-point0.longitude))+point0.latitude < objet_geo.latitude:i+=1
            point0=point1          
        if i % 2 == 1:return True
        else:return False
        
        
class CheminK():
    """class chemin"""
    def __init__(self, list_point=None,list_lieu=None, parent=None,  mere=None):
        self.parent=parent
        self._mere=mere
        self._mere.dictChemin[parent.dbid]=self
        self._chemin=None#suite de dbid lieu
        if self.parent:
            if self.parent.line:self._chemin=self.parent.line

    @property
    def listLieu(self):
        if self.chemin:
            return map(lambda dbid: self._mere.Lieu(dbid),self.chemin)
        else :return []

    @property
    def longueur(self):
        listLieu=list(self.listLieu)
        d0=0
        if len(listLieu)>1:
            for lieu1, lieu2 in zip(listLieu,listLieu[1:]):d0+=self.distance(lieu1, lieu2)
        return d0

    def distance(self, lieu1, lieu2):
        """
        calcule la distance sur une sphere de deux point
        """
        lon1, lat1, lon2, lat2 = map(math.radians, [lieu1.adresse.longitude, lieu1.adresse.latitude, lieu2.adresse.longitude,lieu2.adresse.latitude])
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 
        km = 6367 * c
        return km

    @property
    def kmlCoordonnees(self):
        if self.listLieu:
            return map(lambda lieu: lieu.adresse.point.kmlCoordonnees, self.listLieu)
        else : return [(2.2923,48.8578)]
    @kmlCoordonnees.setter
    def kmlCoordonnees(self,kml_coordonnees):
        kml_coordonnees=kml_coordonnees.strip()
        list_str_point=kml_coordonnees.split(' ')      
        line=[]
        for str_point in list_str_point:
            str_lat_long=str_point.split(',')
            lon=float(str_lat_long[0])
            lat=float(str_lat_long[1])        
            point=PointK(longitude=lon,latitude=lat,parent=self)
            lieu=point.matchingLieu(self.parent.listLieu)[0]
            if lieu:
                line.append(lieu.dbid)
        self.chemin=line
        
    @property
    def chemin(self):
        return self._chemin
    @chemin.setter
    def chemin(self,chemin):
        self._chemin=chemin
        if self.parent:self.parent.line=chemin
            


