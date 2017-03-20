#coding: utf-8

### MES COMMENTAIRES ET CORRECTIONS SONT MARQUÉS PAR TROIS DIÈSES

### Il manquait le suffixe .py à ton script...

# NE PAS OUBLIER DE CRÉER L'ENVIRONNEMENT VIRTUEL

# Tout ce qui est écrit ci-bas est basé sur les directives inscrites dans le syllabus edm5240

import csv
import requests
from bs4 import BeautifulSoup

# Je voulais savoir les contrats récents en matière d'environnement
# Avoir le tout sur une seule page
url1 = "http://www.ec.gc.ca/gc-sc/index.cfm?lang=Fr&state=quarter&quarter=3&fiscal=2016%2F2017"

# Nom du fichier .csv
fich = "contrats-environnement-JHR.csv" ### J'ai ajouté «JHR» au nom du CSV pour le reconnaître

# Toujours se présenter quand on fait une requête

### Excellent!
### Le site d'Environnement Canada, cependant, était capricieux et bloquait les requêtes automatisées après quelques secondes.
### J'ai ajouté différentes entêtes.
### C'est le COOKIE qui a débloqué ce site.
### Cela m'a incité à ajouter une nouvelle page à mon document sur BeautifulSoup.
### La nouvelle version est disponible à la même URL: http://bit.ly/jhroybs4

entetes = {
	# "User-Agent":"Genevieve Jette - Requête envoyée dans le cadre d'un cours de journalisme informatique à l'UQAM (EDM5240)",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36",
	"From":"genevieve.jette1@gmail.com",
    "Connection":"Keep-Alive",
    "Referer":"http://www.ec.gc.ca/gc-sc/index.cfm?lang=Fr&state=quarter&quarter=3&fiscal=2016%2F2017",
    "Cookie":"ARPT=XQIRQLS10.30.105.10CKMKM; WT_FPC=id=210e23ea7315559b1cc1489884433101:lv=1489884437012:ss=1489884433101"
}

# Le contenu, c'est demander ce qu'on veut en cherchant dans le contenu de l'url (donc sur le site)
# tout en se présentant
contenu = requests.get(url1, headers=entetes)

# La page, c'est BeautifulSoup qui va faire le moissonnage de notre contenu
# Puis va lire du html grâce à parser
page = BeautifulSoup(contenu.text,"html.parser")
# print(page)

i = 0

# On va faire une loop qui va extraire les données de chaque url
# Au sein de notre premier url
for ligne in page.find_all("tr"):
    if i != 0:
        # print(ligne)
        
        lien = ligne.a.get("href")
        # print(lien)
        
        # Tous les autres liens dans la page d'url1 a ce début de « phrase » dans leur url 
        hyperlien = "http://www.ec.gc.ca/gc-sc/" + lien
        # print(hyperlien)
        
        # Alors, le contenu2 (ce qui se trouve dans comme url dans notre url1)
        # On veut encore une fois lire le html dans leur section
        contenu2 = requests.get(hyperlien, headers=entetes)
        page2 = BeautifulSoup(contenu2.text, "html.parser")
        
        # On le laisse vide parce qu'on va le préciser après
        contrat = []
        
        # Voici la précision! Append va créer une liste (pas en ordre) avec les données recueillies
        contrat.append(hyperlien)
        
        # Ce qu'on veut, c'est un élément dans chaque « ligne » (voir plus haut).
        # C'est pour ça qu'on crée « item » ou « choses »
        # Quand on va dans le code source du site web, on voit « tr » 
        # Parce que la liste d'url dans notre url1, est un « tr »
        # Et on veut trouver les « choses » dans le « tr »
        # Donc on va chercher dedans!
        for choses in page2.find_all("tr"):
            # print(choses)
            
            # Il peut y avoir des cases vides dans notre contenu2
            # On fait un « if » dans les cas où il y a des cases vides

### OUPS! Ici, tu n'as pas changé le nom de la variable. Ce n'est pas «item», mais «choses»
### C'est tout ce qui manquait pour que ça marche! :)

            # if item.td is not None:
            #     contrat.append(item.td.text)
            
            # else:
            #     contrat.append(None)

            if choses.td is not None:
                contrat.append(choses.td.text)
            
            else:
                contrat.append(None)
        
        print(contrat)
        
        # Grâce à ces définitions de variables, on va créer notre fichier .csv
        # Qu'on pourra téléverser dans Excel
        torpinouche = open(fich,"a")
        talonhaut = csv.writer(torpinouche)
        talonhaut.writerow(contrat)
        
    i =+ 1
