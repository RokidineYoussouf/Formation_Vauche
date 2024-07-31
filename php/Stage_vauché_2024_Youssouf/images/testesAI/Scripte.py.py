# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 10:49:21 2024

@author: yrd
"""

import pandas as pd
import re
# Lecture des fichiers CSV avec la gestion des caractères spécifiques
df_retraiter = pd.read_csv("A retraiter.csv", encoding='latin-1', sep=";")
df_format = pd.read_csv("Format.csv", encoding='latin-1', sep=";")
print(df_retraiter.head())
print(df_format.head())

# Affichons les colonnes des deux fichiers
colonnes_retraiter = df_retraiter.columns
colonnes_format = df_format.columns

print("Colonnes du fichier A retraiter:")
print(colonnes_retraiter)

print("\nColonnes du fichier Format:")
print(colonnes_format)

# Convertissons les colonnes en sets pour une comparaison facile
colonnes_retraiter_set = set(colonnes_retraiter)
colonnes_format_set = set(colonnes_format)

# Colonnes présentes dans les deux fichiers
colonnes_communes = colonnes_retraiter_set.intersection(colonnes_format_set)

# Colonnes présentes uniquement dans "A retraiter"
colonnes_supp_retraiter = colonnes_retraiter_set.difference(colonnes_format_set)

# Colonnes présentes uniquement dans "Format"
colonnes_supp_format = colonnes_format_set.difference(colonnes_retraiter_set)

print("\nColonnes communes :")
print(colonnes_communes)

print("\nColonnes supplémentaires dans A retraiter :")
print(colonnes_supp_retraiter)

print("\nColonnes supplémentaires dans Format :")
print(colonnes_supp_format)

# Colonnes nécessaires
colonnes_necessaires = ['ANNEE', 'NOMENCLATURE', 'STATUT', 'Réalisé total', 'FONCTION',
                        'CODE_AXE_ANALYTIQUE_PROFONDEUR_1', 'LIBELLE_AXE_ANALYTIQUE_PROFONDEUR_1',
                        'CODE_AXE_ANALYTIQUE_PROFONDEUR_2', 'LIBELLE_AXE_ANALYTIQUE_PROFONDEUR_2']

# Supprimons les lignes avec des valeurs nulles ou 0 dans la colonne "réalisé total"
df_retraiter = df_retraiter[df_retraiter['Réalisé total'].notna() & (df_retraiter['Réalisé total'] != 0)]

# Filtrons les colonnes nécessaires
df_retraiter_filtered = df_retraiter[colonnes_necessaires]
# Supprimer les lignes où toutes les valeurs sont NaN
df_retraiter_filtered.dropna(how='all', inplace=True)
print("\nDonnées après filtrage et nettoyage:")
print(df_retraiter_filtered.head())

# Renommons les colonnes pour correspondre au format final
df_retraiter_filtered.rename(columns={
    'Réalisé total': 'REALISE TOTAL'
}, inplace=True)

print("\nDonnées après renommage des colonnes:")
print(df_retraiter_filtered.head())

#on remarques que les données de la colonnes Fonction =Fonction_Parent
df_retraiter_filtered['FONCTION_PARENT'] = df_retraiter_filtered['FONCTION']

# Ajoutons les colonnes manquantes avec des valeurs par défaut
colonnes_manquantes = set(df_format.columns) - set(df_retraiter_filtered.columns)
for colonne in colonnes_manquantes:
    df_retraiter_filtered[colonne] = None

# Réorganisons les colonnes pour correspondre à l'ordre du fichier Format.csv
df_retraiter_final = df_retraiter_filtered[df_format.columns]

# Remplir la colonne CLE avec les valeurs concaténées de SECTION, CHAPITRE, et ARTICLE
df_retraiter_final['CLE'] = df_retraiter['Section '].astype(str) + '/' + df_retraiter['CHAPITRE'].astype(str) + '/' + df_retraiter['ARTICLE'].astype(str)


print("\nDonnées finales prêtes à être exportées:")
print(df_retraiter_final.head())
df_retraiter_final.dropna(how='all', inplace=True)

# Exportons les données retraitées
df_retraiter_final.to_csv("A_retraiter_Format.csv", index=False, encoding='latin-1', sep=';')
df_retraiter_final.to_excel('A_retraiters_Format.xlsx')
#Analyse des données et créer des visualisations en fonction de nos besoins
#------------------------- Statistiques descriptives--------------------------------------------
statistiques = df_retraiter_final.describe()
print("\nStatistiques descriptives:")
print(statistiques)
 























