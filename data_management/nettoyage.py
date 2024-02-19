import streamlit as st


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
        valeurs_null = "Non"
    else :
        message = 'Votre base de données contient des valeurs manquantes'
        valeurs_nan = valeurs[valeurs >0]
        st.write(valeurs_nan)
        valeurs_null = "Oui"
    return message, valeurs_null

        
def supprimer_colonnes(data) :
    valeurs = data.isna().sum()
    valeurs_nan = valeurs[valeurs >0]
    colonnes_avec_nan = valeurs_nan.index.tolist()
    data = data.drop(columns=colonnes_avec_nan,axis=1)
    return data

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


def choix_traitement_nan(data) :
    st.write('Que souhaitez-vous faire ?')
    supprimer_lignes = st.checkbox("Supprimer toutes les lignes contenant des valeurs null ?")
    traitement_commun = st.checkbox("Traiter toutes les colonnes de la même façon")
    traitement_indiv = st.checkbox("Traiter les colonnes une par une")
    
    if supprimer_lignes :
        st.write("<span style='color:red'>!! Attention, cette action peut fortement réduire le nombre d'enregistrements de votre base de données !! </span>", unsafe_allow_html=True)
        nb_enreg = data.shape[0]
        st.write("Votre base de données contient actuellement " + str(nb_enreg) + " enregistrements")
        data_sans_nulles = data.dropna()
        nb_enreg_apres = data_sans_nulles.shape[0]
        nb_supp = nb_enreg - nb_enreg_apres
        st.write("Vous allez supprimer " + str(nb_supp) + " enregistrements")
        verification_supp = st.radio("Souhaitez-vous vraiment supprimer tous les enregistrements ?", ("Oui", "Non"))
        if verification_supp == "Non" :
            st.write("Veuillez sélectionner un autre choix au menu du dessus")
        elif verification_supp == "Oui" :
            data = data_sans_nulles
            st.write(data.head())
        

    if traitement_commun :
        choix_commun = st.radio("Quelle action souhaitez-vous effectuer ?", ("Supprimer les colonnes", "Remplacer les valeurs manquantes"))
        if choix_commun == "Supprimer les colonnes" :
            data = supprimer_colonnes(data)  
            st.write(data.head()) 
        if choix_commun == "Remplacer les valeurs manquantes" : 
            data = remplacer_valeurs_manquantes(data)
            st.write(data.head())
    
    if traitement_indiv :
        valeurs = data.isna().sum()
        valeurs_nan = valeurs[valeurs >0]
        colonnes_avec_nan = valeurs_nan.index.tolist()
        for colonne in colonnes_avec_nan :
            choix_indiv = st.radio("Quelle action souhaitez-vous effectuer pour la colonne " + colonne + " ?", ("Supprimer la colonne", "Remplacer les valeurs manquantes"))
            if choix_indiv == "Supprimer la colonne" :
                data = data.drop(columns=colonne,axis=1)
                st.write("Vous venez de supprimer la colonne "+ colonne + ". Voici votre nouvelle base de données")
                st.write(data.head())
            if choix_indiv == "Remplacer les valeurs manquantes" :
                choix_remplace = st.radio("Par quelle valeur souhaitez-vous remplacer ?",("Une valeur unique","La moyenne/la valeur la plus fréquente"))
                if choix_remplace == "Une valeur unique" :
                    pass
                if choix_remplace == "La moyenne/la valeur la plus fréquente" : 
                    pass
        
    
    return data
            
            
        




    

        


