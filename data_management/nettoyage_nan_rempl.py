#########################
##### PARTIE IMPORT #####
#########################

#########################
# IMPORT DES LIBRAIRIES #
#########################

import streamlit as st

##############################
# IMPORT DES FICHIERS PYTHON #
##############################

from data_management import nettoyage_general as general



#################################################
##### PARTIE VALEURS NULLES -- REMPLACEMENT ##### 
#################################################

##############
# NUMERIQUES #
##############

## Fonction qui remplace les valeurs manquantes - numériques - par la moyenne
def remplace_valeur_num_moyenne(data,colonne) :
    moyenne = data[colonne].mean()
    data = data[colonne].fillna(moyenne, inplace=True)
    return data

## Fonction qui remplace les valeurs manquantes - numériques - par la médiane
def remplace_valeur_num_mediane(data,colonne) :
    moyenne = data[colonne].median()
    data = data[colonne].fillna(moyenne, inplace=True)
    return data

#################
# CATEGORIELLES #
#################

## Fonction qui remplace les valeurs manquantes - catégorielles
def remplace_valeur_cat_freq(data,colonne) :
    valeur_frequente = data[colonne].mode()[0]
    data = data[colonne].fillna(valeur_frequente, inplace=True)
    
###########
# MESSAGE #
###########

## Fonction qui affiche la méthode de remplacement des valeurs manquantes automatique
def remplace_auto_mess() :
    st.write("Pour remplacer les données nulles, nous appliquons deux méthodes : ")
    st.write(" - Colonnes numériques : on remplace la valeur null par la moyenne de la colonne")
    st.write(" - Colonnes catégorielles : on remplace la valeur null par la valeur de la colonne la plus fréquente")

################
# REMPLACEMENT #
################
        
## Fonction qui remplace les valeurs manquantes (quelque soit le type)
def remplacer_valeurs_manquantes(data):
    colonnes_numeriques,colonnes_categorielles = general.split_data_type(data)
    # On affiche le message de remplacement automatique
    remplace_auto_mess()
    
    # Remplacer les valeurs manquantes dans les colonnes numériques par la moyenne
    for colonne in colonnes_numeriques:
        moyenne = data[colonne].mean()
        data[colonne].fillna(moyenne, inplace=True)
    
    # Remplacer les valeurs manquantes dans les colonnes catégorielles par la valeur la plus fréquente
    for colonne in colonnes_categorielles:
        valeur_frequente = data[colonne].mode()[0]
        data[colonne].fillna(valeur_frequente, inplace=True)

    return data