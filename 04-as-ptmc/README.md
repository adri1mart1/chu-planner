Prise de notes pour le pb N°3

Objectif

Faire des propositions de planning pour les AS du PTMC de Nantes.
Il y a 3 plannings à construire:

- 1 planning de jour pour 22 personnes à la fois en 12h et en 7h30.
- 1 planning en alternance jour nuit (8 semaines de jour et 8 semaines de nuit), pour 16 personnes.
  La nuit c'est tout en 12h. Et le jour c'est du 12h et du 7h30
- 1 planning que de nuit pour 8 personnes, tout en 12h

Et il faut que tous les planning combinés ensemble:
- il y ait:
  - 2 personnes en 7h30 par jour (du lundi au vendredi)
  - 1 personne en 7h30 le samedi et le dimanche
  - (il y ai 1 personne en Jca tous les jours et toutes les nuits (du lundi au dimanche))
  - 9 personnes tous les jours (we compris) en 12h


vérifier si c'est 48h sur 7j glissant la limite légale (vs 52h)


# Calcul de charge

Chaque personne travaille 35h.

## En journée

Sur le service il y a 22 personnes (jour) + 16 personnes (alternance)
(22 + 16) * 35 = 1330 heures par semaines de travail

Il est demandé d'avoir:
- 2 personnes en 7h30 chaque jour
- 1 personne en 7h30 le weekend
- 9 personnes en 12h toute la semaine

(2 * 7.5 * 5) + (1 * 7.5 * 2) + (9 * 12 * 7) = 75 + 15 + 108 + 756 = 954h.

Chaque semaine, la charge de travail demandée dans le service (954h) par rapport à la charge du
service théorique (1330h) semble cohérente. ça ne prends pas en compte les congés, RTT, JCA, arrêts...
(Je ne connais pas ces nombres).

## La nuit

Il est demandé d'avoir:
 - 6 personnes en 12h du Lundi au Vendredi
 - 5 personnes en 12h le samedi et le dimanche

(6 * 12) + (5 * 12) = 132h.

Chaque semaine, la charge de travail demandée dans le service la nuit est de 132h. L'effectif théorique
de nuit est de 8 personnes (8 * 35 = 280h)

## Equilibre

Par curiosité, on va faire un calcul d'équilibre de charge.
Normalement, un service doit fournir une offre de soin. Cette offre de soin se compte se compte en heure.
(Ex: en rea, il y a 2.5 patient par infirmier.e, s'il y a 10 lits, il nous faut 4 personnes). C'est très
empirique car je suppose que ce n'est pas la même entre la nuit et le jour, entre les services etc...

En revanche, si le besoin d'un service est d'avoir X personnes en continue, il est nécessaire d'avoir
X+n personnes (en discontinue) pour faire le job. Pourquoi en discontinue ? car on ne travaille pas 24h/24h.

Une façon de penser les choses est de raisonner en heure, comme ci-dessus. Si on doit fournir 954h de soin,
ça veut dire qu'on a besoin à minima de 954h / 35h = 27.25. Donc 28 personnes sur une semaine. C'est à peu
près vrai sur une semaine mais clairement pas sur le long terme car toutes les personnes ont des arrêts
prévus (congés payés, RTT, formation, ..) et malheureusement des fois, des jours imprévus (arrêts maladies,
démissions, ...).
Les arrêts prévus peuvent être estimés assez finement, il y a des règles strictes à suivre pour l'attribution
des congés. Il peut également y avoir des quotas de jours de formation.
Les arrêts imprévus peuvent être estimés empiriquement. Une possibilité naive pourrait être de moyenner le
temps d'arrêt imprévus sur une certaine période (6 mois, 1 an, 2 ans, .. faire l'exercice sur plusieurs
périodes pour voir ce qui est le plus juste), et de rajouter ce pourcentage d'arrêts au nombre global de
personnes nécéssaires.

Ainsi et pour résumé:

Si on ajoute le nombre d'heure travaillées nécéssaires dans le service
+ les arrêts prévus
+ les arrêts imprévus
On est censé tomber sur le nombre idéal de personnes pour satisfaire les besoins du service.

Nous n'avons pas ces infos, par contre, nous avons:
 - Le nombre d'heure travaillées nécéssaires dans le service (ce qui est demandé par les cadres)
 - Le nombre de personnes disponibles avec leur nombre d'heure (l'effectif).

On devrait tomber sur un équilibre entre le jour et la nuit.

### La nuit

On a besoin de 132h de travail. Il y a un effectif pouvant fournir 280h (hors arrêts).
132 / 280 = 47.1%

### Le jour

On a besoin de 954h de travail. Il y a un effectif pouvant fournir 1330h (hors arrêts).
954 / 1330 = 71.7%

### Conclusion

L'écart entre les 2 ratios est grands. Il ne sont pas dimensionnés de la même manière. Après en avoir discuté,
mon calcul considère que toutes les personnes travaillent à 100% ce qui ne semble pas être la vérité.
Je laisse la réflexion en l'état pour la partager en tout cas.


# Déroulement

## 1e étape, génération des trames

1er essais de génération des trames sur 16 semaines car le planning d'alternance est sur 16 semaines.
C'est normalement hors la loi, cf:
https://www.demarches.interieur.gouv.fr/particuliers/duree-travail-fonction-publique-hospitaliere-fph
mais les retours des personnes concernées disent que le rythme 2 mois jour / 2 mois nuit est nécessaire. Un rythme
plus court induit plus de fatigue.

Il est finalement plus judicieux de proposer une trame sur 18 semaines car 18 est un multiple de 3. Si
on souhaite trouver une solution pour travailler un weekend sur 3, faire en sortie d'avoir un multiple
de 3 permet de reboucler indéfiniement la trame sans déséquilibre.
Pour le planning d'alternance, ce ne serait plus 8 semaines / 8 semaines mais 9 semaines / 9 semaines.
ça semble être un compromis raisonnable.


Contrainement à ce qui est fait actuellement, tous les plannings sont générés sur 18 semaines pour
simplifier le programme. Lorsqu'il faudra mettre ensemble les différentes trames (alternance, jour, etc..),
C'est nettement plus simple de comparer les effectifs chaque jour si les trames font tous la même
taille.
