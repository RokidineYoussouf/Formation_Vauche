# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 10:17:14 2024

@author: yrd
"""


###########################--------------------------Simulation 1---------------------------------------------------
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

excel_path = 'BDD.xlsx'
df = pd.read_excel(excel_path)

df_selected1 = df[['ID_carac_3', 'Sous-catégorie', 'Masse nette (kg)', '% éch.']].iloc[780:1224].dropna()
#df_selected1 = pd.concat([df_selected1,df_selected1,df_selected1])
df_selected1[['% éch.', 'Masse nette (kg)']] = df_selected1[['% éch.', 'Masse nette (kg)']].apply(pd.to_numeric, errors='coerce')
num_bacs = 12
num_categories = num_bacs
N = 1666360.00  # Masse totale disponible en kg pour l'ensemble du mois de décembre

mu_i = df_selected1.groupby('Sous-catégorie')['Masse nette (kg)'].mean()
p = df_selected1.groupby('Sous-catégorie')['% éch.'].mean()[:num_categories].values

# Multiplier par 1.5 pour les catégories "EMR" et "ELA
#categories_to_multiply = ["EMR", "ELA","Aluminiums","Papiers (1.11)","ELA","PET Clair Bouteilles / flacons","Refus"]
categories_to_multiply = ["EMR", "Papiers (1.11)","Acier","ELA"]
mu_i.loc[categories_to_multiply] = mu_i.loc[categories_to_multiply] * 2.5


#mu_i = df_selected2.groupby('Sous-catégorie')['Masse nette (kg)'].apply(lambda x: x.nlargest(3).mean()).values
#p = df_selected2.groupby('Sous-catégorie')['% éch.'].apply(lambda x: x.nlargest(3).mean()).values
mu = np.sum(mu_i * p)

# Niveaux de confiance et tailles d'échantillon à tester
confidence_level = 0.95 
z_value = stats.norm.ppf((1 + confidence_level) / 2)
#tailles_echantillon =[1147, 1652, 2052, 5233,6147, 9233, 1666360.00] # Tailles d'échantillon
points_fixes = np.array([1150,83319]) # 50121, 83319
# Génération des points supplémentaires entre 105000 et N, excluant 105000 puisqu'il est déjà inclus
points_supplementaires = np.linspace(100000, N, num=1)[1:]  # Ajustez le 'num' selon le nombre de points désirés
# Concaténation des deux séries de points
points_abscisse = np.concatenate((points_fixes, points_supplementaires))

etiquettes_x = [f"{int(x)}kg ({(x/N*100):.2f}%)" for x in points_abscisse]  # Etiquettes personnalisées
categories = df_selected1['Sous-catégorie'].unique()[:num_categories]
categories = np.sort(categories)

# Simulation
num_simulations = 10  # Nombre de simulations à effectuer
all_theta_hats = np.zeros((num_simulations, len(points_abscisse), len(categories), num_bacs))
all_ci_lowers = np.zeros_like(all_theta_hats)
all_ci_uppers = np.zeros_like(all_theta_hats)

# Simulation pour chaque taille d'échantillon
for sim in range(num_simulations):
    for n_idx, n in enumerate(points_abscisse):
        cov_matrix = np.zeros((num_categories, num_categories))
        for i in range(num_categories):
            for j in range(num_categories):
                if i == j:
                    cov_matrix[i, j] = (p[i] * mu_i[i]**2)/mu**2
                else:
                    cov_matrix[i, j] = (-p[i] * p[j] * mu_i[i] * mu_i[j])/mu**2
        cov_matrix /= n
        Z = np.random.multivariate_normal(np.zeros(len(categories)), cov_matrix, size=num_bacs)

        for i in range(len(categories)):
            for j in range(num_bacs):
                numerator = mu_i[i] * p[i] + mu * Z[j, i]
                denominator = mu * (1 + np.sum(Z[j, :]))
                theta_hat = numerator / denominator if denominator > 0 else 0

                std_error = np.sqrt((theta_hat * (1 - theta_hat)) / n)
                ci_lower = theta_hat - stats.norm.ppf(0.975) * std_error
                ci_upper = theta_hat + stats.norm.ppf(0.975) * std_error

                all_theta_hats[sim, n_idx, i, j] = theta_hat
                all_ci_lowers[sim, n_idx, i, j] = ci_lower
                all_ci_uppers[sim, n_idx, i, j] = ci_upper

# Calcul des moyennes des résultats de la simulation
mean_theta_hats = all_theta_hats.mean(axis=0)
mean_ci_lowers = all_ci_lowers.mean(axis=0)
mean_ci_uppers = all_ci_uppers.mean(axis=0)

# Affichage des résultats pour chaque taille d'échantillon et chaque catégorie
print(f"Résultats moyens après {num_simulations} simulations :\n{'-' * 60}")
for n_idx, n in enumerate(points_abscisse):
    pct = (n / N) * 100
    print(f"Taille d'échantillon = {n}kg ({pct:.2f}%)")
    for i, category in enumerate(categories):
        for j in range(num_bacs):
            print(f" {category}, Bac {j+1}: Estimateur = {mean_theta_hats[n_idx, i, j]:.4f}, "
                  f"IC = [{mean_ci_lowers[n_idx, i, j]:.4f}, {mean_ci_uppers[n_idx, i, j]:.4f}]")
    print('-' * 60)

"""
# Tracé des graphiques pour chaque catégorie
for i, category in enumerate(categories):
    plt.figure(figsize=(12, 6))
    
    # Calcul des moyennes des bornes inférieures et supérieures pour chaque taille d'échantillon
    mean_ci_lower = mean_ci_lowers[:, i, :].mean(axis=1)
    mean_ci_upper = mean_ci_uppers[:, i, :].mean(axis=1)
    
    # Tracé de l'intervalle de confiance moyen
    plt.fill_between(points_abscisse, mean_ci_lower, mean_ci_upper, color='purple', alpha=0.3, label=f'IC moyen pour {category}')
    plt.plot(points_abscisse, mean_ci_lower, '-o', color='red', label='Borne inférieure moyenne')
    plt.plot(points_abscisse, mean_ci_upper, '-o', color='blue', label='Borne supérieure moyenne')

    # Configuration du graphique
    plt.title(f'Intervalle de confiance moyen pour {category} avec la taille de l\'échantillon')
    plt.xlabel('Taille de l\'échantillon (kg & %)(Simulation)')
    plt.ylabel('Intervalle de confiance (Dec_21)')
    plt.legend()
    plt.grid(True)
    plt.xticks(points_abscisse, etiquettes_x, rotation=45)
    
    # Ajout des étiquettes de taux de confiance pour chaque point d'abscisse
    for x in points_abscisse:
        idx = (np.abs(points_abscisse - x)).argmin()
        marge_erreur = (mean_ci_upper[idx] - mean_ci_lower[idx]) / 2
        # Affichage de la marge d'erreur
        taux_confiance = 100 - (marge_erreur / ((mean_ci_upper[idx] + mean_ci_lower[idx]) ) * 100)
       # Affichage du taux de confiance
        plt.text(x, mean_ci_upper[idx], f"{taux_confiance:.2f}%", ha='center', va='bottom', fontsize=8, color='black')
       
    plt.show()"""

import matplotlib.pyplot as plt
import numpy as np

# Initialisation des variables nécessaires
num_simulations = 5
num_categories = len(categories)
num_bacs = 12
global_confidence_rates = []

# Boucle sur chaque point d'abscisse pour calculer le taux de confiance global
for n_idx, n in enumerate(points_abscisse):
    # Calcul de la marge d'erreur pour ce point sur toutes les simulations, catégories et bacs
    marge_erreur = (all_ci_uppers[:, n_idx, :, :] - all_ci_lowers[:, n_idx, :, :]) / 2

    # Calcul du taux de confiance pour ce point
    taux_confiance = 100 - (np.mean(marge_erreur) / (np.mean(all_ci_uppers[:, n_idx, :, :]) + np.mean(all_ci_lowers[:, n_idx, :, :])) * 100)
    global_confidence_rates.append(taux_confiance)

# Tracer le taux de confiance global pour chaque point d'abscisse
plt.figure(figsize=(12, 6))
plt.plot(points_abscisse, global_confidence_rates, '-o', color='green', label='Taux de confiance global')

# Configuration du graphique
plt.title('Taux de confiance global en fonction de la taille de l\'échantillon')
plt.xlabel('Taille de l\'échantillon (kg & %) dec_21')
plt.ylabel('Taux de confiance global (%)')
plt.legend()
plt.grid(True)
plt.xticks(points_abscisse, etiquettes_x, rotation=45)
plt.ylim(90 ,100)  # Vous pouvez ajuster ces limites en fonction de vos données

plt.show()


######################

"""
from scipy.interpolate import interp1d
# Taux de confiance existants et leurs tailles d'échantillon correspondantes
taux_confiance = np.array(global_confidence_rates)
tailles_echantillon = np.array(points_abscisse)

# Création de la fonction d'interpolation
interpolate = interp1d(taux_confiance, tailles_echantillon, kind='linear', fill_value="extrapolate")

# Estimation de la taille d'échantillon pour un taux de confiance de 94%
taille_echantillon_94 = interpolate(97)
taille_echantillon_96 = interpolate(98)

# Ajouter ce point au graphique
plt.figure(figsize=(12, 6))
plt.plot(tailles_echantillon, taux_confiance, '-o', color='green', label='Taux de confiance global')
plt.scatter(taille_echantillon_94, 97, color='blue', label='')  # Point ajouté
plt.scatter(taille_echantillon_96, 98, color='blue', label='')  # Point ajouté


# Ajout d'une annotation
#plt.text(taille_echantillon_94, 94, f'{taille_echantillon_94:.0f}kg ({(taille_echantillon_94/N*100):.2f}%)', color='red')
# Ajout des annotations pour chaque point d'abscisse
for x, y in zip(points_abscisse, global_confidence_rates):
    plt.text(x, y, f'{y:.2f}%', color='blue', ha='center', va='bottom')
# Configuration du graphique
plt.title('Taux de confiance global en fonction de la taille de l\'échantillon')
plt.xlabel('Taille de l\'échantillon (kg & %) Dec_21',color='orange')
plt.ylabel('Taux de confiance global (%)',color='blue')
plt.legend()
plt.grid(True)
plt.xticks(np.append(tailles_echantillon, (taille_echantillon_94,taille_echantillon_96)), [f"{int(x)}kg ({(x/N*100):.2f}%)" for x in np.append(tailles_echantillon, (taille_echantillon_94,taille_echantillon_96))], rotation=45)
plt.ylim(90, 100)
plt.text(np.max(points_abscisse)*0.25, 98.1, "Entre 0.07 % à 1.0 %", fontsize=14, color='orange')

plt.show()"""

################

import matplotlib.pyplot as plt
import numpy as np

# ... (votre code existant pour le chargement des données, la simulation, etc.) 

# Calcul des taux de confiance pour chaque catégorie
confidence_rates_per_category = np.zeros((len(points_abscisse), len(categories)))

for n_idx, n in enumerate(points_abscisse):
    for i, category in enumerate(categories):
        marge_erreur = (all_ci_uppers[:, n_idx, i, :].mean(axis=1) - all_ci_lowers[:, n_idx, i, :].mean(axis=1)) / 2
        taux_confiance = 100 - (marge_erreur / ((all_ci_uppers[:, n_idx, i, :].mean(axis=1) + all_ci_lowers[:, n_idx, i, :].mean(axis=1))) * 100)
        confidence_rates_per_category[n_idx, i] = taux_confiance.mean() 

# Tracé des taux de confiance pour chaque catégorie
plt.figure(figsize=(12, 6))

for i, category in enumerate(categories):
    plt.plot(points_abscisse, confidence_rates_per_category[:, i], '-o', label=f'{category}')

# Configuration du graphique
plt.title('Taux de confiance pour chaque catégorie en fonction de la taille de l\'échantillon')
plt.xlabel('Taille de l\'échantillon (kg & %) dec_21')
plt.ylabel('Taux de confiance (%)')
plt.legend()
plt.grid(True)
plt.xticks(points_abscisse, etiquettes_x, rotation=45)
plt.ylim(80, 100)  # Ajustez ces limites en fonction de vos données

plt.show()

#################

import matplotlib.pyplot as plt
import numpy as np

# ... (votre code existant pour le chargement des données, la simulation, etc.)

# Calcul des taux de confiance moyens pour chaque catégorie
mean_confidence_rates = confidence_rates_per_category.mean(axis=0)

# Tri des catégories par taux de confiance moyen décroissant
sorted_categories = np.argsort(mean_confidence_rates)[::-1]

# Création des figures et des sous-graphiques
for i in range(3):  # Boucle sur les 3 figures
    start_idx = i * 4
    end_idx = (i + 1) * 4

    plt.figure(figsize=(12, 6))  # Création d'une nouvelle figure pour chaque groupe de 4 catégories

    for j in range(start_idx, end_idx):  # Boucle sur les 4 catégories
        category_idx = sorted_categories[j]
        category_name = categories[category_idx]
        plt.plot(points_abscisse, confidence_rates_per_category[:, category_idx], '-o', label=f'{category_name}')

    plt.title(f'Taux de confiance - Top {start_idx+1}-{end_idx} catégories', fontsize=12)
    plt.xlabel('Taille de l\'échantillon (kg & %) dec_21', fontsize=10)
    plt.ylabel('Taux de confiance (%)', fontsize=10)
    plt.legend()
    plt.grid(True)
    plt.xticks(points_abscisse, etiquettes_x, rotation=45)
    plt.ylim(70, 100)  # Ajustez ces limites en fonction de vos données

    plt.show()  # Affichage de la figure actuelle avant de passer à la suivante


###################fin



import matplotlib.pyplot as plt
import numpy as np

# ... (votre code existant pour le chargement des données, la simulation, etc.)

# Calcul des taux de confiance moyens pour chaque catégorie
mean_confidence_rates = confidence_rates_per_category.mean(axis=0)

# Tri des catégories par taux de confiance moyen décroissant
sorted_categories = np.argsort(mean_confidence_rates)[::-1]

# Création des figures et des sous-graphiques
fig, axes = plt.subplots(3, 1, figsize=(12, 18))  # 3 figures, 1 colonne

for i in range(3):  # Boucle sur les 3 figures
    start_idx = i * 4
    end_idx = (i + 1) * 4

    for j in range(start_idx, end_idx):  # Boucle sur les 4 catégories
        category_idx = sorted_categories[j]
        category_name = categories[category_idx]
        axes[i].plot(points_abscisse, confidence_rates_per_category[:, category_idx], '-o', label=f'{category_name}')

    axes[i].set_title(f'Taux de confiance - Top {start_idx+1}-{end_idx} catégories', fontsize=12)
    axes[i].set_xlabel('Taille de l\'échantillon (kg & %) dec_21', fontsize=10)
    axes[i].set_ylabel('Taux de confiance (%)', fontsize=10)
    axes[i].legend()
    axes[i].grid(True)
    axes[i].set_xticks(points_abscisse)
    axes[i].set_xticklabels(etiquettes_x, rotation=45)
    axes[i].set_ylim(90, 100)  # Ajustez ces limites en fonction de vos données

plt.tight_layout()  # Ajuste automatiquement l'espacement entre les sous-graphiques
plt.show()




import matplotlib.pyplot as plt
import numpy as np

# ... (votre code existant pour le chargement des données, la simulation, etc.)

# Calcul des taux de confiance moyens pour chaque catégorie
mean_confidence_rates = confidence_rates_per_category.mean(axis=0)

# Tri des catégories par taux de confiance moyen décroissant
sorted_categories = np.argsort(mean_confidence_rates)[::-1]

# Création des figures et des sous-graphiques
for i in range(3):  # Boucle sur les 3 figures
    start_idx = i * 4
    end_idx = (i + 1) * 4

    plt.figure(figsize=(12, 6))  # Création d'une nouvelle figure pour chaque groupe de 4 catégories

    for j in range(start_idx, end_idx):  # Boucle sur les 4 catégories
        category_idx = sorted_categories[j]
        category_name = categories[category_idx]
        plt.plot(points_abscisse, confidence_rates_per_category[:, category_idx], '-o', label=f'{category_name}')

    plt.title(f'Taux de confiance - Top {start_idx+1}-{end_idx} catégories', fontsize=12)
    plt.xlabel('Taille de l\'échantillon (kg & %) dec_21', fontsize=10)
    plt.ylabel('Taux de confiance (%)', fontsize=10)
    plt.legend()
    plt.grid(True)
    plt.xticks(points_abscisse, etiquettes_x, rotation=45)
    plt.ylim(80, 100)  # Ajustez ces limites en fonction de vos données

    plt.show()  # Affichage de la figure actuelle avant de passer à la suivante



###########################--------------------------Simulation 2---------------------------------------------------
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
excel_path = 'BDD.xlsx'
df = pd.read_excel(excel_path)

df_selected2 = df[['ID_carac_3','Sous-catégorie', 'Masse nette (kg)', '% éch.']].iloc[1260:1692].dropna() # 
df_selected2_al = df[['ID_carac_3','Sous-catégorie', 'Masse nette (kg)', '% éch.']].iloc[1836:1848].dropna() # 
df_selected2 = pd.concat([df_selected2,df_selected2_al])
df_selected2[['% éch.', 'Masse nette (kg)']] = df_selected2[['% éch.', 'Masse nette (kg)']].apply(pd.to_numeric, errors='coerce')
num_bacs = 12
num_categories = num_bacs
N = 2274741.00  # Masse totale disponible en kg pour l'ensemble du mois de décembre

#mu_i =df_selected2.groupby('Sous-catégorie')[[ 'Masse nette (kg)']].mean()[:num_categories].values
p = df_selected2.groupby('Sous-catégorie')['% éch.'].mean()
mu_i = df_selected2.groupby('Sous-catégorie')['Masse nette (kg)'].mean()

categories_to_multiply = ["PET Clair Bouteilles / flacons","Papiers (1.11)"]
mu_i.loc[categories_to_multiply] = mu_i.loc[categories_to_multiply] * 2

#mu_i = df_selected2.groupby('Sous-catégorie')['Masse nette (kg)'].apply(lambda x: x.nlargest(3).mean()).values
#p = df_selected2.groupby('Sous-catégorie')['% éch.'].apply(lambda x: x.nlargest(3).mean()).values
mu = np.sum(mu_i * p)

# Niveaux de confiance et tailles d'échantillon à tester
confidence_level = 0.95
z_value = stats.norm.ppf((1 + confidence_level) / 2)
#Ttailles_echantillon =  np.linspace(1150.84, N, num=20) # Tailles d'échantillon
categories = df_selected2['Sous-catégorie'].unique()[:num_categories]
categories = np.sort(categories)

points_fixes = np.array([2150,22747]) #  116304
# Génération des points supplémentaires entre 105000 et N, excluant 105000 puisqu'il est déjà inclus
points_supplementaires = np.linspace(150000, N, num=1)[1:]  # Ajustez le 'num' selon le nombre de points désirés
# Concaténation des deux séries de points
points_abscisse = np.concatenate((points_fixes, points_supplementaires))
# Simulation
num_simulations = 10  # Nombre de simulations à effectuer
all_theta_hats = np.zeros((num_simulations, len(points_abscisse), len(categories), num_bacs))
all_ci_lowers = np.zeros_like(all_theta_hats)
all_ci_uppers = np.zeros_like(all_theta_hats)

# Simulation pour chaque taille d'échantillon
for sim in range(num_simulations):
    for n_idx, n in enumerate(points_abscisse):
        cov_matrix = np.zeros((num_categories, num_categories))
        for i in range(num_categories):
            for j in range(num_categories):
                if i == j:
                    cov_matrix[i, j] = (p[i] * mu_i[i]**2)/mu**2
                else:
                    cov_matrix[i, j] = (-p[i] * p[j] * mu_i[i] * mu_i[j])/mu**2
        cov_matrix /= n
        Z = np.random.multivariate_normal(np.zeros(len(categories)), cov_matrix, size=num_bacs)

        for i in range(len(categories)):
            for j in range(num_bacs):
                numerator = mu_i[i] * p[i] + mu * Z[j, i]
                denominator = mu * (1 + np.sum(Z[j, :]))
                theta_hat = numerator / denominator if denominator > 0 else 0

                std_error = np.sqrt((theta_hat * (1 - theta_hat)) / n)
                ci_lower = theta_hat - stats.norm.ppf(0.975) * std_error
                ci_upper = theta_hat + stats.norm.ppf(0.975) * std_error

                all_theta_hats[sim, n_idx, i, j] = theta_hat
                all_ci_lowers[sim, n_idx, i, j] = ci_lower
                all_ci_uppers[sim, n_idx, i, j] = ci_upper

# Calcul des moyennes des résultats de la simulation
mean_theta_hats = all_theta_hats.mean(axis=0)
mean_ci_lowers = all_ci_lowers.mean(axis=0)
mean_ci_uppers = all_ci_uppers.mean(axis=0)

# Affichage des résultats pour chaque taille d'échantillon et chaque catégorie
print(f"Résultats moyens après {num_simulations} simulations :\n{'-' * 60}")
for n_idx, n in enumerate(points_abscisse):
    pct = (n / N) * 100
    print(f"Taille d'échantillon = {n}kg ({pct:.2f}%)")
    for i, category in enumerate(categories):
        for j in range(num_bacs):
            print(f" {category}, Bac {j+1}: Estimateur = {mean_theta_hats[n_idx, i, j]:.4f}, "
                  f"IC = [{mean_ci_lowers[n_idx, i, j]:.4f}, {mean_ci_uppers[n_idx, i, j]:.4f}]")
    print('-' * 60)


# Définir les points d'abscisse et les étiquettes personnalisées
# = np.linspace(1150.84, N, num=20)  # 8 points répartis régulièrement de 1147 à N
etiquettes_x = [f"{int(x)}kg ({(x/N*100):.2f}%)" for x in points_abscisse]  # Etiquettes personnalisées
"""
# Tracé des graphiques pour chaque catégorie
for i, category in enumerate(categories):
    plt.figure(figsize=(12, 6))
    
    # Calcul des moyennes des bornes inférieures et supérieures pour chaque taille d'échantillon
    mean_ci_lower = mean_ci_lowers[:, i, :].mean(axis=1)
    mean_ci_upper = mean_ci_uppers[:, i, :].mean(axis=1)
    
    # Tracé de l'intervalle de confiance moyen
    plt.fill_between(points_abscisse, mean_ci_lower, mean_ci_upper, color='purple', alpha=0.3, label=f'IC moyen pour {category}')
    plt.plot(points_abscisse, mean_ci_lower, '-o', color='red', label='Borne inférieure moyenne')
    plt.plot(points_abscisse, mean_ci_upper, '-o', color='blue', label='Borne supérieure moyenne')

    # Configuration du graphique
    plt.title(f'Intervalle de confiance moyen pour {category} avec la taille de l\'échantillon')
    plt.xlabel('Taille de l\'échantillon (kg & %)(Simulation)')
    plt.ylabel('Intervalle de confiance (Jan_22)')
    plt.legend()
    plt.grid(True)
    plt.xticks(points_abscisse, etiquettes_x, rotation=45)
    
    # Ajout des étiquettes de taux de confiance pour chaque point d'abscisse
    for x in points_abscisse:
        idx = (np.abs(points_abscisse-x)).argmin()
        marge_erreur = (mean_ci_upper[idx] - mean_ci_lower[idx]) / 2
        # Affichage de la marge d'erreur
        taux_confiance = 100 - (marge_erreur / ((mean_ci_upper[idx] + mean_ci_lower[idx]) ) * 100)
       # Affichage du taux de confiance
        plt.text(x, mean_ci_upper[idx], f"{taux_confiance:.2f}%", ha='center', va='bottom', fontsize=8, color='black')
       
    plt.show()"""

import matplotlib.pyplot as plt
import numpy as np

# Initialisation des variables nécessaires
num_simulations = 10
num_categories = len(categories)
num_bacs = 12
global_confidence_rates = []

# Boucle sur chaque point d'abscisse pour calculer le taux de confiance global
for n_idx, n in enumerate(points_abscisse):
    # Calcul de la marge d'erreur pour ce point sur toutes les simulations, catégories et bacs
    marge_erreur = (all_ci_uppers[:, n_idx, :, :] - all_ci_lowers[:, n_idx, :, :]) / 2

    # Calcul du taux de confiance pour ce point
    taux_confiance = 100 - (np.mean(marge_erreur) / (np.mean(all_ci_uppers[:, n_idx, :, :]) + np.mean(all_ci_lowers[:, n_idx, :, :])) * 100)
    global_confidence_rates.append(taux_confiance)

# Tracer le taux de confiance global pour chaque point d'abscisse
plt.figure(figsize=(12, 6))
plt.plot(points_abscisse, global_confidence_rates, '-o', color='green', label='Taux de confiance global')

# Configuration du graphique
plt.title('Taux de confiance global en fonction de la taille de l\'échantillon')
plt.xlabel('Taille de l\'échantillon (kg & %)')
plt.ylabel('Taux de confiance global (%)')
plt.legend()
plt.grid(True)
plt.xticks(points_abscisse, etiquettes_x, rotation=45)
plt.ylim(90,100)  # Vous pouvez ajuster ces limites en fonction de vos données
plt.show()



from scipy.interpolate import interp1d
# Taux de confiance existants et leurs tailles d'échantillon correspondantes
taux_confiance = np.array(global_confidence_rates)
tailles_echantillon = np.array(points_abscisse)

# Création de la fonction d'interpolation
interpolate = interp1d(taux_confiance, tailles_echantillon, kind='linear', fill_value="extrapolate")

# Estimation de la taille d'échantillon pour un taux de confiance de 94%
taille_echantillon_94 = interpolate(98)
taille_echantillon_96 = interpolate(96)

# Ajouter ce point au graphique
plt.figure(figsize=(12, 6))
plt.plot(tailles_echantillon, taux_confiance, '-o', color='green', label='Taux de confiance global')
plt.scatter(taille_echantillon_94, 98, color='blue', label='')  # Point ajouté
plt.scatter(taille_echantillon_96, 96, color='blue', label='')  # Point ajouté


# Ajout d'une annotation
#plt.text(taille_echantillon_94, 94, f'{taille_echantillon_94:.0f}kg ({(taille_echantillon_94/N*100):.2f}%)', color='red')
# Ajout des annotations pour chaque point d'abscisse
for x, y in zip(points_abscisse, global_confidence_rates):
    plt.text(x, y, f'{y:.2f}%', color='blue', ha='center', va='bottom')
# Configuration du graphique
plt.title('Taux de confiance global en fonction de la taille de l\'échantillon')
plt.xlabel('Taille de l\'échantillon (kg & %) Jav_22',color='orange')
plt.ylabel('Taux de confiance global (%)',color='blue')
plt.legend()
plt.grid(True)
plt.xticks(np.append(tailles_echantillon, (taille_echantillon_94,taille_echantillon_96)), [f"{int(x)}kg ({(x/N*100):.2f}%)" for x in np.append(tailles_echantillon, (taille_echantillon_94,taille_echantillon_96))], rotation=45)
plt.ylim(90, 100)
plt.text(np.max(points_abscisse)*0.2, 98.2, "Entre 0.09 % à 1.0 %", fontsize=13, color='orange')

plt.show()


################
import matplotlib.pyplot as plt
import numpy as np

# ... (votre code existant pour le chargement des données, la simulation, etc.) 

# Calcul des taux de confiance pour chaque catégorie
confidence_rates_per_category = np.zeros((len(points_abscisse), len(categories)))

for n_idx, n in enumerate(points_abscisse):
    for i, category in enumerate(categories):
        marge_erreur = (all_ci_uppers[:, n_idx, i, :].mean(axis=1) - all_ci_lowers[:, n_idx, i, :].mean(axis=1)) / 2
        taux_confiance = 100 - (marge_erreur / ((all_ci_uppers[:, n_idx, i, :].mean(axis=1) + all_ci_lowers[:, n_idx, i, :].mean(axis=1))) * 100)
        confidence_rates_per_category[n_idx, i] = taux_confiance.mean() 

# Tracé des taux de confiance pour chaque catégorie
plt.figure(figsize=(12, 6))

for i, category in enumerate(categories):
    plt.plot(points_abscisse, confidence_rates_per_category[:, i], '-o', label=f'{category}')

# Configuration du graphique
plt.title('Taux de confiance pour chaque catégorie en fonction de la taille de l\'échantillon')
plt.xlabel('Taille de l\'échantillon (kg & %) JAV.22')
plt.ylabel('Taux de confiance (%)')
plt.legend()
plt.grid(True)
plt.xticks(points_abscisse, etiquettes_x, rotation=45)
plt.ylim(87, 100)  # Ajustez ces limites en fonction de vos données

plt.show()

#################

import matplotlib.pyplot as plt
import numpy as np

# ... (votre code existant pour le chargement des données, la simulation, etc.)

# Calcul des taux de confiance moyens pour chaque catégorie
mean_confidence_rates = confidence_rates_per_category.mean(axis=0)

# Tri des catégories par taux de confiance moyen décroissant
sorted_categories = np.argsort(mean_confidence_rates)[::-1]

# Création des figures et des sous-graphiques
for i in range(3):  # Boucle sur les 3 figures
    start_idx = i * 4
    end_idx = (i + 1) * 4

    plt.figure(figsize=(12, 6))  # Création d'une nouvelle figure pour chaque groupe de 4 catégories

    for j in range(start_idx, end_idx):  # Boucle sur les 4 catégories
        category_idx = sorted_categories[j]
        category_name = categories[category_idx]
        plt.plot(points_abscisse, confidence_rates_per_category[:, category_idx], '-o', label=f'{category_name}')

    plt.title(f'Taux de confiance - Top {start_idx+1}-{end_idx} catégories', fontsize=12)
    plt.xlabel('Taille de l\'échantillon (kg & %) JAV.22', fontsize=10)
    plt.ylabel('Taux de confiance (%)', fontsize=10)
    plt.legend()
    plt.grid(True)
    plt.xticks(points_abscisse, etiquettes_x, rotation=45)
    plt.ylim(80, 100)  # Ajustez ces limites en fonction de vos données

    plt.show()  # Affichage de la figure actuelle avant de passer à la suivante

###########################--------------------------Simulation 3---------------------------------------------------
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

excel_path = 'BDD.xlsx'
df = pd.read_excel(excel_path)
df_selected3 = df[['ID_carac_3','Sous-catégorie', 'Masse nette (kg)', '% éch.']].iloc[1968:2412].dropna() 
df_selected3[['% éch.', 'Masse nette (kg)']] = df_selected3[['% éch.', 'Masse nette (kg)']].apply(pd.to_numeric, errors='coerce')

num_bacs = 12
num_categories = num_bacs
N = 1986460.00  # Masse totale disponible en kg pour l'ensemble du mois de décembre

#mu_i =df_selected2.groupby('Sous-catégorie')[[ 'Masse nette (kg)']].mean()[:num_categories].values
p = df_selected3.groupby('Sous-catégorie')['% éch.'].mean()
mu_i = df_selected3.groupby('Sous-catégorie')['Masse nette (kg)'].mean()

categories_to_multiply = ["PET Clair Bouteilles / flacons","Papiers (1.11)"]
mu_i.loc[categories_to_multiply] = mu_i.loc[categories_to_multiply] * 2

sum(mu_i)
ech=N/93.360

#mu_i = df_selected2.groupby('Sous-catégorie')['Masse nette (kg)'].apply(lambda x: x.nlargest(3).mean()).values
#p = df_selected2.groupby('Sous-catégorie')['% éch.'].apply(lambda x: x.nlargest(3).mean()).values
mu = np.sum(mu_i * p)

# Niveaux de confiance et tailles d'échantillon à tester
confidence_level = 0.95
z_value = stats.norm.ppf((1 + confidence_level) / 2)
#tailles_echantillon = np.linspace(4242.51, N, num=20)   #  [1242.51, 2052,3562,4662, 5233, 1986460.00] # Tailles d'échantillon
categories = df_selected3['Sous-catégorie'].unique()[:num_categories]
categories = np.sort(categories)

# Définir les points d'abscisse et les étiquettes personnalisées
points_fixes = np.array([1242,18964]) # 29796.9
# Génération des points supplémentaires entre 105000 et N, excluant 105000 puisqu'il est déjà inclus
points_supplementaires = np.linspace(105000, N, num=1)[1:]  # Ajustez le 'num' selon le nombre de points désirés

# Concaténation des deux séries de points
points_abscisse = np.concatenate((points_fixes, points_supplementaires))
# Simulation
num_simulations = 1  # Nombre de simulations à effectuer
all_theta_hats = np.zeros((num_simulations, len(points_abscisse), len(categories), num_bacs))
all_ci_lowers = np.zeros_like(all_theta_hats)
all_ci_uppers = np.zeros_like(all_theta_hats)

# Simulation pour chaque taille d'échantillon
for sim in range(num_simulations):
    for n_idx, n in enumerate(points_abscisse):
        cov_matrix = np.zeros((num_categories, num_categories))
        for i in range(num_categories):
            for j in range(num_categories):
                if i == j:
                    cov_matrix[i, j] = (p[i] * mu_i[i]**2)/mu**2
                else:
                    cov_matrix[i, j] = (-p[i] * p[j] * mu_i[i] * mu_i[j])/mu**2
        cov_matrix /= n
        Z = np.random.multivariate_normal(np.zeros(len(categories)), cov_matrix, size=num_bacs)

        for i in range(len(categories)):
            for j in range(num_bacs):
                numerator = mu_i[i] * p[i] + mu * Z[j, i]
                denominator = mu * (1 + np.sum(Z[j, :]))
                theta_hat = numerator / denominator if denominator > 0 else 0

                std_error = np.sqrt((theta_hat * (1 - theta_hat)) / n)
                ci_lower = theta_hat - stats.norm.ppf(0.975) * std_error
                ci_upper = theta_hat + stats.norm.ppf(0.975) * std_error

                all_theta_hats[sim, n_idx, i, j] = theta_hat
                all_ci_lowers[sim, n_idx, i, j] = ci_lower
                all_ci_uppers[sim, n_idx, i, j] = ci_upper

# Calcul des moyennes des résultats de la simulation
mean_theta_hats = all_theta_hats.mean(axis=0)
mean_ci_lowers = all_ci_lowers.mean(axis=0)
mean_ci_uppers = all_ci_uppers.mean(axis=0)

# Affichage des résultats pour chaque taille d'échantillon et chaque catégorie
print(f"Résultats moyens après {num_simulations} simulations :\n{'-' * 60}")
for n_idx, n in enumerate(points_abscisse):
    pct = (n / N) * 100
    print(f"Taille d'échantillon = {n}kg ({pct:.2f}%)")
    for i, category in enumerate(categories):
        for j in range(num_bacs):
            print(f" {category}, Bac {j+1}: Estimateur = {mean_theta_hats[n_idx, i, j]:.4f}, "
                  f"IC = [{mean_ci_lowers[n_idx, i, j]:.4f}, {mean_ci_uppers[n_idx, i, j]:.4f}]")
    print('-' * 60)


#points_abscisse = np.linspace(1242.51, N, num=8)  # 8 points répartis régulièrement de 1147 à N
#tailles_echantillon=points_abscisse
etiquettes_x = [f"{int(x)}kg ({(x/N*100):.2f}%)" for x in points_abscisse]  # Etiquettes personnalisées
"""
# Tracé des graphiques pour chaque catégorie
for i, category in enumerate(categories):
    plt.figure(figsize=(12, 6))
    
    # Calcul des moyennes des bornes inférieures et supérieures pour chaque taille d'échantillon
    mean_ci_lower = mean_ci_lowers[:, i, :].mean(axis=1)
    mean_ci_upper = mean_ci_uppers[:, i, :].mean(axis=1)
    
    # Tracé de l'intervalle de confiance moyen
    plt.fill_between(points_abscisse, mean_ci_lower, mean_ci_upper, color='purple', alpha=0.3, label=f'IC moyen pour {category}')
    plt.plot(points_abscisse, mean_ci_lower, '-o', color='red', label='Borne inférieure moyenne')
    plt.plot(points_abscisse, mean_ci_upper, '-o', color='blue', label='Borne supérieure moyenne')

    # Configuration du graphique
    plt.title(f'Intervalle de confiance moyen pour {category} en fonction de la taille de l\'échantillon')
    plt.xlabel('Taille de l\'échantillon (kg & %)')
    plt.ylabel('Intervalle de confiance (Fev_22)')
    plt.legend()
    plt.grid(True)
    plt.xticks(points_abscisse, etiquettes_x, rotation=45)
    
    # Ajout des étiquettes de pourcentage de marge d'erreur pour chaque point d'abscisse
    for x in points_abscisse:
        # Trouver l'indice du point d'abscisse le plus proche dans tailles_echantillon
        idx = (np.abs(points_abscisse - x)).argmin()
        # Calcul de la marge d'erreur pour ce point
        marge_erreur = mean_ci_upper[idx] - mean_ci_lower[idx]
        # Calcul du pourcentage de la marge d'erreur
        taux_confiance = 100 - (marge_erreur / ((mean_ci_upper[idx] + mean_ci_lower[idx]))*100)
       # Affichage du taux de confiance
        plt.text(x, mean_ci_upper[idx], f"{taux_confiance:.2f}%", ha='center', va='bottom', fontsize=8, color='black')

    plt.show()"""


import matplotlib.pyplot as plt
import numpy as np

# Initialisation des variables nécessaires
num_simulations = 1
num_categories = len(categories)
num_bacs = 12
global_confidence_rates = []

# Boucle sur chaque point d'abscisse pour calculer le taux de confiance global
for n_idx, n in enumerate(points_abscisse):
    # Calcul de la marge d'erreur pour ce point sur toutes les simulations, catégories et bacs
    marge_erreur = (all_ci_uppers[:, n_idx, :, :] - all_ci_lowers[:, n_idx, :, :]) / 2

    # Calcul du taux de confiance pour ce point
    taux_confiance = 100 - (np.mean(marge_erreur) / (np.mean(all_ci_uppers[:, n_idx, :, :]) + np.mean(all_ci_lowers[:, n_idx, :, :])) * 100)
    global_confidence_rates.append(taux_confiance)

# Tracer le taux de confiance global pour chaque point d'abscisse
plt.figure(figsize=(12, 6))
plt.plot(points_abscisse, global_confidence_rates, '-o', color='green', label='Taux de confiance global')

# Configuration du graphique
plt.title('Taux de confiance global en fonction de la taille de l\'échantillon')
plt.xlabel('Taille de l\'échantillon (kg & %)')
plt.ylabel('Taux de confiance global (%)')
plt.legend()
plt.grid(True)
plt.xticks(points_abscisse, etiquettes_x, rotation=45)
plt.ylim(90, 100)  # Vous pouvez ajuster ces limites en fonction de vos données

plt.show()



from scipy.interpolate import interp1d
# Taux de confiance existants et leurs tailles d'échantillon correspondantes
taux_confiance = np.array(global_confidence_rates)
tailles_echantillon = np.array(points_abscisse)

# Création de la fonction d'interpolation
interpolate = interp1d(taux_confiance, tailles_echantillon, kind='linear', fill_value="extrapolate")

# Estimation de la taille d'échantillon pour un taux de confiance de 94%
taille_echantillon_94 = interpolate(96)
taille_echantillon_96 = interpolate(97.999)

# Ajouter ce point au graphique
plt.figure(figsize=(12, 6))
plt.plot(tailles_echantillon, taux_confiance, '-o', color='green', label='Taux de confiance global')
plt.scatter(taille_echantillon_94, 96, color='blue', label='')  # Point ajouté
plt.scatter(taille_echantillon_96, 97.999, color='blue', label='')  # Point ajouté


# Ajout d'une annotation
#plt.text(taille_echantillon_94, 94, f'{taille_echantillon_94:.0f}kg ({(taille_echantillon_94/N*100):.2f}%)', color='red')
# Ajout des annotations pour chaque point d'abscisse
for x, y in zip(points_abscisse, global_confidence_rates):
    plt.text(x, y, f'{y:.2f}%', color='blue', ha='center', va='bottom')
# Configuration du graphique
plt.title('Taux de confiance global en fonction de la taille de l\'échantillon')
plt.xlabel('Taille de l\'échantillon (kg & %) Fev_22',color='orange')
plt.ylabel('Taux de confiance global (%)',color='blue')
plt.legend()
plt.grid(True)
plt.xticks(np.append(tailles_echantillon, (taille_echantillon_94,taille_echantillon_96)), [f"{int(x)}kg ({(x/N*100):.2f}%)" for x in np.append(tailles_echantillon, (taille_echantillon_94,taille_echantillon_96))], rotation=45)
plt.ylim(90, 100)
plt.text(np.max(points_abscisse)*0.2, 98.2, "Entre 0.06% à 1%", fontsize=15, color='orange')

plt.show()

################ partie2
import matplotlib.pyplot as plt
import numpy as np

# ... (votre code existant pour le chargement des données, la simulation, etc.) 

# Calcul des taux de confiance pour chaque catégorie
confidence_rates_per_category = np.zeros((len(points_abscisse), len(categories)))

for n_idx, n in enumerate(points_abscisse):
    for i, category in enumerate(categories):
        marge_erreur = (all_ci_uppers[:, n_idx, i, :].mean(axis=1) - all_ci_lowers[:, n_idx, i, :].mean(axis=1)) / 2
        taux_confiance = 100 - (marge_erreur / ((all_ci_uppers[:, n_idx, i, :].mean(axis=1) + all_ci_lowers[:, n_idx, i, :].mean(axis=1))) * 100)
        confidence_rates_per_category[n_idx, i] = taux_confiance.mean() 

# Tracé des taux de confiance pour chaque catégorie
plt.figure(figsize=(12, 6))

for i, category in enumerate(categories):
    plt.plot(points_abscisse, confidence_rates_per_category[:, i], '-o', label=f'{category}')

# Configuration du graphique
plt.title('Taux de confiance pour chaque catégorie en fonction de la taille de l\'échantillon')
plt.xlabel('Taille de l\'échantillon (kg & %) FEV.22')
plt.ylabel('Taux de confiance (%)')
plt.legend()
plt.grid(True)
plt.xticks(points_abscisse, etiquettes_x, rotation=45)
plt.ylim(80, 100)  # Ajustez ces limites en fonction de vos données

plt.show()

#################

import matplotlib.pyplot as plt
import numpy as np

# ... (votre code existant pour le chargement des données, la simulation, etc.)

# Calcul des taux de confiance moyens pour chaque catégorie
mean_confidence_rates = confidence_rates_per_category.mean(axis=0)

# Tri des catégories par taux de confiance moyen décroissant
sorted_categories = np.argsort(mean_confidence_rates)[::-1]

# Création des figures et des sous-graphiques
for i in range(3):  # Boucle sur les 3 figures
    start_idx = i * 4
    end_idx = (i + 1) * 4

    plt.figure(figsize=(12, 6))  # Création d'une nouvelle figure pour chaque groupe de 4 catégories

    for j in range(start_idx, end_idx):  # Boucle sur les 4 catégories
        category_idx = sorted_categories[j]
        category_name = categories[category_idx]
        plt.plot(points_abscisse, confidence_rates_per_category[:, category_idx], '-o', label=f'{category_name}')

    plt.title(f'Taux de confiance - Top {start_idx+1}-{end_idx} catégories', fontsize=12)
    plt.xlabel('Taille de l\'échantillon (kg & %) FEV.22', fontsize=10)
    plt.ylabel('Taux de confiance (%)', fontsize=10)
    plt.legend()
    plt.grid(True)
    plt.xticks(points_abscisse, etiquettes_x, rotation=45)
    plt.ylim(78, 100)  # Ajustez ces limites en fonction de vos données

    plt.show()  # Affichage de la figure actuelle avant de passer à la suivante



#finn












import matplotlib.pyplot as plt
import numpy as np

# Définir la largeur initiale pour le calcul de la variation du taux de confiance
initial_widths = np.array([mean_ci_uppers[0, i, :].mean() - mean_ci_lowers[0, i, :].mean() for i in range(len(categories))])

for i, category in enumerate(categories):
    plt.figure(figsize=(12, 6))

    # Calculer la largeur de l'intervalle de confiance pour cette catégorie à chaque taille d'échantillon
    ci_widths_category = mean_ci_uppers[:, i, :] - mean_ci_lowers[:, i, :]
    mean_width_category = ci_widths_category.mean(axis=1)  # Moyenne sur tous les bacs pour chaque taille d'échantillon

    # Calculer le taux de confiance comme la réduction relative de la largeur de l'IC par rapport à la première mesure
    confidence_rates = 100 * (1 - mean_width_category / initial_widths[i])

    # Tracer la variation du taux de confiance pour la catégorie actuelle
    plt.plot(points_abscisse, confidence_rates, '-o', color='green', label=f'Taux de confiance pour {category}')

    # Configuration du graphique
    plt.title(f'Variation du taux de confiance pour {category}')
    plt.xlabel('Taille de l\'échantillon (kg)')
    plt.ylabel('Taux de confiance (%)')                                                                                                                                                             
    plt.grid(True)
    plt.legend()
    plt.ylim(60, 105)  # Limiter l'échelle de l'ordonnée de 80 à 100

    plt.xticks(points_abscisse, [f"{int(x)}kg ({(x/N*100):.2f}%)" for x in points_abscisse], rotation=45)
    plt.show()


import matplotlib.pyplot as plt
import numpy as np

# Étape 1: Calcul de la largeur initiale moyenne globale
initial_widths_global =np.mean([mean_ci_uppers[0, :, :].mean() - mean_ci_lowers[0, :, :].mean()])

# Étape 2: Calcul des largeurs moyennes pour chaque taille d'échantillon
global_ci_widths = mean_ci_uppers - mean_ci_lowers
mean_global_widths = global_ci_widths.mean(axis=(1, 2))  # Moyenne sur toutes les catégories et tous les bacs

# Étape 3: Calcul du taux de confiance ajusté
confidence_rates_global = 100 * (1 - mean_global_widths / initial_widths_global)

# Étape 4: Tracer la variation du taux de confiance ajusté
plt.figure(figsize=(12, 6))
plt.plot(points_abscisse, confidence_rates_global, '-o', color='blue', label='Taux de confiance global')

# Configuration du graphique
plt.title('Variation du taux de confiance global')
plt.xlabel('Taille de l\'échantillon (kg)')
plt.ylabel('Taux de confiance ajusté (%)')
plt.grid(True)
plt.legend()
plt.ylim(60, 105)  # Ajuster les limites de l'ordonnée comme nécessaire

plt.xticks(points_abscisse, [f"{int(x)}kg ({(x/N*100):.2f}%)" for x in points_abscisse], rotation=45)
plt.show()



import matplotlib.pyplot as plt
import numpy as np

# Préparation des données pour le graphique de la variation du taux de confiance global
mean_global_ci_lower = mean_ci_lowers.mean(axis=(1, 2))  # Moyenne globale des bornes inférieures
mean_global_ci_upper = mean_ci_uppers.mean(axis=(1, 2))  # Moyenne globale des bornes supérieures
initial_global_ci_width = mean_global_ci_upper[0] - mean_global_ci_lower[0]  # Largeur initiale globale de l'IC

# Calcul du taux de confiance global ajusté
global_confidence_rates = 100 * (1 - (mean_global_ci_upper - mean_global_ci_lower) / initial_global_ci_width)

# Affichage du graphique
plt.figure(figsize=(12, 6))
plt.plot(points_abscisse, global_confidence_rates, '-o', color='blue', label='Taux de confiance global')

# Configuration du graphique
plt.title('Variation du taux de confiance global en fonction de la taille de l\'échantillon')
plt.xlabel('Taille de l\'échantillon (kg & %)')
plt.ylabel('Taux de confiance global (%)')
plt.grid(True)
plt.legend()
plt.xticks(points_abscisse, [f"{int(x)}kg ({(x/N*100):.2f}%)" for x in points_abscisse], rotation=45)

# Limitation de l'échelle de l'ordonnée
plt.ylim(80, 100)  # Vous pouvez ajuster ceci selon les données et les taux de confiance réels

plt.show()
