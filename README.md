# Porosimètre

### Présentation :
Il s'agit d'une application pour mesurer la taille de porosité à l'intérieur de perçages usinés sur des pièces de fonderie. L'utilisateur fournit une image du perçage avec sa porosité, le diamètre du perçage et la longueur du perçage. L'application renvoie ensuite la largeur et la longueur de la porosité.

### Guide d'utilisation :
1. Déployer l'application (voir chapitre Déploiement)
2. Importer l'image du perçage avec la porosité en prenant bien soin d'avoir une photo qui montre le perçage dans toute sa longueur.

_photo OK : on voit le perçage dans toute sa longueur :_

![photo_OK](/data/perçage_OK.png)

_photo NOK : on ne voit pas le perçage dans toute sa longueur :_

![photo_NOK](/data/perçage_NOK.png)

3. Cliquer ensuite sur différents points précis de l'image pour permettre à l'algorithme de faire ses calculs. Les points à sélectionner sont présentés sous l'onglet "guide"
4. Une fois les points sélectionnés, le calcul se fait automatiquement et à la fin apparaissent les valeurs de la largeur et de la longueur de la porosité. En même temps s'affiche une image avec les différents traits de construction pour arriver au résultat. Il est possible de replacer les points en recliquant sur les zones les plus appropriées sur l'image interactive.

Voir la vidéo ci-dessous qui synthétise tout ce qui est vu dans ce chapitre.

### Explication des calculs :
Les points renseignés permettent de déterminer l'axe de symétrie de la figure et le point de fuite des lignes parallèles à l'axe du perçage. Grâce à ce point de fuite, on peut projeter sur une ligne horizontale le diamètre apparent du perçage ainsi que la largeur apparente de la porosité. Avec la valeur du diamètre du perçage rentrée au départ, on en déduit, par un produit en croix, la largeur réelle de la porosité :

$\text{largeur réelle porosité} = \frac{\text{largeur apparente porosité} \times \text{diamètre réel perçage}}{\text{diamètre apparent perçage}} \$

En ce qui concerne la détermination de la longueur de la porosité qui se trouve dans l'axe du perçage, on doit procéder d'une manière différente. Sur la ligne d'horizon, on va poser un nouveau point décalé par rapport au point de fuite. À partir de ce nouveau point, comme dans l'étape précédente pour la largeur, on va pouvoir projeter la longueur du perçage ainsi que la longueur de la porosité sur une ligne horizontale. On en déduit la longueur apparente de la porosité par rapport à la longueur apparente du perçage. Et avec la valeur réelle de la longueur du perçage rentrée au départ, par un produit en croix, on en déduit la longueur réelle de la porosité :

$\text{longueur réelle porosité} = \frac{\text{longueur apparente porosité} \times \text{longueur réelle perçage}}{\text{longueur apparente perçage}}\$

## Déploiement :

### Option 1 - Pour la déployer en local :
- Cloner ce dépôt
- Dans la CLI, se placer dans le répertoire Porosimetre
- Taper la commande suivante :
  ```streamlit run ui.py```

### Option 2 - Pour la déployer avec docker :
- Ouvrir Docker desktop (préalablement installé)
- Dans la CLI taper :
  ```docker build -t img .```
(attention : ne pas oublier le ".")

- Ensuite Dans la CLI taper :  
```docker run -d -p 8501:8501 img```
- Dans google Chrome taper 
  ```Localhost:8501```
et l'interface streamlit s'ouvre

- Une fois terminé, taper dans la CLI 
  ```docker ps```
pour récupérer l'id (ex:1d0464dd6def)

- Dans la CLI taper : 
  ```docker stop 1d0464dd6def```
pour fermer le conteneur

### Option 3 - Pour la déployer avec streamlit.io :

- Dans le navigateur aller dans streamlit.io

- Deploying?: Try free en haut à droite de l'écran

- Create app en haut à droite de l'écran

- Deploy a public app from GitHub - Deploy now

- Remplir les champs (ceux du repos GitHub)

- Dans setting préciser Python 3.9

- Deploy