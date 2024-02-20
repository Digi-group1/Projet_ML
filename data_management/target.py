import pandas as pd
from sklearn import preprocessing

# file = r'D:\POEC_Data_Analyst_Diginamic\Projet_ML\vin.csv' #à modifier selon chemin fichier
# data = pd.read_csv(file, sep=',')

# Détection et identification d'une colonne Target
def detect_target(data):
    nom_target = 'target' #ou = re.compile(r'\b\w*target\w*\b', re.IGNORECASE) pour généraliser -> à tester
    if nom_target in data.columns:
        target_detect = data[nom_target]
        #print(f"La colonne '{nom_target}' a été détectée :\n{target_detect}")
        test_target = isinstance(target_detect, (int, float))
        if test_target == True:
            msg_num = "La target détectée est de type numérique."
            return msg_num
        else:
            msg_txt = "La target détectée est de type objet/texte."
            return msg_txt
    else:
        no_target = f"La colonne '{nom_target}' n'existe pas dans le DataFrame." 
        return no_target # ->Choix de la target dans ce cas ?

# test = detect_target(data)
# print(test) #OK

# Afficher le compteur et la fréquence de chaque valeur
def stats(data,col: str): #prend le nom de la colonne à tester
    compt = data[col].value_counts()
    for val, compt in compt.items():
        freq = compt / len(data)
        print(f"Valeur : {val}, Compteur : {compt}, Fréquence : {freq:.1%}")

# test = stats('target') #OK


#Encodage de la target (cas d'une target non numérique)
def encodage(colonne: str, new_col: str): # prend le nom de la colonne à encoder et celui de la nvle colonne
    i = 0
    labels = {}
    for _, val in enumerate(data[colonne].unique()):
        labels.update({val : i})
        i +=1
        data[new_col] = data[colonne].map(labels)
    message = f"La colonne {colonne} a bien été encodée. Voici le résultat de {new_col} : "
    new_col_test = data[new_col].value_counts()
    return message, new_col_test

test = encodage('target', 'target_code')
# print(test) #OK
# print(data) #OK
