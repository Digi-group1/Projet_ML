def colonnes_unnamed(data) :
    colonnes_non_nommees = [colonne for colonne in data.columns if colonne.startswith("Unnamed")]
    return colonnes_non_nommees

def affichage_unnamed(colonnes) :
    nombre = len(colonnes)
    if nombre == 0 :
        message = 'Votre jeu de données ne comporte pas de variables sans nom. Toutes vos variables comportent une dénomination'
    elif nombre <= 1 :
        message = 'Votre jeu de données comporte ' + str(nombre) + ' variable sans nom'
    else : 
        message = 'Votre jeu de données comporte ' + str(nombre) + ' variables sans nom'
    return message 

def supp_colonnes(data,colonnes) : 
    data = data.drop(columns=colonnes,axis=1)
    return data

def renommer_colonnes(data,colonne,nouveau_nom) :
    if nouveau_nom != "" :
        data.rename(columns={colonne: nouveau_nom}, inplace=True)
    return data

def identification_nan(data) : 
    valeurs = data.isna().sum()
    if valeurs.sum() == 0 :
        message = 'Votre base de données ne contient pas de valeurs manquantes'
    else :
        message = 'Votre base de données contient des valeurs manquantes'
    return message
        
        


