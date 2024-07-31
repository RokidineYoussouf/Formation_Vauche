# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:47:17 2024

@author: yrd
"""

import pandas as pd

# Charger le fichier Excel
file_path =  'bddAI.xlsx'
data = pd.read_excel(file_path, sheet_name='Feuil1')

# Supprimer la colonne 'Unnamed: 0'
data.drop(columns=['Unnamed: 0'], inplace=True)

# Renommer la colonne "Long\\larg" pour plus de clarté
data.rename(columns={'Long\\larg': 'Longueur'}, inplace=True)

# Utiliser la méthode melt pour transformer les colonnes de largeurs en une seule colonne
melted_data = data.melt(id_vars=['Longueur'], var_name='Largeur', value_name='Poids')

# Filtrer les lignes où "Largeur" est numérique et où "Poids" n'est pas NaN
melted_data = melted_data[melted_data['Largeur'].apply(lambda x: str(x).isdigit())]

# Convertir les colonnes "Largeur" et "Poids" en valeurs numériques
melted_data['Largeur'] = pd.to_numeric(melted_data['Largeur'])
melted_data['Poids'] = pd.to_numeric(melted_data['Poids'])

# Afficher les premières lignes des données transformées
print(melted_data.head())



import pandas as pd

# Charger le fichier Excel
file_path =  'bddAI.xlsx'

data = pd.read_excel(file_path, sheet_name='Feuil1')

# Supprimer la colonne 'Unnamed: 0'
data.drop(columns=['Unnamed: 0'], inplace=True)

# Renommer la colonne "Long\\larg" pour plus de clarté
data.rename(columns={'Long\\larg': 'Longueur'}, inplace=True)

# Utiliser la méthode melt pour transformer les colonnes de largeurs en une seule colonne
melted_data = data.melt(id_vars=['Longueur'], var_name='Largeur', value_name='Poids')

# Filtrer les lignes où "Largeur" est numérique et où "Poids" n'est pas NaN
melted_data = melted_data[melted_data['Largeur'].apply(lambda x: str(x).isdigit())]

# Convertir les colonnes "Largeur" et "Poids" en valeurs numériques
melted_data['Largeur'] = pd.to_numeric(melted_data['Largeur'])
melted_data['Poids'] = pd.to_numeric(melted_data['Poids'])

# Créer une nouvelle colonne pour la surface
melted_data['Surface'] = melted_data['Longueur'] * melted_data['Largeur']

# Calculer le poids moyen par surface
average_weight_by_surface = melted_data.groupby('Surface')['Poids'].mean().reset_index()

# Afficher les premières lignes des poids moyens par surface
print(average_weight_by_surface.head())

















import pandas as pd

# Charger le fichier Excel
file_path = 'bddAI.xlsx'
data = pd.read_excel(file_path, sheet_name='Feuil1')

# Supprimer la colonne 'Unnamed: 0'
data.drop(columns=['Unnamed: 0'], inplace=True)

# Renommer la colonne "Long\\larg" pour plus de clarté
data.rename(columns={'Long\\larg': 'Longueur'}, inplace=True)

# Utiliser la méthode melt pour transformer les colonnes de largeurs en une seule colonne
melted_data = data.melt(id_vars=['Longueur'], var_name='Largeur', value_name='Poids')

# Filtrer les lignes où "Largeur" est numérique et où "Poids" n'est pas NaN
melted_data = melted_data[melted_data['Largeur'].apply(lambda x: str(x).isdigit())]

# Convertir les colonnes "Largeur" et "Poids" en valeurs numériques
melted_data['Largeur'] = pd.to_numeric(melted_data['Largeur'])
melted_data['Poids'] = pd.to_numeric(melted_data['Poids'])

# Créer une nouvelle colonne pour la surface
melted_data['Surface'] = melted_data['Longueur'] * melted_data['Largeur']

# Calculer le poids moyen par surface
average_weight_by_surface = melted_data.groupby(['Longueur', 'Largeur'])['Poids'].mean().reset_index()

# Réorganiser les données sous forme matricielle
pivot_table = average_weight_by_surface.pivot(index='Longueur', columns='Largeur', values='Poids')

# Afficher les premières lignes de la table pivotée
print(pivot_table.head())

# Si vous souhaitez enregistrer le résultat dans un fichier Excel
pivot_table.to_excel('poids_moyens_surface.xlsx')



















import pandas as pd

# Charger le fichier Excel
file_path = 'bddAI.xlsx'
data = pd.read_excel(file_path, sheet_name='Feuil1')

# Supprimer la colonne 'Unnamed: 0'
data.drop(columns=['Unnamed: 0'], inplace=True)

# Renommer la colonne "Long\\larg" pour plus de clarté
data.rename(columns={'Long\\larg': 'Longueur'}, inplace=True)

# Utiliser la méthode melt pour transformer les colonnes de largeurs en une seule colonne
melted_data = data.melt(id_vars=['Longueur'], var_name='Largeur', value_name='Poids')

# Filtrer les lignes où "Largeur" est numérique et où "Poids" n'est pas NaN
melted_data = melted_data[melted_data['Largeur'].apply(lambda x: str(x).isdigit())]

# Convertir les colonnes "Largeur" et "Poids" en valeurs numériques
melted_data['Largeur'] = pd.to_numeric(melted_data['Largeur'])
melted_data['Poids'] = pd.to_numeric(melted_data['Poids'])

# Créer une nouvelle colonne pour la surface
melted_data['Surface'] = melted_data['Longueur'] * melted_data['Largeur']

# Calculer le poids moyen par surface
average_weight_by_surface = melted_data.groupby(['Longueur', 'Largeur'])['Poids'].mean().reset_index()

# Réorganiser les données sous forme matricielle
pivot_table = average_weight_by_surface.pivot(index='Longueur', columns='Largeur', values='Poids')

# Afficher les résultats sous forme matricielle
print(pivot_table)

# Si vous souhaitez enregistrer le résultat dans un fichier Excel
pivot_table.to_excel('poids_moyens_surface.xlsx')

















import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt

# Charger le fichier Excel
file_path = 'bddAI.xlsx'
data = pd.read_excel(file_path, sheet_name='Feuil1')

# Supprimer la colonne 'Unnamed: 0'
data.drop(columns=['Unnamed: 0'], inplace=True)

# Renommer la colonne "Long\\larg" pour plus de clarté
data.rename(columns={'Long\\larg': 'Longueur'}, inplace=True)

# Utiliser la méthode melt pour transformer les colonnes de largeurs en une seule colonne
melted_data = data.melt(id_vars=['Longueur'], var_name='Largeur', value_name='Poids')

# Filtrer les lignes où "Largeur" est numérique et où "Poids" n'est pas NaN
melted_data = melted_data[melted_data['Largeur'].apply(lambda x: str(x).isdigit())]

# Convertir les colonnes "Largeur" et "Poids" en valeurs numériques
melted_data['Largeur'] = pd.to_numeric(melted_data['Largeur'])
melted_data['Poids'] = pd.to_numeric(melted_data['Poids'])

# Créer une nouvelle colonne pour la surface
melted_data['Surface'] = melted_data['Longueur'] * melted_data['Largeur']

# Calculer le poids moyen par surface
average_weight_by_surface = melted_data.groupby(['Longueur', 'Largeur'])['Poids'].mean().reset_index()

# Réorganiser les données sous forme matricielle
pivot_table = average_weight_by_surface.pivot(index='Longueur', columns='Largeur', values='Poids')


surface_moyenne=melted_data["Surface"].mean()



