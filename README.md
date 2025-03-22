# WikipediaBigData

Ce projet a pour but de trouver des chemins optimaux pour le jeu Wiki Speedrun Game. Ce dernier consiste à passer d'une page à une autre, en utilisant uniquement les hyperliens présents dans les pages.

Pour ce projet, nous avons décidé d'utiliser le Wikipédia normand puisque ce dernier contient moins de pages et que celles-ci sont plus petites.

En ce qui concerne le fonctionnement, le script `crawler.py` va chercher des pages au hasard grace à la page `https://nrm.wikipedia.org/wiki/Spécial:Page_au_hasard` pour mettre leur contenu dans le dossier `/target/raw`.
Ensuite, le mapper `parser.py` s'occupe d'extraire tous les liens, et d'en faire un fichier dans `/target/extracted`.
Puis, on refait un appel à `crawler.py` pour refaire les requêtes sur les liens trouvés.
Enfin, un fois les données traitées de cette manière, on utilise divers map/reduce pour traiter les données avec des algorithmes de graphes, tels qu'un map avec pour fonction l'algorithme de Dijkstra et un reduce pour le calcul du nombre de pages atteignables.

