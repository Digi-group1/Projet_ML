#########################
##### PARTIE IMPORT #####
#########################

#########################
# IMPORT DES LIBRAIRIES #
#########################

import streamlit as st



##########################################
##### PARTIE VALEURS NULLES -- INFOS ##### 
##########################################

################
# INFORMATIONS #
################

## Fonction qui renvoie des infos sur les valeurs nulles
def infos_valeurs_nan(data) :
    valeurs = data.isna().sum()
    valeurs_nan = valeurs[valeurs >0]
    colonnes_avec_nan = valeurs_nan.index.tolist()
    return valeurs, valeurs_nan, colonnes_avec_nan

###########
# MESSAGE #
###########

## Fonction qui affiche un message si notre BDD comporte des valeurs nulles ou non
def identification_nan(data) : 
    valeurs, valeurs_nan, colonnes_avec_nan = infos_valeurs_nan(data)
    if valeurs.sum() == 0 :
        message = 'Votre base de données ne contient pas de valeurs manquantes'
        valeurs_null = "Non"
    else :
        message = 'Votre base de données contient des valeurs manquantes'
        st.write(valeurs_nan)
        valeurs_null = "Oui"
    return message, valeurs_null