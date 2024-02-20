"""
IMPORTS NÉCESSAIRES À CE MODULE :
"""

# Pour la récupération d'entrées utilisateur sur streamlit + l'affichage (titres, figures, texte) :
import streamlit as st

# Module contenant les fonctions appelées pour le modèle de regression
import regression # remplacer par : from modeles import regression

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
        cv_metrics, list_fig, list_models = regression.validation_croisee(model,n_splits,features,target)
        st.write(cv_metrics)

        # Plots
        for fig in list_fig:
            st.pyplot(fig)

        # Métriques moyennes
        cv_R2_moy, cv_RMSE_moy, cv_MAE_moy = regression.metrics_moy(cv_metrics,n_splits)

        # Affichage les scores de validation croisée
        st.write("Metrics moyennes de validation croisée sur les", str(n_splits),"lots :")
        st.write("- Moyenne des coefficients de détermination : R² = ", str(round(cv_R2_moy,4)))
        st.write("- Moyenne des racines carrées de l'erreur quadratique moyenne : RMSE = ",str(round(cv_RMSE_moy,2)))
        st.write("- Moyenne de l'erreur absolue moyenne : MAE = ",str(round(cv_MAE_moy,2)))


        """
        c. ENREGISTREMENT DU MODÈLE (SÉLECTION PARMI LES LOTS DE LA x VALIDATION
        """

        st.subheader("Sauvegarde du modèle")
        select_svg_model = st.radio("--> Souhaitez-vous sauvegarder le modèle ?", ("Non","Oui"))

        if select_svg_model == "Non":
            st.write("--> Pas de modèle sauvegardé.")
            model_svg = "" # car la fonction retourne forcément un modèle

        else:         
            list_index_models = list(range(0,n_splits))
            index_model = int(st.radio(label="Entrez l'indice du modèle que vous souhaitez enregistrer : ",options=list_index_models))
            model_svg = list_models[index_model]

            if model_selection == "LinearRegression (par défaut)":
                st.write("--> Modèle LinearRegression entraînement n°",index_model,"sauvegardé pour réaliser des prédictions.")
            else:
                st.write("--> Modèle",model_selection," (alpha :",str(alpha)," ; max_iter :",str(max_iter)," ; tol :",str(tol),"), entraînement n°",index_model, "sauvegardé pour réaliser des prédictions.")

        
    """
    3. COMPARAISON DES MODÈLES
    """

    with st.expander("**Comparaison des trois modèles de régression (méthode manuelle) :**", expanded=False):
        
        """
        a. GRID SEARCH
        """

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

            info = "-"+str(iteration)+": ok"
            st.write(info)
            
            model = structure[iteration]['model']
            parameters = structure[iteration]['hyperparameters']
            values_lists = list(parameters.values())
            combinations = list(product(*values_lists))
            possibility = [dict(zip(parameters.keys(), combo)) for combo in combinations]
            
            for possible in possibility:

                i += 1
                # st.write(i)
                
                try:                    
                    model.set_params(**possible)
                    # st.write(model.get_params(deep=True))

                    # Appel de la focntion validation croisée, retourne un dataframe avec les 3 metrics R2, RMSE, MAE:
                    # 'R2','RMSE','MAE','train_sample_size','test_sample_size'
                    cv_metrics_GS, liste_fig, list_models = regression.validation_croisee(model,n_splits,features,target)

                    # Métriques moyennes
                    cv_R2_moy, cv_RMSE_moy, cv_MAE_moy = regression.metrics_moy(cv_metrics,n_splits)

                    results_GS[i] = [possible,model,cv_R2_moy, cv_RMSE_moy, cv_MAE_moy]

                except:
                    st.write(i, "Les hyperparamètres ne sont pas initialisables entre eux.")
           
        st.write("Nombre de modèles testés : ",len(results_GS))

        """
        b. SÉLECTION DU MEILLEUR MODÈLE
        """

        st.subheader("Sélection du meilleur modèle")

        # results_GS_df = pd.DataFrame(results_GS)
        results_GS_df = pd.DataFrame.from_dict(results_GS, orient='index')
        results_GS_df = results_GS_df.rename(columns={0:'param',1:'model',2:'R2',3:'RMSE',4:'MAE'})
        st.write(results_GS_df)

        st.write("Meilleur modèle (R² le plus élevé) : ")
        ligne_max_R2 = results_GS_df.loc[results_GS_df['R2'].idxmax()]
        st.write(ligne_max_R2)
        
        
        """
        c. ENREGISTREMENT DU MEILLEUR MODÈLE
        """

        st.subheader("Sauvegarde du modèle")
        select_svg_model = st.radio("--> Souhaitez-vous sauvegarder le modèle ?", ("Non","Oui"),key="34")

        if select_svg_model == "Non":
            st.write("--> Pas de modèle sauvegardé.")
            model_svg = "" # car la fonction retourne forcément un modèle

        else:         
            index_model = ligne_max_R2.name
            model_svg = ligne_max_R2['model']

            if model_selection == "LinearRegression (par défaut)":
                st.write("--> Modèle LinearRegression entraînement n°",index_model,"sauvegardé pour réaliser des prédictions.")
            else:
                st.write("--> Modèle",model_selection," (alpha :",str(alpha)," ; max_iter :",str(max_iter)," ; tol :",str(tol),"), entraînement n°",index_model, "sauvegardé pour réaliser des prédictions.")


    with st.expander("**Comparaison des trois modèles de régression (méthode GridSearchCV) :**", expanded=False):


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
    return model_svg