# Porosimetre
## Cette application permet de mesurer la largeur et la longueur d'une porosité à l'intérieur d'un cylindre à partir d'une photo
Option 1 - Pour la déployer en local:
-Dans la CLI se placer dans le répertoire Porosimetre
-Taper streamlit run ui.py
-Dans google Chrome taper Localhost:8501 et l'interface streamlit s'ouvre

Option 2 - Pour la déployer avec docker:
-Ouvrir Docker desktop (préalblement installé)
-Dans la CLI taper docker build -t img . (attention : ne pas oublier le ".")
-Ensuite Dans la CLI taper docker run -d -p 8501:8501 img
-Dans google Chrome taper Localhost:8501 et l'interface streamlit s'ouvre
-Une fois terminé, taper dans la CLI docker ps pour récupérer l'id (ex:1d0464dd6def)
-Dans la CLI taper docker stop 1d0464dd6def

Option 3 - Pour la déployer avec streamlit.io:
-Dans le navigateur aller dans streamlit.io
-Deploying?: Try free en haut à droite de l'écran
-Create app en haut à droite de l'écran
-Deploy a public app from GitHub - Deploy now
-Remplir les champs (ceux du repos GitHub)
-Dans setting préciser Python 3.9
-Deploy

