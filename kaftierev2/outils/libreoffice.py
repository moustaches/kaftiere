import uno
from collections import defaultdict



def UnoClient(port=None):
    # get the uno component context from the PyUNO runtime
    # libreoffice "--accept=socket,host=localhost,port=2002;urp;" --invisible

    localContext = uno.getComponentContext()

    # create the UnoUrlResolver
    resolver = localContext.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", localContext)

    # connect to the running office
    ctx = resolver.resolve("uno:socket,host=localhost,port=" + str(port) + ";urp;StarOffice.ComponentContext")
    smgr = ctx.ServiceManager

    # get the central desktop object
    DESKTOP =smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    #url = unohelper.systemPathToFileUrl(os.path.abspath(filename))
    Fichier = "private:factory/scalc"
    doc = DESKTOP.loadComponentFromURL(Fichier, '_blank', 0, ()) 

    return doc

def colonneFeuilleREF(sheet =None,index=(None, None), tournee=None):
    dict_depot_index={}
    ind_list_client=[]
    ind_client=0

    for client in tournee.listClient:
        ind_list_client.append(ind_client+2)
        sheet.getCellByPosition(index[0]-1,index[1]+ind_client+2).setString(client.surnom)#edition des clients
        i_contrat=0
        for contrat in client.listContratDepuisTournee(tournee):
            for depot in contrat.listDepot:
                ind_depot=ind_client+i_contrat+2
                sheet.getCellByPosition(index[0],index[1]+ind_depot).setString(depot.surnom)#edition des depots
                dict_depot_index[ind_depot]=depot
                i_contrat+=1    
        ind_client+=i_contrat  
                
    ind_pedaleur=0
    for pedaleur in tournee.listPedaleur:
        ind_parcours=0
        dict_depot_pedaleur=defaultdict(int)
        for parcours in pedaleur.listParcoursDepuisTournee(tournee):
            sheet.getCellByPosition(index[0]+ind_pedaleur+ind_parcours+3,index[1]+1).setString(parcours.dbid)#edition des parcours
            ind_parcours+=1
            for ind_depot, depot in dict_depot_index.items():
                nb_depot=parcours.quantiteDepot(depot)
                dict_depot_pedaleur[ind_depot]+=nb_depot
                sheet.getCellByPosition(index[0]+ind_pedaleur+ind_parcours+2,index[1]+ind_depot).setValue(nb_depot)#edition des nb depot/parcours
        for ind_depot, depot in dict_depot_index.items():
            if depot.infoQuantiteDepot:
                pour_cent_depot_pedaleur=dict_depot_pedaleur[ind_depot]/depot.infoQuantiteDepot
                sheet.getCellByPosition(index[0]+ind_pedaleur+1,index[1]+ind_depot).setValue(pour_cent_depot_pedaleur)#edition des % depot/pedaleur
                sheet.getCellByPosition(index[0]+ind_pedaleur+1,index[1]+ind_depot).setPropertyValue( "NumberFormat", 10 )#style des % depot/pedaleur
                sheet.getCellByPosition(index[0]+ind_pedaleur+2,index[1]+ind_depot).setValue(dict_depot_pedaleur[ind_depot])#edition des totales depot/pedaleur
        sheet.getCellByPosition(index[0]+ind_pedaleur+1,index[1]).setString(pedaleur.surnom)#edition des pedaleurs
        sheet.getCellByPosition(index[0]+ind_pedaleur+1,index[1]).ParaAdjust=uno.Enum('com.sun.star.style.ParagraphAdjust','CENTER')#style pedaleurs
        sheet.getCellByPosition(index[0]+ind_pedaleur+1,index[1]).CharWeight=uno.getConstantByName('com.sun.star.awt.FontWeight.BOLD')   
        sheet.getCellRangeByPosition(index[0]+ind_pedaleur+1,index[1], index[0]+ind_pedaleur+ind_parcours+2,index[1]).merge(True)  
        ind_pedaleur+=(ind_parcours+2)
        
    for ind_client in ind_list_client:
        sheet.getCellRangeByPosition(index[0],ind_client+index[1], index[0]+ind_pedaleur,ind_client+index[1]).CellBackColor= 190190190 #couleur ligne client
    

def styleFeuilleREF(sheet =None,index=(None, None), tournee=None):
    dict_depot_index={}
    ind_client=0
    ind_list_client=[]
    
    sheet.CharFontName = "Arial"
    sheet.CharHeight = 10
    sheet.ParaAdjust=uno.Enum('com.sun.star.style.ParagraphAdjust', 'LEFT')#uno.Enum('com.sun.star.style.ParagraphAdjust.LEFT')
    
    for client in tournee.listClient:
        ind_list_client.append(ind_client+2)
        sheet.getCellByPosition(index[0]-1,index[1]+ind_client+2).ParaAdjust=uno.Enum('com.sun.star.style.ParagraphAdjust','LEFT')#style des clients
        sheet.getCellByPosition(index[0]-1,index[1]+ind_client+2).CharWeight=uno.getConstantByName('com.sun.star.awt.FontWeight.BOLD')
        i_contrat=0
        for contrat in client.listContratDepuisTournee(tournee):
            for depot in contrat.listDepot:
                ind_depot=ind_client+i_contrat+2
                sheet.getCellByPosition(index[0],index[1]+ind_depot).ParaAdjust=uno.Enum('com.sun.star.style.ParagraphAdjust','RIGHT')#style des depots
                sheet.getCellByPosition(index[0],index[1]+ind_depot).CharPosture=uno.Enum('com.sun.star.awt.FontSlant','ITALIC')
                dict_depot_index[ind_depot]=depot
                i_contrat+=1
            sheet.getCellRangeByPosition(index[0]-1, index[1]+ind_client+2,index[0]-1, index[1]+ind_client+2+i_contrat).merge(True)
        ind_client+=i_contrat    

                
    ind_pedaleur=0
    for pedaleur in tournee.listPedaleur:
        sheet.getCellByPosition(index[0]+ind_pedaleur+1,index[1]).setString(pedaleur.surnom)#edition des pedaleurs
        sheet.getCellRangeByPosition(index[0],index[1]+ind_client+2).ParaAdjust=uno.Enum('com.sun.star.style.ParagraphAdjust','RIGHT')
        sheet.getCellRangeByPosition(index[0],index[1]+ind_client+2).CharWeight=uno.getConstantByName('com.sun.star.awt.FontWeight.BOLD')
        ind_parcours=0
        dict_depot_pedaleur=defaultdict(int)
#         for parcours in pedaleur.listParcoursDepuisTournee(tournee):
#             sheet.getCellByPosition(index[0]+ind_pedaleur+ind_parcours+2,index[1]+1).setString(parcours.dbid)#edition des parcours
#             ind_parcours+=1
#             for ind_depot, depot in dict_depot_index.items():
#                 nb_depot=parcours.quantiteDepot(depot)
#                 dict_depot_pedaleur[ind_depot]+=nb_depot
#                 sheet.getCellByPosition(index[0]+ind_pedaleur+ind_parcours+1,index[1]+ind_depot).setValue(nb_depot)#edition des nb depot/parcours
#         for ind_depot, depot in dict_depot_index.items():
#             pour_cent_depot_pedaleur=dict_depot_pedaleur[ind_depot]/depot.infoQuantiteDepot
#             sheet.getCellByPosition(index[0]+ind_pedaleur+1,index[1]+ind_depot).setValue(pour_cent_depot_pedaleur)#edition des % depot/pedaleur
#         ind_pedaleur+=(ind_parcours+1)

def ligneFeuilleDeRoute(sheet =None,index=None,num=None, lieu=None, info_depot=None):
    sheet.getCellByPosition(0,index*2).setValue(num)
    sheet.getCellByPosition(1,index*2).setString(lieu.nom)
    sheet.getCellByPosition(2,index*2).setString(lieu.adresse.adresse)
    sheet.getCellByPosition(3,index*2).setString(lieu.adresse.cp)
    sheet.getCellByPosition(4,index*2).setString(lieu.adresse.ville)
    sheet.getCellByPosition(0,index*2+1).setString(info_depot)

def ligneFeuilleTamponnade(sheet =None,index=None, num=None, lieu=None,  info_depot=None):
    sheet.getCellByPosition(0,index*2).setValue(num)
    sheet.getCellByPosition(1,index*2).setString(lieu.nom)
    sheet.getCellByPosition(2,index*2).setString(lieu.adresse.adresse)
    sheet.getCellByPosition(4,index*2).setString(lieu.adresse.cp)
    sheet.getCellByPosition(5,index*2).setString(lieu.adresse.ville)
    sheet.getCellByPosition(6,index*2).setString(" ")
    sheet.getCellByPosition(0,index*2+1).setString(info_depot)

def styleFeuilleDeRoute(sheet=None, card=None):
    sheet.getCellByPosition(0, 0).getColumns().Width = 600
    sheet.getCellByPosition(1, 0).getColumns().Width = 6000
    sheet.getCellByPosition(2, 0).getColumns().Width = 6000
    sheet.getCellByPosition(3, 0).getColumns().Width = 1250
    sheet.getCellByPosition(4, 0).getColumns().Width =2500
    sel=sheet.getCellRangeByPosition(0, 0, 4, card*2)
    sel.CharFontName = "Arial"
    sel.CharHeight = 10
    sheet.getCellRangeByPosition(0, 0, 2, card*2).ParaAdjust=uno.Enum('com.sun.star.style.ParagraphAdjust','BLOCK')
    sheet.getCellRangeByPosition(4, 0, 4, card*2).ParaAdjust=uno.Enum('com.sun.star.style.ParagraphAdjust','BLOCK')
    sheet.getCellRangeByPosition(3, 0, 3, card*2).ParaAdjust=uno.Enum('com.sun.star.style.ParagraphAdjust','CENTER')
    sheet.getCellRangeByPosition(2, 0, 2, card*2).CharPosture=uno.Enum('com.sun.star.awt.FontSlant','ITALIC')
    sheet.getCellRangeByPosition(3, 0, 4,card*2).CharWeight=uno.getConstantByName('com.sun.star.awt.FontWeight.BOLD')
    i=0
    while i<card:
        sheet.getCellRangeByPosition(0, 2*i, 0, 2*i).CharWeight=uno.getConstantByName('com.sun.star.awt.FontWeight.BOLD')
        sheet.getCellRangeByPosition(0, 2*i+1,3, 2*i+1).merge(True)
        sheet.getCellRangeByPosition(0, 2*i+1,3, 2*i+1).CharHeight = 8
        i+=1
    sel = sheet.getCellRangeByPosition(0, 0, 4,card*2-1)
    Border = sel.TopBorder
    Border.OuterLineWidth = 2
    sel.TopBorder = Border
    sel.BottomBorder = Border
    sel.LeftBorder = Border
    sel.RightBorder = Border

def styleFeuilleTamponnade(sheet=None, card=None):
    sheet.getCellByPosition(0, 0).getColumns().Width = 700
    sheet.getCellByPosition(1, 0).getColumns().Width = 4000
    sheet.getCellByPosition(2, 0).getColumns().Width = 2000
    sheet.getCellByPosition(3, 0).getColumns().Width = 2000
    sheet.getCellByPosition(4, 0).getColumns().Width =1250
    sheet.getCellByPosition(5, 0).getColumns().Width =2000
    sheet.getCellByPosition(6, 0).getColumns().Width =5000
    sel=sheet.getCellRangeByPosition(0, 0, 4, card*2)
    sel.CharFontName = "Arial"
    sel.CharHeight = 10
    sheet.getCellRangeByPosition(0, 0, 5, card*2).ParaAdjust=uno.Enum('com.sun.star.style.ParagraphAdjust','BLOCK')
    sheet.getCellRangeByPosition(4, 0, 4, card*2).ParaAdjust=uno.Enum('com.sun.star.style.ParagraphAdjust','CENTER')
    sheet.getCellRangeByPosition(2, 0, 2, card*2).CharPosture=uno.Enum('com.sun.star.awt.FontSlant','ITALIC')
    sheet.getCellRangeByPosition(4, 0, 4, card*2).CharWeight=uno.getConstantByName('com.sun.star.awt.FontWeight.BOLD')
    i=0
    while i<card:
        sheet.getCellRangeByPosition(0, 2*i, 0, 2*i+1).getRows().Height =1200
        sheet.getCellRangeByPosition(0, 2*i, 0, 2*i).CharWeight=uno.getConstantByName('com.sun.star.awt.FontWeight.BOLD')
        sheet.getCellRangeByPosition(6, 2*i, 6, 1+2*i).merge(True)
        sheet.getCellRangeByPosition(2, 2*i, 3, 2*i).merge(True)  
        sheet.getCellRangeByPosition(0, 1+2*i, 2, 1+2*i).merge(True) 
        sheet.getCellRangeByPosition(3, 1+2*i, 5, 1+2*i).merge(True)
        sheet.getCellRangeByPosition(0, 2*i+1, 3, 2*i+1).CharHeight = 8
        i+=1
    sel = sheet.getCellRangeByPosition(0, 0, 6, card*2-1)
    Border = sel.TopBorder
    Border.OuterLineWidth = 2
    sel.TopBorder = Border
    sel.BottomBorder = Border
    sel.LeftBorder = Border
    sel.RightBorder = Border

def editerFeuilleDeRoute(sheet =None,parcours=None):
    list_lieu_ordonne= parcours.listLieuOrdonne[0]
    if list_lieu_ordonne:
        styleFeuilleDeRoute(sheet=sheet,card=len(list_lieu_ordonne))
        j=0
        for (card, lieu) in list_lieu_ordonne:
            info=""
            dict_depot_tournee=lieu.dictDepotTournee(tournee=parcours.tournee)
            for contrat, dict_depots in dict_depot_tournee.items():
                info+="  |{} ".format(contrat.client.surnom)
                for depot, quantite in dict_depots.items(): info+=" {}{}  ".format(quantite,depot.surnom)          
            ligneFeuilleDeRoute(sheet =sheet,index=j, num=card, lieu=lieu, info_depot=info[3:])
            j+=1

def editerFeuilleTamponnade(sheet =None,parcours=None,contrat=None):
    list_lieu_ordonne= parcours.listLieuOrdonne[0]
    if list_lieu_ordonne:
        list_lieu=[]
        for (card, lieu) in list_lieu_ordonne:
            if lieu in contrat.listLieu:
                info=""
                for depot in contrat.listDepot:
                    if lieu in depot.listLieu:
                        info+=" {} {}   ".format(depot.quantiteLieu(lieu),depot.nom)                         
                list_lieu.append((card, lieu, info))
        styleFeuilleTamponnade(sheet =sheet,card=len(list_lieu))
        j=0
        for card, lieu, info in list_lieu:
            ligneFeuilleTamponnade(sheet =sheet,index=j, num=card, lieu=lieu, info_depot=info)  
            j+=1
    
def editerTamponnade(tournee=None, calc=None):

    sheet = calc.getSheets().getByIndex(0)
    colonneFeuilleREF(sheet =sheet,index=(1, 0), tournee=tournee)
    i=0
    for parcours in tournee.listParcours:
        i+=1
        calc.getSheets().insertNewByName("P{} - {}".format(parcours.dbid, parcours.pedaleur.surnom),i)
        sheet = calc.getSheets().getByIndex(i)
        editerFeuilleDeRoute(sheet =sheet,parcours=parcours)
        for contrat in tournee.listContrat:
            i+=1
            calc.getSheets().insertNewByName("P{} - {}-{}".format(parcours.dbid, contrat.client.nom, contrat.dbid),i)
            sheet =calc.getSheets().getByIndex(i)
            editerFeuilleTamponnade(sheet =sheet,parcours=parcours, contrat=contrat)
           

        
def acction(tournee=None):
    calc = UnoClient(port=2002) #cree un nouveau classeur
    editerTamponnade(tournee=tournee, calc=calc)
    
#    dd=calc.getScriptProvider().getScript("vnd.sun.star.script:testfdr.py$editerTamponnade?language=Python&location=user")
#    dd.invoke((([[[], ['r', 'f']], ['g']],), ), None,None )









