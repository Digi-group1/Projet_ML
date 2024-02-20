#################################
##### IMPORT DES LIBRAIRIES #####
#################################

import streamlit as st

####################################
##### PARTIE CHAMPS NON NOMMES ##### 
####################################

#############
# RECHERCHE #
#############

## Fonction qui recherche si notre BDD comporte des champs non nommés (donc contiennent "Unnamed")
def colonnes_unnamed(data) :
    colonnes_non_nommees = [colonne for colonne in data.columns if colonne.startswith("Unnamed")]
    return colonnes_non_nommees

###########
# MESSAGE #
###########

## Fonction qui affiche un message différent si notre BDD comporte des champs non nommés ou non
def affichage_unnamed(colonnes) :
    nombre = len(colonnes)
    if nombre == 0 :
        message = 'Votre jeu de données ne comporte pas de variables sans nom. Toutes vos variables comportent une dénomination'
    elif nombre <= 1 :
        message = 'Votre jeu de données comporte ' + str(nombre) + ' variable sans nom'
    else : 
        message = 'Votre jeu de données comporte ' + str(nombre) + ' variables sans nom'
    return message 
