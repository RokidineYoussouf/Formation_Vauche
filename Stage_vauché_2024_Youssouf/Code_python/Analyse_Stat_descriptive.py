# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 09:27:42 2024

@author: yrd
"""

import matplotlib.pyplot as plt
import numpy as np

# Données pour les mois en tonnes
data = {
    'Décembre': 1666.360,
    'Janvier': 2326.080,
    'Février': 1986.460
}

# Noms des mois et leurs valeurs respectives en tonnes
months = list(data.keys())
tonnages = list(data.values())

# Couleurs pour chaque segment du camembert
colors = ['#6b486b', '#a05d56', '#d0743c']

# Explosion du segment le plus grand pour le mettre en évidence
explode = (0, 0.1, 0)  # Seulement Janvier est "explosé"

# Fonction pour afficher les tonnages au lieu des pourcentages
def absolute_value(val):
    a = np.round(val/100.*sum(tonnages), 2)
    return f'{a} T'

# Création du graphique à secteurs
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(tonnages, labels=months, autopct=absolute_value, startangle=140,
                                  colors=colors, explode=explode, shadow=True, wedgeprops={'linewidth': 1, 'edgecolor': 'black'})

# Ajout d'effets pour améliorer l'illusion 3D
for w in wedges:
    w.set_edgecolor('yellow')

# Ajout de texte pour chaque segment
for text, autotext in zip(texts, autotexts):
    text.set_color('blue')
    autotext.set_color('white')
    autotext.set_weight('bold')

# Ajouter un titre
plt.title('Répartition des tonnages entrants par mois')

# Affichage du graphique
plt.show()


###########################-----------------------------Stat-Descriptive pour Decembre----------------------------------------------------
#import seaborn as sns
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

excel_path = 'BDD.xlsx'

df = pd.read_excel(excel_path)

df_selected1 = df[['ID_carac_3', 'Sous-catégorie', 'Masse nette (kg)', '% éch.']].iloc[780:1224].dropna()
#df_selected1 = pd.concat([df_selected1,df_selected1,df_selected1,df_selected1,df_selected1,df_selected1,df_selected1,df_selected1,df_selected1,df_selected1,df_selected1,df_selected1,df_selected1,df_selected1,df_selected1,df_selected1,df_selected1,df_selected1,df_selected1,df_selected1,df_selected1])

df_selected1[['% éch.', 'Masse nette (kg)']] = df_selected1[['% éch.', 'Masse nette (kg)']].apply(pd.to_numeric, errors='coerce')
#-------------------------------------------------------------# Statistiques descriptives
# Calcul des statistiques descriptives par sous-catégorie
stats_descriptives1 = df_selected1.groupby('Sous-catégorie')[['% éch.', 'Masse nette (kg)']].agg(['mean', 'median', 'std', 'min', 'max','sum'])
print(stats_descriptives1)
df_selected1_PEBD = df_selected1[df_selected1['ID_carac_3'].str.contains("REFUS")]

sous_categorie_1 = 'sous-catégorie'
df_specific = df_selected1[df_selected1['Sous-catégorie'] == sous_categorie_1]
#plt.figure(figsize=(10, 6))
#sns.boxplot(x='% éch.', y='Sous-catégorie', data=df_selected1)
#plt.title('Boxplot de % éch. par Sous-catégorie')
#plt.show()

stats_descriptives1 = df_selected1.groupby('Sous-catégorie').agg({
    'Masse nette (kg)': ['mean', 'std', 'sum']  # 'size' est le nombre d'observations par sous-catégorie
})
import matplotlib.pyplot as plt

# Supposons que stats_descriptives1 est déjà calculé avec le groupe 'Sous-catégorie' et l'agrégation de 'Masse nette (kg)'
# Vous devez maintenant extraire les sommes pour chaque sous-catégorie
mass_sum = stats_descriptives1[('Masse nette (kg)', 'sum')]

# Noms des sous-catégories
categories = mass_sum.index

# Couleurs pour chaque segment du camembert
colors = ['#6b486b', '#a05d56', '#d0743c', '#ff8c00', '#7b6888', '#9c9ede', '#17becf']

# Création du graphique à secteurs
plt.figure(figsize=(5, 5))
plt.pie(mass_sum, labels=categories, colors=colors, autopct='%1.1f%%', startangle=140)

# Ajouter un titre
plt.title('Répartition de la masse d \'échantillon de Flux Entrant (Dec_21)')

# Afficher le graphique
plt.show()

###########################-----------------------------Stat-Descriptive pour Janvier----------------------------------------------------
#import seaborn as sns
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

excel_path = 'BDD.xlsx'

df = pd.read_excel(excel_path)

df_selected2 = df[['ID_carac_3','Sous-catégorie', 'Masse nette (kg)', '% éch.']].iloc[1260:1692].dropna() # 
df_selected2_al = df[['ID_carac_3','Sous-catégorie', 'Masse nette (kg)', '% éch.']].iloc[1836:1848].dropna() # 
df_selected2 = pd.concat([df_selected2,df_selected2_al])#df_selected2_al = df[['ID_carac_3','Sous-catégorie', 'Masse nette (kg)', '% éch.']].iloc[1836:1848].dropna() # 
#df_selected2 = pd.concat([df_selected2,df_selected2_al])

df_selected2[['% éch.', 'Masse nette (kg)']] = df_selected2[['% éch.', 'Masse nette (kg)']].apply(pd.to_numeric, errors='coerce')
#-------------------------------------------------------------# Statistiques descriptives
# Calcul des statistiques descriptives par sous-catégorie
stats_descriptives2 = df_selected2.groupby('Sous-catégorie')[['% éch.', 'Masse nette (kg)']].agg(['mean', 'median', 'std', 'min', 'max','sum'])
print(stats_descriptives2)
df_selected2_PEBD = df_selected2[df_selected2['ID_carac_3'].str.contains("REFUS")]

sous_categorie_exemple = ' sous-catégorie'
df_specific = df_selected2[df_selected2['Sous-catégorie'] == sous_categorie_exemple]
#plt.figure(figsize=(10, 6))
#sns.boxplot(x='% éch.', y='Sous-catégorie', data=df_selected2)
#plt.title('Boxplot de % éch. par Sous-catégorie')
#plt.show()

stats_descriptives2 = df_selected2.groupby('Sous-catégorie').agg({
    'Masse nette (kg)': ['mean', 'std', 'sum']  # 'size' est le nombre d'observations par sous-catégorie
})
import matplotlib.pyplot as plt

# Supposons que stats_descriptives1 est déjà calculé avec le groupe 'Sous-catégorie' et l'agrégation de 'Masse nette (kg)'
# Vous devez maintenant extraire les sommes pour chaque sous-catégorie
mass_sum2 = stats_descriptives2[('Masse nette (kg)', 'sum')]

# Noms des sous-catégories
categories2 = mass_sum2.index

# Couleurs pour chaque segment du camembert
colors = ['#6b486b', '#a05d56', '#d0743c', '#ff8c00', '#7b6888', '#9c9ede', '#17becf']

# Création du graphique à secteurs
plt.figure(figsize=(5, 5))
plt.pie(mass_sum2, labels=categories2, colors=colors, autopct='%1.1f%%', startangle=140)

# Ajouter un titre
plt.title('Répartition de la masse de l\'échantillon de Flux Entrant (Janv_22)')

# Afficher le graphique
plt.show()

###########################-----------------------------Stat-Descriptive pour Fevrier----------------------------------------------------
#import seaborn as sns
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

excel_path = 'BDD.xlsx'

df = pd.read_excel(excel_path)

df_selected3 = df[['ID_carac_3','Sous-catégorie', 'Masse nette (kg)', '% éch.']].iloc[1968:2412].dropna() 
df_selected3[['% éch.', 'Masse nette (kg)']] = df_selected3[['% éch.', 'Masse nette (kg)']].apply(pd.to_numeric, errors='coerce')
#-------------------------------------------------------------# Statistiques descriptives
# Calcul des statistiques descriptives par sous-catégorie
stats_descriptives3 = df_selected3.groupby('Sous-catégorie')[['% éch.', 'Masse nette (kg)']].agg(['mean', 'median', 'std', 'min', 'max','sum'])
print(stats_descriptives3)
df_selected2_PEBD = df_selected3[df_selected3['ID_carac_3'].str.contains("REFUS")]

sous_categorie_exemple = ' sous-catégorie'
df_specific = df_selected3[df_selected3['Sous-catégorie'] == sous_categorie_exemple]
#plt.figure(figsize=(10, 6))
#sns.boxplot(x='% éch.', y='Sous-catégorie', data=df_selected3)
#plt.title('Boxplot de % éch. par Sous-catégorie')
#plt.show()

stats_descriptives3 = df_selected3.groupby('Sous-catégorie').agg({
    'Masse nette (kg)': ['mean', 'std', 'sum']  # 'size' est le nombre d'observations par sous-catégorie
})
import matplotlib.pyplot as plt

# Supposons que stats_descriptives1 est déjà calculé avec le groupe 'Sous-catégorie' et l'agrégation de 'Masse nette (kg)'
# Vous devez maintenant extraire les sommes pour chaque sous-catégorie
mass_sum3 = stats_descriptives3[('Masse nette (kg)', 'sum')]

# Noms des sous-catégories
categories3 = mass_sum3.index

# Couleurs pour chaque segment du camembert
colors = ['#6b486b', '#a05d56', '#d0743c', '#ff8c00', '#7b6888', '#9c9ede', '#17becf']

# Création du graphique à secteurs
plt.figure(figsize=(5, 5))
plt.pie(mass_sum3, labels=categories3, colors=colors, autopct='%1.1f%%', startangle=140)

# Ajouter un titre
plt.title('Répartition de la masse  de l\'échantillon Flux Entrant(Fev_22)')

# Afficher le graphique
plt.show()
               
###################################-----------------------sortie Vauché decembre 2021 --------------------------------

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

excel_path1 = 'V:\/BDD_sortie.xlsx'

df1 = pd.read_excel(excel_path1)
df1 = df1[41:54].dropna() # mois de Decembre

# Afficher les premières lignes du DataFrame
print(df1.head())
df1 = df1.dropna(how='all')
print(df1.head)
data=df1.iloc[:, ::3+1]
moyennes_par_objet = data.groupby('Unnamed: 0').mean()
# Supposons que le DataFrame 'df1' est déjà chargé et préparé comme décrit précédemment 
data = df1.iloc[:, ::3+1]
moyennes_par_objet = data.groupby('Unnamed: 0').mean()*100
# Tracer les moyennes par objet en utilisant matplotlib directement pour plus de contrôle
plt.figure(figsize=(10, 6))
# plt.bar prend les étiquettes sur l'axe des x et les hauteurs des barres sur l'axe des y
for i in range(12):
    bars = plt.bar(moyennes_par_objet.index, moyennes_par_objet.iloc[:,i])
    plt.title('Moyenne des tris correct par Objet')
    plt.xlabel('Objet en Dec_21')
    plt.ylabel('Moyenne des Valeurs')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Ajouter des étiquettes sur les barres pour les valeurs > 50%
    for bar in bars:
        height = bar.get_height()
        # Modifier ici pour correspondre à votre critère, par exemple > 50% de quelque valeur de référence
        if height > 4:  # Assurez-vous de choisir un seuil approprié
            plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%', ha='center', va='bottom')
plt.show()


#data = data.drop('Unnamed: 0', axis=1)
#data['Somme_Ligne'] = data.sum(axis=1)


###################################-----------------------sortie Vauché Janvier 2022--------------------------------

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

excel_path1 = 'V:\/BDD_sortie.xlsx'

df1 = pd.read_excel(excel_path1)
df1 = df1[83:95].dropna() # mois de Decembre

# Afficher les premières lignes du DataFrame
print(df1.head())
df1 = df1.dropna(how='all')
print(df1.head)
data=df1.iloc[:, ::3+1]
moyennes_par_objet = data.groupby('Unnamed: 0').mean()
# Supposons que le DataFrame 'df1' est déjà chargé et préparé comme décrit précédemment 
data = df1.iloc[:, ::3+1]
moyennes_par_objet = data.groupby('Unnamed: 0').mean()*100
# Tracer les moyennes par objet en utilisant matplotlib directement pour plus de contrôle
plt.figure(figsize=(10, 6))
# plt.bar prend les étiquettes sur l'axe des x et les hauteurs des barres sur l'axe des y
for i in range(12):
    bars = plt.bar(moyennes_par_objet.index, moyennes_par_objet.iloc[:,i])
    plt.title('Moyenne des tris correct par Objet')
    plt.xlabel('Objet en Janv_22')
    plt.ylabel('Moyenne des Valeurs')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Ajouter des étiquettes sur les barres pour les valeurs > 50%
    for bar in bars:
        height = bar.get_height()
        # Modifier ici pour correspondre à votre critère, par exemple > 50% de quelque valeur de référence
        if height > 4:  # Assurez-vous de choisir un seuil approprié
            plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%', ha='center', va='bottom')
plt.show()


#data = data.drop('Unnamed: 0', axis=1)
#data['Somme_Ligne'] = data.sum(axis=1)


###################################-----------------------sortie Vauché Fevrier 2022--------------------------------

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

excel_path1 = 'V:\/BDD_sortie.xlsx'

df1 = pd.read_excel(excel_path1)
df1 = df1[123:135].dropna() # mois de Decembre

# Afficher les premières lignes du DataFrame
print(df1.head())
df1 = df1.dropna(how='all')
print(df1.head)
data=df1.iloc[:, ::3+1]
moyennes_par_objet = data.groupby('Unnamed: 0').mean()
# Supposons que le DataFrame 'df1' est déjà chargé et préparé comme décrit précédemment 
data = df1.iloc[:, ::3+1]
moyennes_par_objet = data.groupby('Unnamed: 0').mean()*100
# Tracer les moyennes par objet en utilisant matplotlib directement pour plus de contrôle
plt.figure(figsize=(10, 6))
# plt.bar prend les étiquettes sur l'axe des x et les hauteurs des barres sur l'axe des y
for i in range(12):
    bars = plt.bar(moyennes_par_objet.index, moyennes_par_objet.iloc[:,i])
    plt.title('Moyenne des tris correct par Objet')
    plt.xlabel('Objet en Fevr_22')
    plt.ylabel('Moyenne des Valeurs')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Ajouter des étiquettes sur les barres pour les valeurs > 50%
    for bar in bars:
        height = bar.get_height()
        # Modifier ici pour correspondre à votre critère, par exemple > 50% de quelque valeur de référence
        if height > 4:  # Assurez-vous de choisir un seuil approprié
            plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%', ha='center', va='bottom')
plt.show()


data = data.drop('Unnamed: 0', axis=1)
data['Somme_Ligne'] = data.sum(axis=1)

################# -------------------------------------------


#----------------------------------------Donner en Tonnage sur le mois du Decembre-------------------
"""
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

excel_path1 = 'V:\/BDD2.xlsx'

df = pd.read_excel(excel_path1)

# Afficher les premières lignes du DataFrame
print(df.head())
df = df.dropna(how='all')
print(df.head)
data=df[['MULT', 'EMB', 'Total']]*1000

# Suppression des lignes vides (toutes les valeurs sont NaN)
df = df.dropna(how='all')

# Vérification que les colonnes nécessaires existent
colonnes_necessaires = ['Type', 'MULT', 'EMB', 'Total']  # Assurez-vous que ces noms correspondent à votre fichier
for col in colonnes_necessaires:
    if col not in df.columns:
        raise ValueError(f"La colonne {col} n'existe pas dans le DataFrame.")

# Regroupement des données par 'Type' et somme des valeurs pour chaque colonne

# Obtention des types pour l'axe des abscisses
types = data.index.tolist()

# Largeur des barres dans le graphique
bar_width = 0.85

# Création d'un graphique en barres empilées
plt.figure(figsize=(12, 8))

# Empilement des barres pour chaque catégorie
plt.bar(types, data['MULT'], width=bar_width, label='MULT', color='blue', alpha=0.7)
plt.bar(types, data['EMB'], width=bar_width, bottom=data['MULT'], label='EMB', color='green', alpha=0.7)

# Ajout des titres et des labels
plt.title('Masses par Type d’Objet')
plt.xlabel('Type d’Objet')
plt.ylabel('Masse')
plt.xticks(rotation=45, ha='right')
plt.legend()

# Ajustement automatique pour tenir compte du layout
plt.tight_layout()

# Affichage du graphique
plt.show()"""


