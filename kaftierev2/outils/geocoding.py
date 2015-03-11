'''
Created on 9 janv. 2015

@author: moustache
'''
from geopy.geocoders import Nominatim 

#from outils.googlesuggest import GoogleSuggest as GS
# suggestions = GS("7 rue de telmcen 75020 Paris").read()
# for suggest in suggestions:
#     print(suggest)



def get_geocodeur():
    """Connection au geocodeur unique"""
    global GEOCODEUR
    if not GEOCODEUR:
        GEOCODEUR = connectionGeocodeur("Nominatim")
    return GEOCODEUR

def connectionGeocodeur(nom_geocodeur):
    global GEOCODEUR   
    if nom_geocodeur=="Nominatim": GEOCODEUR = Nominatim(view_box=(2.1665,48.9629,2.6170,48.7796))
    return True

def formatageAdresseNomiatim(adresse):
    '''
     prend une adresse et rend un sting bien ordornée pour geocogage avec nominatim:
    addresse:-> string
    '''
    num=0
    adresse.adresse=adresse.adresse.replace(',', ' ')
    for j,caractere in enumerate(adresse.adresse):
        if caractere.isnumeric():num=j
        if adresse.adresse[j:j+5] in ("bis ","BIS ","ter ","TER ","Bis ","Ter "):num=j+4
    if num != 0:str_adresse="France, {}, {}, {}, {}".format(adresse.cp,adresse.ville,adresse.adresse[num+1:],adresse.adresse[:num+1])
    else : str_adresse="France, {}, {}, {}".format(adresse.cp,adresse.ville,adresse.adresse)     
    return str_adresse

def geocoder(adresse):
    '''
    prend une adresse la geocode et rend les resultats:
    lieux:-> list_resultat [(dict_resultat)
                {'type':'Geocodage',
                'i':i,
                'adresse':adresse,
                'longitude':longitude,
                'latitude':latitude,
                'cp':cp,
                'ville':ville,
                'nom':nom})
	'''

    list_resultat,i=[],1
    list_geolocalisation=get_geocodeur().geocode(formatageAdresseNomiatim(adresse),exactly_one=False, timeout=60, addressdetails=True, language="fr")
    print(formatageAdresseNomiatim(adresse))
    print(list_geolocalisation)
    if list_geolocalisation:
        for i,geolocalisation in enumerate(list_geolocalisation):
            dict_resultat={'type':'Geocodage',
                            'i':i,
                            'adresse':"Sans adresse",
                            'longitude':0,
                            'latitude':0,
                            'cp':75000,
                            'ville':"Sans ville",
                            'nom':"Sans nom"}
            if "address" in geolocalisation.raw:
                address_geoloc=""
                if 'house_number' in geolocalisation.raw["address"]:address_geoloc+=geolocalisation.raw["address"]['house_number']+' '
                if 'road' in geolocalisation.raw["address"]:address_geoloc+=format(geolocalisation.raw["address"]['road'])  
                ville_geoloc=""   
                if 'town' in geolocalisation.raw["address"]:ville_geoloc=geolocalisation.raw["address"]['town']
                if 'city' in geolocalisation.raw["address"]:ville_geoloc=geolocalisation.raw["address"]['city'] 
                cp_geoloc=75000  
                if 'postcode' in geolocalisation.raw["address"]:
                    if ';' in geolocalisation.raw["address"]['postcode']: cp_geoloc=geolocalisation.raw["address"]['postcode'].split(';')[0]
                    else: cp_geoloc=geolocalisation.raw["address"]['postcode'] 
            dict_resultat['adresse']=address_geoloc
            dict_resultat['longitude']=float(geolocalisation.raw['lon'])
            dict_resultat['latitude']=float(geolocalisation.raw['lat'])
            dict_resultat['cp']=int(cp_geoloc)
            dict_resultat['ville']=ville_geoloc
            list_resultat.append(dict_resultat)
    return list_resultat
                

        