"""
IMPORTS NÉCESSAIRES À CE MODULE :
"""

# Pour la récupération d'entrées utilisateur sur streamlit + l'affichage (titres, figures, texte) :
import streamlit as st

# Module contenant les fonctions appelées pour le modèle de regression
from modeles import regression # remplacer par : from modeles import regression

# Pour la validation croisée et le grissearch
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import GridSearchCV,train_test_split
from itertools import product

import pandas as pd


"""
FONCTION "ETAPE_REGRESSION" :
    > fonction unique de ce module
    > entrée : la serie "target" + le dataframe "features" (entrées du modèle)
    > sorties : R² et erreur quadratique moyenne
"""

def etapes(features,target):

    st.subheader('Modèle de régression linéaire')
   
    """
    1. CHOIX D'UN MODÈLE
    """

    with st.expander("**Entrainement des données sur un modèle de régression :**", expanded=False):
       
        """
        a. CHOIX DU MODÈLE DE RÉGRESSION :
        """

        model_selection = st.radio("Sélectionnez un modèle de régression : ", \
                                            ("LinearRegression (par défaut)", "Ridge", "Lasso")
                                            )
        st.write("Vous avez choisi : "+model_selection)


        """
        b. CROSS VALIDATION
        """
        n_splits = st.number_input(label="Entrez un nombre de lots : ", min_value=5, max_value=10, step=1)

        if model_selection == "Ridge":
            alpha_defaut = 0.5
            max_iter_defaut = 1000
            tol_defaut = 1e-4
            alpha = float(st.text_input("Entrez une valeur de alpha (nombre décimal ou entier) : ", alpha_defaut))
            max_iter = int(st.text_input("Entrez un nombre d'itérations maximum : ", max_iter_defaut))
            tol = float(st.text_input("Entrez une valeur pour la tolérance : ", tol_defaut))
            model = regression.ridge_instant(alpha, max_iter, tol)

        elif model_selection == "Lasso":
            alpha_defaut = 0.5
            max_iter_defaut = 1000
            tol_defaut = 1e-4
            alpha = float(st.text_input("Entrez une valeur de alpha (nombre décimal ou entier) : ", alpha_defaut))
            max_iter = int(st.text_input("Entrez un nombre d'itérations maximum : ", max_iter_defaut))
            tol = float(st.text_input("Entrez une valeur pour la tolérance : ", tol_defaut))
            model = regression.lasso_instant(alpha, max_iter, tol)

        else:
            model = regression.linear_instant()


        # Appel de la focntion validation croisée, retourne un dataframe avec les 3 metrics R2, RMSE, MAE:
        # 'R2','RMSE','MAE','train_sample_size','test_sample_size'
        cv_metrics, liste_fig = regression.validation_croisee(model,n_splits,features,target)
        st.write(cv_metrics)

        # Plots
        for fig in liste_fig:
            st.pyplot(fig)

        # Métriques moyennes
        cv_R2_moy, cv_RMSE_moy, cv_MAE_moy = regression.metrics_moy(cv_metrics,n_splits)

        # Affichage les scores de validation croisée
        st.write("Metrics moyennes de validation croisée sur les", str(n_splits),"lots :")
        st.write("- Moyenne des coefficients de détermination : R² = ", str(round(cv_R2_moy,4)))
        st.write("- Moyenne des racines carrées de l'erreur quadratique moyenne : RMSE = ",str(round(cv_RMSE_moy,2)))
        st.write("- Moyenne de l'erreur absolue moyenne : MAE = ",str(round(cv_MAE_moy,2)))


        """
        c. ENREGISTREMENT DU MODÈLE (NOUVEL ENTRAINEMENT)
        """

        st.header("Sauvegarde du modèle")
        select_svg_model = st.radio("--> Réentrainer le modèle sur le jeu de données et le sauvegarder ?", ("Non","Oui"))

        if select_svg_model == "Non":
            st.write("--> Pas de modèle sauvegardé.")
            model_svg = "" # car la fonction retourne forcément un modèle

        else:
         
            # Nouveau split train/test du jeu de données :
            X_train, X_test, y_train, y_test = regression.split(features,target,n_splits)

            # Reprend le modèle sélectionné et l'entraîne sur un nouvel échantillon de train :
            if model_selection == "Ridge":
                model = regression.ridge_instant(alpha, max_iter, tol)

            elif model_selection == "Lasso":
                model = regression.lasso_instant(alpha, max_iter, tol)

            else:
                model = regression.linear_instant()
            
            # Entraînement du modèle :
            model.fit(X_train, y_train)

            # Prédiction du modèle sur X_test :
            y_pred = model.predict(X_test)

            # Trace le plot y_pred y_test
            fig = regression.plot_test_pred(y_test,y_pred)
            st.pyplot(fig)
            
            # Évaluation du modèle sur les données de test :
            R2, RMSE, MAE = regression.metrics(y_test,y_pred)
            st.write("- Coefficient de détermination : R² = ", str(R2))
            st.write("- Racine carrée de l'erreur quadratique moyenne : RMSE = ",str(RMSE))
            st.write("- Erreur absolue moyenne : MAE = ",str(MAE))

            if model_selection == "LinearRegression (par défaut)":
                st.write("--> Modèle LinearRegression sauvegardé pour réaliser des prédictions.")
            else:
                st.write("--> Modèle",model_selection," (alpha :",str(alpha)," ; max_iter :",str(max_iter)," ; tol :",str(tol),") sauvegardé pour réaliser des prédictions.")

            model_svg = model


        
    """
    3. GRID SEARCH
    """

    with st.expander("**Évaluation des trois modèles de régression (1) :**", expanded=False):

        # iteration
        n_splits = 5
        structure = {
            'LinearRegression': {
                'model': LinearRegression(),
                'hyperparameters': {}
            },
            'Lasso': {
                'model': Lasso(),
                'hyperparameters': {
                    'alpha': [0.01, 0.1, 1.0, 10.0],
                    'max_iter': [100, 1000, 10000],
                    'tol': [0.0001, 0.001, 0.01]
                    }
            },
            'Ridge': {
                'model': Ridge(),
                'hyperparameters': {
                    'alpha': [0.01, 0.1, 1.0, 10.0],
                    'max_iter': [100, 1000, 10000],
                    'tol': [0.0001, 0.001, 0.01]
                    }
            },
        }


        results_GS = {}  
        i = 0 

        for iteration in structure:

            info = str(iteration)
            # st.write(info)
            
            model = structure[iteration]['model']
            parameters = structure[iteration]['hyperparameters']
            values_lists = list(parameters.values())
            combinations = list(product(*values_lists))
            possibility = [dict(zip(parameters.keys(), combo)) for combo in combinations]
            
            for possible in possibility:

                i += 1
                # st.write(possible)
                
                try:
                    
                    model.set_params(**possible)

                    # Appel de la focntion validation croisée, retourne un dataframe avec les 3 metrics R2, RMSE, MAE:
                    # 'R2','RMSE','MAE','train_sample_size','test_sample_size'
                    cv_metrics, liste_fig = regression.validation_croisee(model,n_splits,features,target)
                    # st.write(cv_metrics)

                    # Métriques moyennes
                    cv_R2_moy, cv_RMSE_moy, cv_MAE_moy = regression.metrics_moy(cv_metrics,n_splits)

                    # st.write("Pour", possible, ":")
                    # st.write("- Coefficient de détermination : R² = ", str(R2))
                    # st.write("- Racine carrée de l'erreur quadratique moyenne : RMSE = ",str(RMSE))
                    # st.write("- Erreur absolue moyenne : MAE = ",str(MAE))

                    results_GS[i] = [possible,model,cv_R2_moy, cv_RMSE_moy, cv_MAE_moy]

                except:
                    st.write("Les hyperparamètres ne sont pas initialisable entre eux pour",possible)
           
        
        st.write(results_GS)




    with st.expander("**Évaluation des trois modèles de régression (2) :**", expanded=False):


        n_splits = st.number_input(label="Entrez un nombre de lots pour la validation croisée : ", min_value=5, max_value=10, step=1)
        # scoring_defaut = 'r2'
        # scoring = st.multiselect(label="Sélectionnez la métrique de performance : ", options = ['r2','neg_mean_squared_error'],default=scoring_defaut)
        scoring = 'r2'
        st.write("Métrique de performance des modèles : coeffeicient de détermination R²")

        # Liste des modèles à évaluer
        models = [
            ('LinearRegression', LinearRegression()),
            ('Lasso', Lasso()),
            ('Ridge', Ridge())
        ]

        # Grille de paramètres pour chaque modèle
        parameters = {
            'LinearRegression': {},
            'Lasso': {'alpha': [0.01, 0.1, 1.0, 10.0], 'max_iter': [100, 1000, 10000], 'tol': [0.0001, 0.001, 0.01]},
            'Ridge': {'alpha': [0.01, 0.1, 1.0, 10.0], 'max_iter': [100, 1000, 10000], 'tol': [0.0001, 0.001, 0.01]}
        }

        # Split des données
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        
        # Effectuer une recherche sur grille pour chaque modèle
        best_estimators = {}
        best_score = {}
        for model_name, model in models:
            grid_search = GridSearchCV(model, parameters[model_name], cv=5, scoring=scoring)
            grid_search.fit(X_train, y_train)
            best_estimators[model_name] = grid_search.best_estimator_
            best_score[model_name] = grid_search.best_score_
            st.write(model, parameters[model_name])

        df1 = pd.DataFrame.from_dict(best_estimators, orient='index', columns=['best estimator'])
        df2 = pd.DataFrame.from_dict(best_score, orient='index', columns=['best score'])

        results_GS = pd.merge(df1, df2, left_index=True, right_index=True)

        st.write(results_GS)


    # sorties de fonction tab_4 :
    return (model_svg)