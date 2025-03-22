# WikipediaBigData

Ce projet a pour but de trouver des chemins optimaux pour le jeu Wiki Speedrun Game. Ce dernier consiste à passer d'une page à une autre, en utilisant uniquement les hyperliens présents dans les pages.

Pour ce projet, nous avons décidé d'utiliser le Wikipédia normand puisque ce dernier contient moins de pages et que celles-ci sont plus petites.

En ce qui concerne le fonctionnement, le script `crawler.py` va chercher des pages au hasard grace à la page `https://nrm.wikipedia.org/wiki/Spécial:Page_au_hasard` pour mettre leur contenu dans le dossier `/target/raw`.
Ensuite, le mapper `parser.py` s'occupe d'extraire tous les liens, et d'en faire un fichier dans `/target/extracted`.
Puis, on refait un appel à `crawler.py` pour refaire les requêtes sur les liens trouvés.
Enfin, un fois les données traitées de cette manière, on utilise divers map/reduce pour traiter les données avec des algorithmes de graphes, tels qu'un map avec pour fonction l'algorithme de Dijkstra et un reduce pour le calcul du nombre de pages atteignables.

Cependant, le crawler étant assez lent pour traiter de nombreux articles, nous avons décidé d'utiliser l'API wikipedia afin de récolter plus efficacement les données et la liste des liens de chaque article. On peut retrouver la liste des articles du wikipédia français (par exemple) dans les dumps wikipédia `http://dumps.wikimedia.org/frwiki/latest`. On a pris le premier fichier (celui du 8 mars) qui contient plus de 4.5 million de pages (dont les catégories, dicussions, projets, etc..)

Le script `mapper2.py` permet d'effectuer des requètes sur l'API wikipédia afin de récolter la liste des liens se trouvant sur une page précise. Par exemple, la requète `https://fr.wikipedia.org/w/api.php?action=query&titles=France&prop=links&pllimit=max&format=json` parmet de récupérer la liste des liens au format json de la page France. Nous avons limité les requêtes à 50000 articles car c'est assez lent (entre 5 et 10 requêtes par seconde) mais avec plusieurs machines se séparant la liste on pourrait réussir à récupérer les données de l'ensemble des pages. Ces données sont ensuite enregistrées au format parquet sous la forme [titre de l'article, liste des titres des articles cités]

Le script `reducer2.py` permet de créer un ranking des pages les plus citées (petite quête annexe) par ces 50000 articles.