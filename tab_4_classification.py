"""
IMPORTS NÉCESSAIRES À CE MODULE :
"""

# Pour la récupération d'entrées utilisateur sur streamlit + l'affichage (titres, figures, texte) :
import streamlit as st
import pandas as pd

# Module contenant les fonctions appelées pour le modèle de regression
import regression # remplacer par : from modeles import regression

# Pour les modèles de classification et le validation croisée
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, cross_val_score

# Entrainement du modèle 
def entrainer_modele(select_model: DecisionTreeClassifier, X_train, y_train, X_test, **params):
    try:
        clf = select_model.set_params(**params)
        clf.fit(X_train, y_train) 
        y_pred = clf.predict(X_test)
        print(f"Le modèle est entrainé avec l'algorithme {clf.__class__.__name__}.")
        print(clf.__dict__)
        return y_pred
    except Exception as e:
        st.write(str(e)," : Il y a eu une erreur")

def clf_report(y_pred, y_test):
    cr = classification_report(y_test, y_pred)
    return cr

## Validation croisée (avec StratifiedKFold)
def val_croisee_clf(select_model: DecisionTreeClassifier,X, y, n_splits:int=4, **params):
    try:
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        clf = select_model.set_params(**params)
        score_clf = cross_val_score(clf, X, y, cv=skf, scoring='accuracy') 
        # à tester avec 1 autre metrics : 'f1', 'f1-weighted', etc. ?
        return score_clf
    except Exception as e:
        st.write(str(e),": Il y a eu une erreur dans la validation croisée.")

# X_train, X_test, y_train, y_test = regression.split(X, y, 0.25)

def etapes_clf(features,target):

    st.subheader('Modèle')
   
    """
    1. CHOIX D'UN MODÈLE
    """

    with st.expander("**Choix d'un modèle de classification :**", expanded=False):

        select_model = st.radio("Sélectionnez un modèle d'entraînement :", \
                                ("LogisticRegression", "DecisionTreeClassifier (défaut)", "RandomForestClassifier", 
                                "SVC", "KNeighborsClassifier"))
        message= "Vous avez choisi : "+select_model
        st.write(message)

        """
        2. TESTS et VALIDATION DU MODÈLE
        """
        n_splits = st.number_input(label="Entrez un nombre de lots : ", min_value=4, max_value=10, step=1)
        
        if select_model == "LogisticRegression":
            rs = 42
            solver = 'liblinear'
            C_defaut = 1 #regularization strenght
            max_iter_defaut = 100
            C_user = float(st.text_input("Entrez une valeur de C (nombre décimal supérieur à 1 ) : ", C_defaut))
            max_iter = int(st.text_input("Entrez un nombre d'itérations maximum : ", max_iter_defaut))
            model = LogisticRegression(random_state=rs, C=C_user, max_iter=max_iter, solver=solver)

        elif select_model == "RandomForestClassifier":
            n_estimator_dft = 20
            rs = 42
            n_estimator = int(st.text_input("Entrez un nombre d'arbres (min: 5, max: 200) : ", n_estimator_dft))
            model = RandomForestClassifier(n_estimators=n_estimator, random_state=rs)
    
        elif select_model == "SVC":
            C_defaut = 1 #regularization strenght
            max_iter_defaut = 100
            C_user = float(st.text_input("Entrez une valeur de C (nombre décimal supérieur à 1 ) : ", C_defaut))
            max_iter = int(st.text_input("Entrez un nombre d'itérations maximum : ", max_iter_defaut))
            model = SVC(C=C_user, max_iter=max_iter)
    
        elif select_model == "KNeighborsClassifier":
            n_neighbors_defaut = 5
            n_neighbors = int(st.text_input("Entrez un nombre de voisins (entre 1 et 50) : ", n_neighbors_defaut))
            model = KNeighborsClassifier(n_neighbors==n_neighbors)

        else:
            cls_weight = None #peut-être modif en 'balanced' ou dict
            rs = 42
            model = DecisionTreeClassifier(random_state=rs, class_weight=cls_weight)

        # data_pred = entrainer_modele(select_model, X_train, y_train, X_test)
        report = val_croisee_clf(select_model, features, target, n_splits)
        
        # Affichage des scores de validation croisée
        st.write("Rapport de validation croisée sur les", str(n_splits),"lots :")
        st.write(report)
        
    """
    3. GRID SEARCH
    """
    n_splits = st.number_input(label="Entrez un nombre de lots pour la validation croisée : ", min_value=4, max_value=8, step=1)
    scoring = 'accuracy'

    with st.expander("**Comparaison des modèles de classification :**", expanded=False):

        # Liste des modèles à évaluer
        models_clf = [
            ('LogReg', LogisticRegression()),
            ('DecisTreeClf', DecisionTreeClassifier()),
            ('RandomForestClf', RandomForestClassifier()),
            ('KNC', KNeighborsClassifier()),
            ('SVC', SVC())
        ]

        # Grille de paramètres pour chaque modèle
        parameters = {
            'LogReg': {'penalty': ['l2', None], 'C': [1, 5, 10], 'solver':['lbfgs', 'liblinear', 'newton-cg', 'sag'], 'class_weight': [None, 'balanced']},
            'DecisTreeClf': {'criterion': ['gini', 'log_loss'], 'splitter': ['best', 'random'], 'max_depth': [None, 2, 5], 'class_weight': [None, 'balanced']},
            'RandomForestClf': {'criterion': ['gini', 'log_loss'], 'n_estimators': [5, 10, 100], 'max_depth': [None, 5], 'class_weight': [None, 'balanced']},
            'KNC': {'n_neighbors': [2, 5, 10, 20], 'weights': ['uniform', 'distance'], 'algorithm': ['ball_tree', 'kd_tree', 'brute']},
            'SVC': {'C': [1, 5, 10], 'kernel': ['poly', 'rbf', 'sigmoid'], 'max_iter': [-1, 10, 100], 'class_weight': [None, 'balanced']}
        }

        # Split des données
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.25, random_state=42)
        
        # Effectuer une recherche sur grille pour chaque modèle
        
        best_estimators = {}
        for model_name, model in models_clf:
            grid_search = GridSearchCV(model, parameters[model_name], cv=5, scoring=scoring)
            grid_search.fit(X_train, y_train)

            best_estimators[model_name] = grid_search.best_estimator_

        st.write(best_estimators)


