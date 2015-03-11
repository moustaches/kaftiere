'''
Created on 5 avr. 2013

@author: moustache
'''
import psycopg2

def get_cursor():
    """Connection a la data-base Postgres et return un cursor standard"""
    global CURSOR
    if not CURSOR:
        connectionDBPostgres()
        CURSOR = conn.cursor()
    return CURSOR

def connectionDBPostgres(nom_base="BASE_KAFEINE",user="axou",password="pw",host="localhost"):
    """Connection a la data-base Postgres
    db.set_isolation_level(0) autorise toutes transactions"""
    try:
        conn = psycopg2.connect("dbname={} user={} password={} host={}".format(nom_base,user,password,host))
        conn.set_isolation_level(0)
        print("Connection DB a: dbname={} user={} password={} host={}".format(nom_base,user,password,host))
    except:
        print("Probleme de connection")
    global CURSOR    
    CURSOR = conn.cursor()    
    return True

def sql_insert(table,dict_args,returning,verbose):
    """Insert dict_args dans la table et rend l'id
        -->
            table: nom de la table (str)
            dict_args: {argument:valeur, ...} (dict)
            returning: return le nouveau dbid si True (bool)
            verbose: commente dans la console si True (bool)
        <--
            controleur,None  (bool) si  returning=False
            controleur,dbid  (bool,int) si returning=True
    """    
    if returning:
        get_cursor().execute("INSERT INTO {} ({}) VALUES ({}) RETURNING dbid;".format(table,','.join(list(dict_args.keys())),(len(dict_args)*'%s,')[:-1]),list(dict_args.values()))
    else:
        get_cursor().execute("INSERT INTO {} ({}) VALUES ({});".format(table,",".join(list(dict_args.keys())),(len(dict_args)*'%s,')[:-1]),list(dict_args.values()))        
    if verbose:print(get_cursor().query)
    if returning:return True,get_cursor().fetchone()[0]
    else:return True, None

def sql_update(table,dict_args,str_conditions,verbose):
    """Update avec dict_args dans la table qui coorespond aux conditions
        -->
            table: nom de la table (str)
            dict_args: {argument:valeur, ...} (dict)
            str_conditions: conditions logiques (str) WHERE '(cond1 and cond2) or ...)
            verbose: commente dans la console si True (bool)
        <--
            controleur (bool)
    """    
    try:
        get_cursor().execute("UPDATE {0} SET {1} WHERE {2}".format(table,",".join(map(lambda x:x+'=%s',list(dict_args.keys()))),str_conditions),list(dict_args.values()))
    except Exception as e:
        if verbose:
            print(get_cursor().query)
            print(e)
        return False
    if verbose:print(get_cursor().query)
    return True
    
def sql_select(table,list_args,str_conditions,list_val_conditions,verbose):
    """SELECT  list_args dans la table qui coorespond aux conditions
        -->
            table: nom de la table (str)
            list_args: [argument1,argument2,...] (list)
            str_conditions: conditions logiques avec ?"(cond1=? AND cond2 = cond3) OR cond4=?" (str)
                            None si pas de condition
            list_val_conditions: val des condition [val1,val2] (list)
                            None si pas de condition
            verbose: commente dans la console si True (bool)
        <--
            liste de dictionnaire de list_args list(dict)""" 
    if str_conditions:
        get_cursor().execute("SELECT {} FROM {} WHERE {};".format(",".join(list_args),table,str_conditions),list_val_conditions )
    else:
        get_cursor().execute("SELECT {} FROM {};".format(",".join(list_args), table))
    if verbose:print(get_cursor().query)
    list_resultat=[]
    for record in get_cursor():
        i=0
        arg_dict={}
        for arg in list_args:
            arg_dict[arg]=record[i]
            i+=1
        list_resultat.append(arg_dict)    
    return list_resultat       
      
    
def sql_delete(table,str_conditions,verbose):
    """DELETE  objet dans la table qui coorespond aux conditions
        -->
            table: nom de la table (str)
            str_conditions: conditions logiques (str)  ex:"(cond1=? AND cond2 = cond3) OR cond4=?" 
            verbose: commente dans la console si True (bool)
        <--
           list[dict_args]: [{argument0,1:valeur0,1,argument0,2:valeur0,2, ...},{argument1,1:valeur1,1,argument1,2:valeur1,2, ...},..] (dict)
    """         
    
    try:
        get_cursor().execute("DELETE FROM {} WHERE {};".format(table,str_conditions))
    except Exception as e:
        if verbose:
            print(get_cursor().query)
            print(e)
        return False
    if verbose:print(get_cursor().query)
    return True
   
    
class SqlTable(object):
    """
    Objet pour les set_tables fixes
    -->
    str_table: nom de la table (str)
    list_args: list pertinantz de colonne de la table (list (str)) 
    <--
    data:
    table:
    """
    def __init__(self,str_table,list_args,verbose):
        self.table=str_table
        self.list_args=list_args
        self._verbose=verbose
        self.data_dbid,self.data_arg=self.loadTable()
       
    def loadTable(self):
        """charge la table
        <--
        data_dbid = {dbid:{arg2:val2,arg3:val3,...},...}
        data_arg = {dbid:[dbid1,dbid2...],arg2:[val1,val2...]}"""
        if self._verbose:print('charge table fixe: {}'.format(self.table))
        list_sel=sql_select(self.table, self.list_args,None,None,self._verbose)
        dict_dbid={}
        dict_arg={}
        for arg in list_sel[0].keys():
            dict_arg[arg]=[]
        for sel in list_sel:
            dbid=sel.pop('dbid')
            dict_arg['dbid'].append(dbid)
            dict_dbid[dbid]=sel
            for arg,val in sel.items():
                dict_arg[arg].append(val)
        return dict_dbid,dict_arg
       
    def dbidToArg(self,nom_arg,dbid):
        """Avec l'id donne la valeur de l'arg
        -->
        dbid: id dans db (int)
        nom_arg: nom de l'argument (str)
        <--
        valeur de l'arg: (int,str,...)"""
        try:
            return self.data_dbid[dbid][nom_arg]
        except  ValueError:
            print('Probleme de matching dbidToArg sur {} avec {} pour {}'.format(self.table,nom_arg,dbid))
            return None
        
    def argToDbid(self,nom_arg,arg):
        """Avec la valeur de l'arg et l'arg donne la valeur de l'id
        -->
        dbid: id dans db (int)
        nom_arg: nom de l'argument (str)
        arg: valeur (str,int,...)
        <--
        id: (int)"""
        #return self.data_arg['dbid'][self.data_arg[nom_arg].index(arg)]
        try:
            return self.data_arg['dbid'][self.data_arg[nom_arg].index(arg)]
        except  ValueError:
            print('Probleme de matching argToDbid sur {} avec {} pour {}'.format(self.table,nom_arg,arg))
            return None
        
        
class SqlObjetK(object):
    """
    Super Classe dont derivera les sql objetK
    dbid : id unique qui coorespond a la db (int)
    _updatable : l'objet peut modifier la db (bool)
    _verbose : commente dans la console si True (bool)
    """
    
    def __init__(self):
        self.dbid=None
        self._updatable=True
        self._verbose=False
        
    def __setattr__(self, *args, **kwargs):
        """Update les attibut de l'objet en direct"""
        if args[0] in self.SQL_ARGS:
            if self._updatable:
                self._sqlUpdate({args[0]:args[1]})
            return object.__setattr__(self,args[0],args[1])
        else:
            return object.__setattr__(self, *args, **kwargs)

    def __repr__(self):
        if hasattr(self,'dbid'):return "{} {}".format(self.__class__.__name__, self.dbid)
        else:return "{}".format(self.__class__.__name__)

    def _initSqlData(self,**arguments):
        SELF_INIT_SQL_ARGS=self.INIT_SQL_ARGS.copy()
        for arg,val in arguments.copy().items():
            if arg in SELF_INIT_SQL_ARGS.keys():
                SELF_INIT_SQL_ARGS[arg]=arguments.pop(arg)
        for arg,val in SELF_INIT_SQL_ARGS.items():        
            self.__setattr__(arg,val)

    def _sqlInsert(self):
        """Insert objet dans db son dict_args et lui donne son dbid et le range dans le dict des fils de mere"""   
        dict_args={} 
        for arg in self.SQL_ARGS:
            dict_args[arg]=getattr(self, arg)
        var_dbid = sql_insert(self.SQL_TABLE,dict_args,True,self._verbose)
        if var_dbid[0]:
            self.dbid=var_dbid[1]
            getattr(self._mere,self.NAME_DICT_MERE)[self.dbid]=self #range dans le dict des fils de mere
            return True
        else: return False
        
    def _sqlUpdate(self,dict_args):
        """Update objet dans db son dict_args"""
        if self.dbid:
            str_conditions="dbid = {}".format(self.dbid)
            if sql_update(self.SQL_TABLE,dict_args,str_conditions,self._verbose):return True
        else: return False
        
    def _sqlDelete(self):
        """Supprime objet dans db"""        
        if self._updatable:
            if self.dbid:
                str_conditions="dbid = {}".format(self.dbid)
                if sql_delete(self.SQL_TABLE,str_conditions,self._verbose):
                    del getattr(self._mere,self.NAME_DICT_MERE)[self.dbid] #supprime ref du dict mere
            return True
        else: return False
        
    def _sqlLoad(self,dbid):
        """Charge les arg de l'objet selon bdid"""
        self._updatable=False
        str_conditions="dbid = %s"
        list_val_conditions=[dbid] 
        list_dict_args= sql_select(self.SQL_TABLE,self.SQL_ARGS,str_conditions,list_val_conditions,self._verbose)
        if list_dict_args:
            for key,val in list_dict_args[0].items():
                setattr(self,key,val)
            self.dbid=dbid
            self._updatable=True
            return True
        else :
            self._updatable=True
            return False
        
        
class SqlClientK(SqlObjetK):
    """Sous class sql du client"""
    SQL_ARGS=['nom','surnom','dbid_lieu','dbid_genre']
    SQL_TABLE='clients_tb'
    INIT_SQL_ARGS={'nom':'Nouveau client','surnom':'N.C','dbid_lieu':833,'dbid_genre':1}
    NAME_DICT_MERE='dictClient'
    
    def __init__(self):
        SqlObjetK.__init__(self)
        self._genre=None
        
    @property
    def genre(self):
        if not self._genre:
            self._genre=self._mere.genresclients_tb.dbidToArg('genre',self.dbid_genre)  
        return self._genre
    @genre.setter
    def genre(self,genre):
        dbid=self._mere.genresclients_tb.argToDbid('genre',genre)
        self.dbid_genre=dbid
        self._genre=genre
        
    def _selectDbidContrat(self):
        """Select les contrats du client et rend liste des dbid contrat"""
        return sql_select('contrats_tb', ['dbid'],'dbid_client = %s', [self.dbid], self._verbose)  

    def sqlInsert(self,composentes=True):
        """S'insert lui même et ses composentes"""
        if not self.dbid :
            self._sqlInsert()
            return True
        else:return False        
    
    
class SqlTourneeK(SqlObjetK):
    """Sous class sql de la Tournee"""
    SQL_ARGS=['date_ouverture','date_cloture']
    SQL_TABLE='tournees_tb'
    INIT_SQL_ARGS={'date_ouverture':None,'date_cloture':None}
    NAME_DICT_MERE='dictTournee'
    
    def __init__(self):
        SqlObjetK.__init__(self)

    def _selectDbidContrat(self):
        """Select les contrats de la tournée et rend liste des dbid contrat"""
        return sql_select('contrats_tb', ['dbid'],'dbid_tournee = %s', [self.dbid], self._verbose)          

    def _selectDbidParcours(self):
        """Select les Parcours de la tournée et rend liste des dbid Parcours"""
        return sql_select('parcours_tb', ['dbid'],'dbid_tournee = %s', [self.dbid], self._verbose)   

    def sqlInsert(self,composentes=True):
        """S'insert lui même et ses composentes"""
        if not self.dbid :
            self._sqlInsert()
            return True
        else:return False  
        

class SqlParcoursK(SqlObjetK):
    """Sous class sql du parcours"""
    SQL_ARGS=['dbid_tournee','dbid_pedaleur','polygon', 'line']
    SQL_TABLE='parcours_tb'
    INIT_SQL_ARGS={'dbid_pedaleur':None,'dbid_tournee':None, 'polygon':None, 'line':None}# 
    NAME_DICT_MERE='dictParcours'
   
    def __init__(self):
        SqlObjetK.__init__(self)
        self._list_dbid_lieu=[]
    
    @property
    def list_dbid_lieu(self):
        if not self._list_dbid_lieu:
            try:
                get_cursor().execute("SELECT list_dbid_lieu FROM parcours_tb WHERE dbid = %s", (self.dbid,))
                self._list_dbid_lieu=get_cursor().fetchall()[0][0]
            except Exception as e:
                if True:
                    print(get_cursor().query)
                    print(e)
                    print(self._list_dbid_lieu)
                    print(get_cursor().fetchall())
                return False
        return self._list_dbid_lieu
    @list_dbid_lieu.setter
    def list_dbid_lieu(self,list_dbid_lieu):
        if not list_dbid_lieu: 
            sql_list_dbid_lieu='\'{0}\'::int[]'.format('{}')
        else:
            sql_list_dbid_lieu='\'{}\'::int[]'.format('{'+','.join(list_dbid_lieu)+'}')
        try:
            get_cursor().execute("UPDATE parcours_tb SET list_dbid_lieu={0} WHERE dbid = {1}".format(sql_list_dbid_lieu, self.dbid))
        except Exception as e:
            if True:
                print(get_cursor().query)
                print(e)
            return False
        return True  
        self._list_dbid_lieu=list_dbid_lieu
        
    def sqlInsert(self,composentes=True):
        """S'insert lui même et ses composentes"""
        if not self.dbid :
            self._sqlInsert()
            return True
        else:return False

    def sqlDelete(self):
        """Se supprime lui même et ses composentes"""
        if self._updatable:
            if self._sqlDelete():
                return True
        return False

    def _selectDbidLieuOrdre(self):
        """Select les lieux et la quantitee dans les lieux"""
        return sql_select('parcours_lieux_tb',['dbid_lieu','ordre'],'dbid_parcours = %s',[self.dbid],self._verbose)       
        
        
class SqlContratK(SqlObjetK):
    """Sous class sql du contrat"""
    SQL_ARGS=['dbid_client','dbid_tournee','date_ouverture','date_cloture','remise','num','dbid_genre','date_debut_prestation','date_fin_prestation']
    SQL_TABLE='contrats_tb'
    INIT_SQL_ARGS={'dbid_client':None,'dbid_tournee':None,'date_ouverture':None,'date_cloture':None,'remise':0,'num':None,'dbid_genre':None,'date_debut_prestation':None,'date_fin_prestation':None}
    NAME_DICT_MERE='dictContrat'
   
    def __init__(self):
        SqlObjetK.__init__(self)
        self._genre=None
        
    @property
    def genre(self):
        if not self._genre:
            self._genre=self._mere.genrescontrats_tb.dbidToArg('genre',self.dbid_genre)  
        return self._genre
    @genre.setter
    def genre(self,genre):
        dbid=self._mere.genrescontrats_tb.argToDbid('genre',genre)
        self.dbid_genre=dbid
        self._genre=genre

    def _selectDbidDepot(self):
        """Select les depots de la tournée et rend liste des dbid depot"""
        return sql_select('depots_tb', ['dbid'],'dbid_contrat = %s', [self.dbid], self._verbose)  
      
    def _nouvNum(self):
        """attribut un nouveau num en prenant le max +1 de son genre"""
        num=sql_select('contrats_tb', ['max(num)'],'dbid_genre=%s',[self.dbid_genre], self._verbose)
        if num[0]['max(num)']:return num[0]['max(num)']+1
        else :return 1

    def sqlInsert(self,composentes=True):
        """S'insert lui même et ses composentes"""
        if not self.dbid :
            self._sqlInsert()
            return True
        else:return False
  
  
class SqlLieuK(SqlObjetK):
    """Sous class sql du lieux"""
    SQL_ARGS=['nom','pertinence','dbid_genre','dbid_etat', 'commentaire', 'saturation_max']
    SQL_TABLE='lieux_tb'
    INIT_SQL_ARGS={'dbid_genre':6,'pertinence':0,'nom':'super nom inconnu','dbid_etat':6, 'commentaire':'',  'saturation_max':0}
    NAME_DICT_MERE='dictLieu'
    
    def __init__(self):
        SqlObjetK.__init__(self)
        self._genre=None
        self._etat=None
        
    @property
    def genre(self):
        if not self._genre:
            self._genre=self._mere.genreslieux_tb.dbidToArg('genre',self.dbid_genre)  
        return self._genre
    @genre.setter
    def genre(self,genre):
        dbid=self._mere.genreslieux_tb.argToDbid('genre',genre)
        self.dbid_genre=dbid
        self._genre=genre
    @property
    def etat(self):
        if not self._etat:
            self._etat=self._mere.etatslieux_tb.dbidToArg('etat',self.dbid_etat)  
        return self._etat
    @etat.setter
    def etat(self,etat):
        dbid=self._mere.etatslieux_tb.argToDbid('etat',etat)
        self.dbid_etat=dbid
        self._etat=etat
    
    def _selectDbidAdresses(self):
        """Select les adresses du lieux et rend liste des dbid d'adresse"""
        return sql_select('adresses_tb', ['dbid'],'dbid_lieu = %s', [self.dbid], self._verbose)

    def _selectDbidNom(self):
        """Select les lieux qui porte le même nom liste des dbid lieux"""
        return sql_select('lieux_tb', ['dbid'],'nom = %s', [self.nom], self._verbose)
    
    def sqlInsert(self,composentes=True):
        """S'insert lui même et ses composentes"""
        if not self.dbid :self._sqlInsert()
        if composentes:
            for adresse in self.listAdresse:
                adresse.dbid_lieu=self.dbid
                adresse.sqlInsert()
    

class SqlPedaleurK(SqlObjetK):
    """Sous class sql Pedaleur"""
    SQL_ARGS=['nom','prenom','surnom','dbid_lieu', 'couleur']
    INIT_SQL_ARGS={'nom':'nom inconnu','prenom':'prenom inconnu','surnom':'surnom inconnu','dbid_lieu':None, 'couleur':'#ffffff'}
    SQL_TABLE='pedaleurs_tb'
    NAME_DICT_MERE='dictPedaleur'
    def __init__(self):
        SqlObjetK.__init__(self)
    
    def sqlInsert(self,composentes=True):
        """S'insert lui même et ses composentes si pas de dbid"""
        if not self.dbid:
            return self._sqlInsert()



class SqlAdresseK(SqlObjetK):
    """Sous class sql de l'adresse"""
    SQL_ARGS=['adresse','dbid_cp_ville','principale','longitude','latitude','hauteur','dbid_lieu']
    INIT_SQL_ARGS={'adresse':'Adresse inconnue','dbid_cp_ville':11678,'principale':1,'longitude':0,'latitude':0,'hauteur':0,'dbid_lieu':None}
    SQL_TABLE='adresses_tb'
    NAME_DICT_MERE='dictAdresse'
    def __init__(self):
        SqlObjetK.__init__(self)
        self._cp=None
        self._ville=None

    @property
    def genre(self):
        if not self._genre:self._genre=self._mere.genresdepots_tb.dbidToArg('genre',self.dbid_genre)  
        return self._genre
    @genre.setter
    def genre(self,genre):
        dbid=self._mere.genresdepots_tb.argToDbid('genre',genre)
        self.dbid_genre=dbid
        self._genre=genre
    @property
    def cp(self):
        if not self._cp:self._cp=self._mere.cpvilles_tb.dbidToArg('cp',self.dbid_cp_ville)
        return self._cp
    @cp.setter
    def cp(self,cp):
        cp=int(cp)
        dbid=self._mere.cpvilles_tb.argToDbid('cp',cp)
        if dbid:
            self.dbid_cp_ville=dbid
            self._cp=cp
            self._ville=self._mere.cpvilles_tb.dbidToArg('ville',self.dbid_cp_ville)
    @property
    def ville(self):
        if not self._ville:self._ville=self._mere.cpvilles_tb.dbidToArg('ville',self.dbid_cp_ville)
        return self._ville
    @ville.setter
    def ville(self,ville):
        dbid=self._mere.cpvilles_tb.argToDbid('ville',ville)
        if dbid:
            self.dbid_cp_ville=dbid
            self._cp=self._mere.cpvilles_tb.dbidToArg('cp',self.dbid_cp_ville)
            self._ville=ville
    
    def sqlInsert(self,composentes=True):
        """S'insert lui même et ses composentes si pas de dbid"""
        if not self.dbid:self._sqlInsert()

    def sqlDelete(self,composentes=True):
        """Se deleta lui même et ses composentes si dbid"""
        if self.dbid:self._sqlDelete()
        
    def _selectDbidGeoloc(self,distance=0):
        """Select les adresses qui sont a une distance d et rend liste des dbid adresses"""
        return sql_select('adresses_tb', ['dbid','terre_dist_plus(latitude, longitude,%s,%s)AS distance'],
                          'terre_dist_plus(latitude, longitude,%s,%s)<%s ORDER BY distance',
                           [self.latitude,self.longitude,self.latitude,self.longitude,distance], self._verbose)        

class SqlDepotK(SqlObjetK):
    """Sous class sql du depot"""
    SQL_ARGS=['nom','surnom','volume','poid','prix_unite','remarque','nb_paquet','nb_carton','dbid_genre','dbid_contrat']#,'quantite' a supprimer
    INIT_SQL_ARGS= {'nom':'Sans nom',
                    'surnom':'Sans nom',
                    'volume':0,
                    'poid':0,
                    'prix_unite':0,
                    'quantite':0,
                    'remarque':'Sans remarque',
                    'nb_paquet':0,
                    'nb_carton':0,
                    'dbid_genre':1,
                    'dbid_contrat':None}
    SQL_TABLE='depots_tb'
    NAME_DICT_MERE='dictDepot'
    def __init__(self):
        SqlObjetK.__init__(self)
        self._genre=None
        
    @property
    def genre(self):
        if not self._genre:
            self._genre=self._mere.genresdepots_tb.dbidToArg('genre',self.dbid_genre)  
        return self._genre
    @genre.setter
    def genre(self,genre):
        dbid=self._mere.genresdepots_tb.argToDbid('genre',genre)
        self.dbid_genre=dbid
        self._genre=genre
        return sql_select('contrats_tb', ['dbid'],'dbid_client = %s', [self.dbid], self._verbose)        

    def _selectDbidLieuQuantite(self):
        """Select les lieux et la quantitee dans les lieux"""
        return sql_select('depots_lieux_tb',['dbid_lieu','quantite'],'dbid_depot = %s',[self.dbid],self._verbose) 
     
    def _upLieuQuantite(self,dbid_lieu,quantite):
        """update la quantite du depot"""
        if self._updatable:
            if sql_update('depots_lieux_tb', {'quantite':quantite},'dbid_lieu = {} AND dbid_depot = {}'.format(dbid_lieu,self.dbid), True):
                return True
            else:return False
 
    def _insLieuQuantite(self,dbid_lieu,quantite):
        """insert quantite du depot pour ce lieux"""
        if self._updatable:
            if self.dbid:
                if sql_insert('depots_lieux_tb',{'dbid_depot':self.dbid,'dbid_lieu':dbid_lieu,'quantite':quantite},False, True):return True
        return False
 
    def _delLieu(self,dbid_lieu):
        """del quantite du depot pour ce lieux"""
        if self._updatable:
            if sql_delete('depots_lieux_tb', 'dbid_lieu = {} AND dbid_depot = {}'.format(dbid_lieu,self.dbid), True):return True
        return False
    
    def sqlInsert(self,composentes=True):
        """S'insert lui même et ses composentes si pas de dbid"""
        if not self.dbid:self._sqlInsert()
        if composentes:
            for lieu, quantite in self.dictLieuQuantite.items():
                if lieu.dbid:self._insLieuQuantite(lieu.dbid,quantite)
            
            
            
            
