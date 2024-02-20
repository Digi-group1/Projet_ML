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
from data_management import nettoyage_nan_info as nan_info
from data_management import nettoyage_nan_supp as nan_supp
from data_management import nettoyage_nan_rempl as nan_rempl




###############################################
##### PARTIE VALEURS NULLES -- TRAITEMENT ##### 
###############################################

##################
# MENU PRINCIPAL #
##################

## Fonction qui affiche le menu principal de traitement
def menu_traitement_principal() :
    st.write('Que souhaitez-vous faire ?')
    supprimer_lignes = st.checkbox("Supprimer toutes les lignes contenant des valeurs null ?")
    traitement_commun = st.checkbox("Traiter toutes les colonnes de la même façon")
    traitement_individuel = st.checkbox("Traiter individuellement les colonnes")
    return supprimer_lignes, traitement_commun, traitement_individuel

##########################
# MENU TRAITEMENT COMMUN #
##########################

## Fonction qui affiche le menu pour le traitement commun 
def menu_trait_commun() :
    choix_commun = st.radio("Quelle action souhaitez-vous effectuer ?", ("Supprimer les colonnes", "Remplacer les valeurs manquantes"))
    return choix_commun

##############################
# MENU TRAITEMENT INDIVIDUEL #
##############################

## Fonction qui affiche le menu pour le traitement individuel 
def menu_trait_indiv() :
    st.write('Que souhaitez-vous faire ?')
    supprimer_col_multi = st.checkbox("Supprimer une ou plusieurs colonnes ?")
    remplacer_moy_multi = st.checkbox("Remplacer les valeurs nulles d'une ou plusieurs colonnes par la moyenne (valeurs numériques) ?")
    remplacer_med_multi = st.checkbox("Remplacer les valeurs nulles d'une ou plusieurs colonnes par la médiane (valeurs numériques) ?")
    remplacer_freq_multi = st.checkbox("Remplacer les valeurs nulles d'une ou plusieurs colonnes par la valeur la plus fréquente (valeurs catégorielles) ?")
    return supprimer_col_multi, remplacer_moy_multi, remplacer_med_multi, remplacer_freq_multi

################################
# MENU REMPLACEMENT INDIVIDUEL #
################################

def menu_rempl_indiv_num() :
    choix_remplace = st.radio("Par quelle valeur souhaitez-vous remplacer ?",("Une valeur unique","La moyenne de la colonne","La médiane de la colonne"))
    return choix_remplace

def menu_rempl_indiv_cat() :
    choix_remplace = st.radio("Par quelle valeur souhaitez-vous remplacer ?",("Une valeur unique","La valeur de la colonne la plus fréquente"))
    return choix_remplace
    
#####################################
# TRAITEMENT DES VALEURS MANQUANTES #
#####################################

## Fonction qui effectue le traitement des valeurs nulles selon le choix de l'utilisateur
def choix_traitement_nan(data) :
    # On splite la BDD entre colonnes numériques VS colonnes catégorielles
    colonnes_numeriques,colonnes_categorielles = general.split_data_type(data)
    valeurs, valeurs_nan, colonnes_avec_nan = nan_info.infos_valeurs_nan(data)
    # On affiche le menu principal :
    supprimer_lignes, traitement_commun, traitement_individuel = menu_traitement_principal()
    
    # Si le choix est de supprimer toutes les lignes d'un coup :   
    if supprimer_lignes :
        data = nan_supp.suppression_ligne_null(data)
        
    # Si le choix est de traiter toutes les colonnes de la même façon :
    if traitement_commun :
        # On affiche le menu : 
        choix_commun = menu_trait_commun()
        # Si choix de suppression des colonnes, on supprime les colonnes
        if choix_commun == "Supprimer les colonnes" :
            data = general.supp_colonnes(data,colonnes_avec_nan) 
        # Si choix de remplacer les valeurs manquantes, on remplace les valeurs manquantes
        if choix_commun == "Remplacer les valeurs manquantes" : 
            data = nan_rempl.remplacer_valeurs_manquantes(data)
    
    # Si le choix est de traiter individuellement les colonnes : 
    if traitement_individuel :
        # On propose plusieurs traitements possibles
        supprimer_col_multi, remplacer_moy_multi, remplacer_med_multi, remplacer_freq_multi = menu_trait_indiv()
        # On récupère la liste des colonnes à modifier 
        valeurs, valeurs_nan, colonnes_avec_nan = nan_info.infos_valeurs_nan(data)       
        # Si la case de suppression de colonnes est cochée
        if supprimer_col_multi :
            # On donne le choix à l'utilisateur de sélectionner les colonnes à supprimer
            col_sel_supp = st.multiselect("Sélectionnez une ou plusieurs colonnes à supprimer", colonnes_avec_nan)
            colonnes_supp = []
            for colonne in col_sel_supp :
                colonnes_supp.append(colonne)
            # On fait la suppression des colonnes sélectionnées
            data = general.supp_colonnes(data,colonnes_supp)
        # Si la case de remplacer des valeurs nulles par la moyenne est cochée    
        if remplacer_moy_multi :
            valeurs, valeurs_nan, colonnes_avec_nan = nan_info.infos_valeurs_nan(data)
            col_sel_moy = st.multiselect("Sélectionnez une ou plusieurs colonnes où on applique la moyenne", colonnes_avec_nan)
            for colonne in col_sel_moy :
                if colonne in colonnes_numeriques : 
                    moyenne = data[colonne].mean()
                    data[colonne].fillna(moyenne, inplace=True)
                else : 
                    st.write("La colonne " + colonne + " n'est pas numérique. Si ce n'est pas le cas, recharger un fichier pré-nettoyé (colonnes au bon format).")
        # Si la case de remplacer des valeurs nulles par la médiane est cochées
        if remplacer_med_multi :
            valeurs, valeurs_nan, colonnes_avec_nan = nan_info.infos_valeurs_nan(data)
            col_sel_med = st.multiselect("Sélectionnez une ou plusieurs colonnes où on applique la médiane", colonnes_avec_nan)
            for colonne in col_sel_med :
                if colonne in colonnes_categorielles : 
                    mediane = data[colonne].mean()
                    data[colonne].fillna(mediane, inplace=True)
                else : 
                    st.write("La colonne " + colonne + " n'est pas numérique. Si ce n'est pas le cas, recharger un fichier pré-nettoyé (colonnes au bon format).")
        # Si la case de remplacer des valeurs nulles par la valeur la plus fréquente est cochée
        if remplacer_freq_multi : 
            valeurs, valeurs_nan, colonnes_avec_nan = nan_info.infos_valeurs_nan(data)
            col_sel_freq = st.multiselect("Sélectionnez une ou plusieurs colonnes où on applique la valeur la plus fréquente", colonnes_avec_nan)
            for colonne in col_sel_freq :
                if colonne in colonnes_categorielles : 
                    valeur_frequente = data[colonne].mode()[0]
                    data[colonne].fillna(valeur_frequente, inplace=True)
                else : 
                    st.write("La colonne " + colonne + " n'est pas catégorielle. Si ce n'est pas le cas, recharger un fichier pré-nettoyé (colonnes au bon format).")
    
    st.write("Voici votre nouvelle base de données :")
    st.write(data.head())
    st.write("Vérification des valeurs manquantes :")
    message_valeurs, valeurs_null = nan_info.identification_nan(data)
    st.write(message_valeurs)
    
    return data
            
            
        




    

        


