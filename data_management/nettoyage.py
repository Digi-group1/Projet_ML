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
    
################
# REMPLACEMENT #
################
        
## Fonction qui remplace les valeurs manquantes (quelque soit le type)
def remplacer_valeurs_manquantes(data):
    colonnes_numeriques = data.select_dtypes(include=['float', 'int']).columns
    colonnes_catégorielles = data.select_dtypes(include=['object']).columns
    st.write("Pour remplacer les données nulles, nous appliquons deux méthodes : ")
    st.write(" - Colonnes numériques : on remplace la valeur null par la moyenne de la colonne")
    st.write(" - Colonnes catégorielles : on remplace la valeur null par la valeur de la colonne la plus fréquente")
    
    # Remplacer les valeurs manquantes dans les colonnes numériques par la moyenne
    for colonne in colonnes_numeriques:
        moyenne = data[colonne].mean()
        data[colonne].fillna(moyenne, inplace=True)
    
    # Remplacer les valeurs manquantes dans les colonnes catégorielles par la valeur la plus fréquente
    for colonne in colonnes_catégorielles:
        valeur_frequente = data[colonne].mode()[0]
        data[colonne].fillna(valeur_frequente, inplace=True)

    return data

###########
# MESSAGE #
###########

## Fonction qui affiche la méthode de remplacement des valeurs manquantes automatique
def remplace_auto_mess() :
    st.write("Pour remplacer les données nulles, nous appliquons deux méthodes : ")
    st.write(" - Colonnes numériques : on remplace la valeur null par la moyenne de la colonne")
    st.write(" - Colonnes catégorielles : on remplace la valeur null par la valeur de la colonne la plus fréquente")



####################################################################
##### PARTIE VALEURS NULLES -- SUPPRESSION DES LIGNES ENTIERES ##### 
####################################################################

#####################
# SUPPRESSION LIGNE #
#####################

def suppression_ligne_null(data) :
    # On affiche un message d'alerte
    st.write("<span style='color:red'>!! Attention, cette action peut fortement réduire le nombre d'enregistrements de votre base de données !! </span>", unsafe_allow_html=True)
    # On compte le nombre d'enregistrements avant suppression, et on affiche le message
    nb_enreg = data.shape[0]
    st.write("Votre base de données contient actuellement " + str(nb_enreg) + " enregistrements")
    # On compte le nombre d'enregistrement qu'il y aurait après suppression, et on affiche le message
    data_sans_nulles = data.dropna()
    nb_enreg_apres = data_sans_nulles.shape[0]
    nb_supp = nb_enreg - nb_enreg_apres
    st.write("Vous allez supprimer " + str(nb_supp) + " enregistrements")
    # On redemande l'utilisateur s'il est sûr de vouoloir supprimer toutes les lignes qui comportent des valeurs nulles
    verification_supp = st.radio("Souhaitez-vous vraiment supprimer tous les enregistrements ?", ("Oui", "Non"))
    # Si non : On revient au menu précédent
    if verification_supp == "Non" :
        st.write("Veuillez sélectionner un autre choix au menu du dessus")
    # Si oui : On applique la suppression
    elif verification_supp == "Oui" :
        data = data_sans_nulles
    return data




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
    #traitement_indiv = st.checkbox("Traiter les colonnes une par une") 
    return supprimer_lignes, traitement_commun #, traitement_indiv

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
def menu_trait_indiv(colonne) :
    choix_indiv = st.radio("Quelle action souhaitez-vous effectuer pour la colonne " + colonne + " ?", ("Supprimer la colonne", "Remplacer les valeurs manquantes"))
    return choix_indiv

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
    colonnes_numeriques,colonnes_categorielles = split_data_type(data)
    valeurs, valeurs_nan, colonnes_avec_nan = infos_valeurs_nan(data)
    # On affiche le menu principal :
    supprimer_lignes, traitement_commun = menu_traitement_principal()
    
    # Si le choix est de supprimer toutes les lignes d'un coup :   
    if supprimer_lignes :
        data = suppression_ligne_null(data)
        
    # Si le choix est de traiter toutes les colonnes de la même façon :
    if traitement_commun :
        # On affiche le menu : 
        choix_commun = menu_trait_commun()
        # Si choix de suppression des colonnes, on supprime les colonnes
        if choix_commun == "Supprimer les colonnes" :
            data = supp_colonnes(data,colonnes_avec_nan) 
        # Si choix de remplacer les valeurs manquantes, on remplace les valeurs manquantes
        if choix_commun == "Remplacer les valeurs manquantes" : 
            data = remplacer_valeurs_manquantes(data)
    #Si le choix est de traiter chaque colonne individuellement : 
    
    # if traitement_indiv :
    #     valeurs, valeurs_nan, colonnes_avec_nan = infos_valeurs_nan(data)
    #     for colonne in colonnes_avec_nan :
    #         for i in range(len(colonnes_avec_nan)) :
    #             # On affiche le menu
    #             choix_indiv = menu_trait_indiv(colonne)
    #             # Si on décide de supprimer la colonne, on le fait et on affiche un message
    #             if choix_indiv == "Supprimer la colonne" :
    #                 data = data.drop(columns=colonne,axis=1)
    #                 st.write("Vous venez de supprimer la colonne "+ colonne + ". Voici votre nouvelle base de données")
    #             # Si on décide de remplacer les valeurs manquantes : 
    #             if choix_indiv == "Remplacer les valeurs manquantes" :
    #                 # Si la colonne est numérique, on aura 3 choix : valeur unique, moyenne ou médiane
    #                 if colonne in colonnes_numeriques : 
    #                     choix_remplace = st.radio("Par quelle valeur souhaitez-vous remplacer ?",("Une valeur unique", "La moyenne de la colonne", "La médiane de la colonne"))
    #                     # Si on décide de remplacer par une valeur unique à saisir : 
    #                     if choix_remplace == "Une valeur unique" :
    #                         # On entre la valeur
    #                         valeur_remplace = st.text_input("Entrez ici la valeur de remplacement")
    #                         # On vérifie que c'est du numérique 
    #                         if int(valeur_remplace) :
    #                             valeur_remplace = int(valeur_remplace)
    #                             data = data[colonne].fillna(valeur_remplace, inplace=True)
    #                         # Sinon message d'erreur 
    #                         else :
    #                             st.write("Erreur, veuillez rentrer un nombre (séparé par un . si décimal) et non du texte")
    #                     # Si on décide de remplacer par la moyenne, on le fait
    #                     if choix_remplace == "La moyenne de la colonne" : 
    #                         data = remplace_valeur_num_moyenne(data,colonne)
    #                     # Si on décide de remplacer par la médiage, on le fait
    #                     if choix_remplace == "La médiane de la colonne" :
    #                         data = remplace_valeur_num_mediane(data,colonne)
    #                 # Si la colonne est catégorielle, on aura 2 choix : valeur unique, valeur la plus fréquente
    #                 else :
    #                     choix_remplace = menu_rempl_indiv_cat()
    #                     # Si on décide de remplacer par une valeur à saisir, on la saisit et on remplace
    #                     if choix_remplace == "Une valeur unique" :
    #                         valeur_remplace = st.text_input("Entrez ici la valeur de remplacement")
    #                         valeur_remplace = str(valeur_remplace)
    #                         data = data[colonne].fillna(valeur_remplace, inplace=True)
    #                     # Si on décide de rempalcer par la fréquence
    #                     if choix_remplace == "La valeur de la colonne la plus fréquente" : 
    #                         data = remplace_valeur_cat_freq(data,colonne)
    st.write("Voici votre nouvelle base de données :")
    st.write(data.head())
    st.write("Vérification des valeurs manquantes :")
    message_valeurs, valeurs_null = identification_nan(data)
    st.write(message_valeurs)
    
    return data
            
            
        




    

        


