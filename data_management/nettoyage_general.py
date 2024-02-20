#########################
##### PARTIE IMPORT #####
#########################

#########################
# IMPORT DES LIBRAIRIES #
#########################

import streamlit as st



###########################
##### PARTIE GENERALE ##### 
###########################

###############
# SUPPRESSION #
###############

## Fonction qui supprime des colonnes 
def supp_colonnes(data,colonnes) : 
    data = data.drop(columns=colonnes,axis=1)
    return data

#############
# RENOMMAGE #
#############

## Fonction qui renomme des colonnes
def renommer_colonnes(data,colonne,nouveau_nom) :
    if nouveau_nom != "" :
        data = data.rename(columns={colonne: nouveau_nom}, inplace=True)
    return data

#########
# SPLIT #
#########

## Fonction qui splite la BDD en colonnes numériques VS colonnes catégorielles
def split_data_type(data) :
    colonnes_numeriques = data.select_dtypes(include=['float', 'int']).columns
    colonnes_categorielles = data.select_dtypes(include=['object']).columns
    return colonnes_numeriques,colonnes_categorielles