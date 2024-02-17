import pandas as pd
#import matplotlib.pyplot as plt
import target
import statsmodels.formula.api as smf

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score


file = r'D:\POEC_Data_Analyst_Diginamic\Projet_ML\vin.csv' #à modifier selon chemin fichier
data = pd.read_csv(file, sep=',')

#suppression de la 1ère colonne
data.drop(columns=['Unnamed: 0'], inplace=True)

#choix des features (tous par défaut)
X = data.loc[:, data.columns != 'target']   

# Ecodage de la target:
test = target.encodage('target', 'target_code')
# print(test)
print(data)

#choix de la target
y = data['target_code']   

#Split du jeu de données
X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)

model_type = ['Regression', 'Classification']
#models_reg = [LinearRegression(), ]
models_clf = [LogisticRegression(), DecisionTreeClassifier(), RandomForestClassifier(),
    SVC(), KNeighborsClassifier()]

# def choix_model(type):

# Entrainement du modèle 
def entrainer_modele(model: LogisticRegression, **params):
    try:
        clf = model.set_params(**params)
        clf.fit(X_train, y_train) #modèle entrainé
        y_pred = clf.predict(X_test)
        cr = classification_report(y_test, y_pred)
        print(clf.__dict__)
        print(f"Le modèle est entrainé avec l'algorithme {clf.__class__.__name__}. Voici son rapport de classification : {cr}")
        return cr
    except Exception as e:
        print(f"{e} :Il y a eu une erreur")

data_pred = entrainer_modele(LogisticRegression())
print(data_pred)

## Validation croisée (cop/col du TP corrigé J3_regressions)
# def cross_validate(model, data, nb_folds):
#     kf = KFold(n_splits=nb_folds, shuffle=True, random_state=42)
#     split = list(kf.split(data[FEATURES],data[TARGET])) #FEATURES/TARGET à remplacer
#     test = []
#     for i,(train_index, test_index) in enumerate(split):
#         print(f"\n ---------------- Fold {i+1} ------------\n")
#         print(f" -------------- Training on {len(train_index)} samples-------------- ")
#         print(f" -------------- Validation on {len(test_index)} samples-------------- ")
    
#         data_train = data.loc[train_index] 
#         data_test = data.loc[test_index] 
    
#         # create a fitted model
#         lm = smf.ols(formula=f'target ~ {equation}',data=data_train).fit()
    
#         y_hat = lm.predict(data_test[FEATURES])
#         test.append({
#             'R2': r2_score(data_test[TARGET].values, y_hat),
#             'model': lm
#         })
#         print(f" Fold {i+1} :  MSE {round(mean_squared_error(data_test[TARGET].values,y_hat),4)}")
#         print(f" Fold {i+1} :  R2 {round(r2_score(data_test[TARGET].values,y_hat),4)}")
#         plt.scatter(data_test[TARGET].values,y_hat)
#         plt.plot(np.arange(0,50))
#         plt.show()

# # Effectuer la validation croisée
# scores = cross_val_score(model, X, y, cv=kf, scoring='accuracy')



'''
Test multi-modèles (à faire ou avec GridSearchCV ?)
'''
# for clf in models_clf:
#     clf.fit(X_train, y_train)
#     y_pred = clf.predict(X_test)
#     cr = classification_report(y_test, y_pred)
    
#     print("Algorithme utilisé : ", clf.__class__.__name__)
#     print("Rapport de classification :")
#     print(cr)
#     print("\n")
