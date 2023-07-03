# Prise de note pour le pb N°2

Contexte, vérifier si un passage de 7h30 en 12h en EPHAD est judicieux (facteur économique / condition de travail humain)


Objectifs:

 - vérifier si un passage de 7h30 en 12h en EPHAD est judicieux (facteur économique / condition de travail humain)
 - déterminer les hypothèses pour l'élaboration d'une trame:
   - combien de personnes faut-il sur l'équipe ?

Hypothèses:

 - Pas de temps partiel
 - Equipe de 10 personnes actuellement
 - En 7h30: 3 personnes le matin, 2 personnes l'après midi. Idem le weekend.
 - Le travail de nuit n'est pas considéré, c'est une autre équipe actuellement.
 - Les horaires n'ont pas d'incidence sur la réflexion globale.
 - Même hypothèses que pour le CHU à savoir:
   - trame de 12 semaines
 - Les 10 personnes n'ont pas obligatoirement une trame différente.


Réflexion:

------
Temps de travail:

Temps de travail par jour (en journée) actuel:
 - 3 personnes en 7h30 + 2 personnes en 7h30 --> 3x7.5 + 2x7.5 = 37.5 heures chaque jour.
Temps de travail par jour (la nuit) actuel:
 - 1 personnes en 7h30 -> 7.5 heures chaque nuit.

Le temps total de travail sur 24h est donc de 45 heures.
L'idée étant de garder ce temps de travail, jugé nécessaire. En gardant ce temps de travail, l'aspect économique est
également globalement conservé.

Attention, la réflexion actuelle porte uniquement sur le planning de jour. Il n'est pas juste de considérer le nombre
d'heures de jour actuel (en 7h30) vs le nombre d'heures de jour futur (en 12h).
Pourquoi ? Car le planning de jour concerne 2 roulements (ceux du matin et ceux de l'apres midi) alors que le planning
de nuit concerne 1 seul roulement.
Il faut donc faire attention à ne pas comparer les heures de jour actuelle en 7h30 vs les heures de jour futures en 12h
puisque ce serait inexacte.
Il est préférable de regarder le nombre journalière et de conserver ce chiffre, de 7h30 en 12h.

Donc au total, il y a:
 - chaque jour: 45 heures
 - chaque semaine: 315 heures
 - chaque mois (30 jours): 9450 heures

----

En gardant les chiffres ci-dessous:

 - 45 heures / 12 = 3.75.
Il est impossible d'avoir pile poil le bon nombre de personne chaque jour, travaillant en 12h, pour avoir la meme quantité
de travail.

Il y a donc 3 possibilités (dont une probablement éliminée d'office, la 1e):
 - 1e possibilité: Diminuer le nombre de personne / jour.
En passant à 3 personnes chaque jour, on a un chiffre rond de 36h de travail par jour. Il manque 9h de travail.
Cette possibilité semble beaucoup trop contraignante pour le personnel et est éliminée d'office.

 - 2e possibilité: Augmenter le nombre de personne / jour.
En passant à 4 personnes chaque jour, on tombe sur 12 x 4 = 48 heures de travail journalier. Cela rajoute 3h par rapport
au fonctionnement actuel. La différence est suffisamment faible pour être considérée dans le raisonnement (surcout de 3h
chaque jour pour l'hopital mais plus de confort pour les soignants)

 - 3e possibilité: Rester sur un nombre exact de 45h / jour en moyenne:
Pour faire ça, il faut trouver la rotation de personnes qui permet de faire 45h par jour en moyenne.
On peut utiliser en mathématiques le PPCM (plus petit commun dénominateur).
PPCM(45, 12) = 180.
Cela veut dire que 180 heures de travail (Correspondant à 4 jours (180h / 45h = 4 jours)) permet de tomber sur un chiffre
rond de rotation en 12h. (180h / 12h = 15 rotations).
Donc cette 3e possibilités de planning doit respecter la condition de faire travailler 15 personnes en 4 jours soit:
4 + 4 + 4 + 3.


-----------

Exploration de la 2e possibilité:

L'objectif est d'avoir tous les jours 3 personnes et toutes les nuits, 1 personne pour un total de 48h par jour.

---
Note: Cette réflexion ne se soucis pas des horaires de travail mais soyons conscient qu'en EPHAD, le lever se fait autour
de 7h du matin et le coucher vers 21h. Avec 3 personnes travaillant en 12h le jour, on serait à staff équivalent entre
les horaires en 7h30 du matin. En revanche, le soir, le coucher serait fait à 1 seule personne (celle sur le créneau de
nuit, contre 2 actuellement en 7h30). Il y aurait alors peut être des astuces à trouver, des plages horaires de 12h différentes
par exemple).
---

Une personne doit travailler 35h par semaine en moyenne avec un maximum de 48h sur 7 jours glissant.
 12h x 3 jours = 36h.
Le code du travail indique: Quand le cycle de travail prévoit une durée de travail supérieure à 35 heures par semaine, les heures accomplies au-delà de la durée légale donnent droit à des RTT.

On considere donc que l'heure supplémentaire (de 35hh à 36h octroie une heure de RTT).

Le minimum de personnel nécessaire pour une semaine est de:
 - 48h de travail par jour, soit 336h par semaine.
336h / 12h = 28 rotations de 12h.
Une personne peut faire en moyenne 3 rotations de 12h par semaine donc: 28 / 3 = 9.3333.

Il faut à minima 10 personnes (à 100%) pour pour tenir la cadence hors congés.

---
Déroulement des algos pour 10 personnes sur 12 semaines.

- Déroulement du script find_best_combinations avec:
  - 10 personnes sur l'équipe
  - roulement du 12 semaines
  - Chaque personne de l'équipe a une trame différente
  - 3 personnes qui travaillent chaque jour.

-> Le nombre de combinations mathématiques est très faible: 66 possibilités différentes.
ça veut dire que pour une trame donnée de 12 semaines et 10 personnes, il existe 66 façons différentes de construire des trames
pour chaque personne de l'équipe. ça peut paraitre peu mais cela vient du faire que:
 - chaque variante de la trame principale doit commencer un lundi (Donc 12 possibilités différentes de commencer la trame)
 - chaque variante doit respecter l'ordre de la trame. Exemple, une trame de base 'ABCD' ne peut pas donner 'CABD'
 - chaque personne doit avoir une variante différente de son voisin.

En considérant ces 66 combinations possibles par variantes, cela nous donne:
 - 115 000 trames sur 12 semaines possibles
 - 66 variantes sur chacune des trames
 --> Au moins 150 possibilités de planning avec toujours au moins 3 personnes chaque jours:
     Exemple:
        Number of day with 0 person: 0
        Number of day with 1 person: 0
        Number of day with 2 person: 0
        Number of day with 3 person: 26
        Number of day with 4 person: 32
        Number of day with 5 person: 22
        Number of day with 6 person: 4
        Number of day with 7 person: 0
        Number of day with 8 person: 0
        Number of day with 9 person: 0
        Number of day with 10 person: 0


 *****************************
 *****************************
 *****************************

Possibilités d'amélioration de l'algo existant:

 - pruner les trames qui sont similaires dans le temps (ex: ABC est la meme chose que BCA. ACB est différent par contre)

 Pas plus de 4 personnes par week end


6h30 -> 21h
1 personne dans tout le service

3 personnes par jour x 12h
ou
4 personnes par jour en 7h30

37,5h  de temps de travail actuel

Durée de journée de travail:
 - max: 12h
 - min: 7h22 (7,37)

Condition:
 - au moins 1 personne entre 6h30 et à 21h
 - 48h max de travail sur 7 jours glissants
 - En semaine en, le travail est et reste en 7h30.
   Les horaires: 6h30 / 14h30 ... 13h30 / 21H
 - Une journée typique: 3 personnes le matin, 2p l'apres midi
 - Temps partiels dans l'équipe:
     1 personne à 80%
     1 personne à 90%
     2 personnes à 50%
   (Ne pas considérer les temps partiels dans un 1er temps)
 - Le trame ne doit pas faire plus de 12 semaines
 - Un travail le samedi implique le dimanche
 - Si une journée de plus ae 7h30 de travail le weekend, récup le lundi
 - Essayer de ne pas changer d'horaire sur le weekend

 - Le matin un peu plus tendu pour la toilette (comprendre qu'il faut privilégier plus de monde le matin)


Output:
 - Soit fournir une trame avec les JCA (marge)
 - Soit 3x12h le WE mais travail 1 WE/3

Souhaits de l'équipe:
 - L'équipe prefère bosser 1 weekend sur 3 quitte à faire + d'heure par jour
   Travailler un week end sur 2 est OK

---
