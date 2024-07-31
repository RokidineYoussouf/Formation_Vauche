# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 08:26:42 2024

@author: yrd
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt


excel_path = 'bddAI.xlsx'
df = pd.read_excel(excel_path)

data=df.drop(["Unnamed: 0"], axis=1)

longueur=data["Long\larg"] 
largeur=data.columns[1:]

# Itérer sur les lignes du DataFrame
for i in range(len(data)):
    # Récupérer la longueur de la ligne actuelle
    longueur = data.iloc[i, 0] 
    
    # Itérer sur les colonnes qui représentent les largeurs
    for j in range(1, len(data.columns)): 
        # Récupérer la largeur de la colonne actuelle
        largeur = data.columns[j]
        
        # Multiplier longueur par largeur et stocker le résultat dans la colonne 'Surface'
        data.iloc[i, j] = longueur * int(largeur)
        Surface=data
# Calculer la surface des convoyeurs
data=df.drop(["Unnamed: 0"], axis=1)
# Créer une nouvelle colonne pour le poids moyen par unité de surface
data['Poids_moyen_par_surface'] = 0


# Calculer le poids moyen pour chaque longueur
for i in range(len(data)):
    # Calculer la somme des poids pour la longueur actuelle
    somme_poids = data.iloc[i, 1:].sum()
    
    # Calculer le poids moyen par unité de surface
    data.iloc[i, -1] = somme_poids / data.iloc[i, -2]

# Afficher le DataFrame avec le poids moyen par unité de surface
print(data)


import pandas as pd

# Charger le fichier Excel
file_path =  'bddAI.xlsx'
data = pd.read_excel(file_path, sheet_name='Feuil1')

# Renommer la première colonne pour plus de clarté
data.rename(columns={'Unnamed: 0': 'Index', 'Long\\larg': 'Longueur'}, inplace=True)

# Utiliser la méthode melt pour transformer les colonnes de largeurs en une seule colonne
melted_data = data.melt(id_vars=['Longueur'], var_name='Largeur', value_name='Poids')

# Filtrer les lignes où "Largeur" est numérique et où "Poids" n'est pas NaN
melted_data = melted_data[melted_data['Largeur'].apply(lambda x: str(x).isdigit())]

# Convertir les colonnes "Largeur" et "Poids" en valeurs numériques
melted_data['Largeur'] = pd.to_numeric(melted_data['Largeur'])
melted_data['Poids'] = pd.to_numeric(melted_data['Poids'])

# Afficher les premières lignes des données transformées
print(melted_data.head())







# Calculer le poids moyen par unité de surface pour chaque longueur
data["Poids_moyen_600"] = data["600"] / data["Surface"] 
data["Poids_moyen_800"] = data["800"] / data["Surface"]
# ... répéter pour chaque colonne de poids

# Calculer le poids moyen total pour chaque longueur
poids_moyen_total_600 = data["Poids_moyen_600"].mean()
poids_moyen_total_800 = data["Poids_moyen_800"].mean()
# ... répéter pour chaque colonne de poids

# Afficher les résultats
print("Poids moyen total pour une longueur de 600 m :", poids_moyen_total_600)
print("Poids moyen total pour une longueur de 800 m :", poids_moyen_total_800)
# ... 