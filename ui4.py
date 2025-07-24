import glob
import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates
import utils4 as ut
import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG, format="[%(asctime)-15s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Configuration de Streamlit
st.set_page_config(
    page_title="Mesure de porosité",
    page_icon="🎯",
    layout="wide",
)

tab1, tab2 = st.tabs(["appli", "guide"])

with tab1:
    st.title(":dart: Mesure de porosités")

    # Initialisation du session_state
    if "points" not in st.session_state:
        st.session_state["points"] = []

    if "rotation_angle" not in st.session_state:
        st.session_state["rotation_angle"] = 0

    st.header("Cliquez sur l'image")

    # Fonction pour visualiser un point lors des clicks sur l'image
    def get_ellipse_coords(point: tuple[int, int]) -> tuple[int, int, int, int]:
        center = point
        radius = 3
        return (
            center[0] - radius,
            center[1] - radius,
            center[0] + radius,
            center[1] + radius,
        )

    def acquisition():
            global A1, A2, A3, B1, B2, C0, C1, C2, C3, C4, C5, D1, D2, E1, E2, E3
            C1 = [e for e in lp if e[1] == min([p[1] for p in lp])][0]
            C5 = [e for e in lp if e[1] == max([p[1] for p in lp])][0]
            A2 = [e for e in lp if e[0] == min([p[0] for p in lp])][0]
            lp.remove(C1)
            lp.remove(C5)
            lp.remove(A2)
            A1 = [e for e in lp if e[1] == min([p[1] for p in lp])][0]
            A3 = [e for e in lp if e[0] == min([p[0] for p in lp])][0]
            lp.remove(A1)
            lp.remove(A3)
            C2 = [e for e in lp if e[1] == min([p[1] for p in lp])][0]
            lp.remove(C2)
            C3 = [e for e in lp if e[1] == min([p[1] for p in lp])][0]
            B2 = [e for e in lp if e[0] == min([p[0] for p in lp])][0]
            lp.remove(C3)
            lp.remove(B2)
            D2 = [e for e in lp if e[1] == max([p[1] for p in lp])][0]
            B1 = [e for e in lp if e[0] == min([p[0] for p in lp])][0]
            lp.remove(D2)
            lp.remove(B1)
            D1 = [e for e in lp if e[0] == max([p[0] for p in lp])][0]
            lp.remove(D1)
            C4 = lp[0]
            # Dessin auto
            E1 = ut.symetric(A1, C1, C5)
            E2 = ut.symetric(A2, C1, C5)
            E3 = ut.symetric(A3, C1, C5)
            C0 = ut.intersect_AB_CD(A1, A3, C1, C5)
            ut.plot_line_AB(C0, D1, img, draw, "green")
            ut.plot_line_AB(C0, A1, img, draw, "white")
            ut.plot_line_AB(C0, E1, img, draw, "white")
            ut.plot_line_AB(C0, B1, img, draw, "green")
            ut.plot_line_AB(C0, A2, img, draw, "green")
            ut.plot_line_AB(C0, E2, img, draw, "green")
            ut.plot_line_AB(C1, C5, img, draw, "blue")

    
    # Liste des fichiers dans le dossier data
    image_files = [f for f in glob.glob("data/*.jpg")]

     # Bouton pour sélectionner une image
    selected_image = st.sidebar.file_uploader("Choose a file")

    # Si aucune image n'est téléversée, permettre à l'utilisateur de sélectionner une image parmi une liste
    if selected_image is None:
        selected_image = st.sidebar.selectbox("Sélectionnez une image:", image_files)

    # Afficher l'image sélectionnée

 
    # Champs pour enregistrer diamètre et longueur du cylindre
    Diam = st.sidebar.number_input("Diamètre")
    Long = st.sidebar.number_input("Longueur")

    # Affichage de l'image et enregistrement du click
    with Image.open(selected_image) as img:
        # Redimensionner l'image à 500 pixels de largeur tout en conservant les proportions
        width, height = img.size
        new_width = 500
        new_height = int((new_width / width) * height)
        img = img.resize((new_width, new_height))

        # Rotation image
        if st.sidebar.button("Rotation"):
            st.session_state["rotation_angle"] = (st.session_state["rotation_angle"] + 90) % 360

        # Appliquer la rotation
        img = img.rotate(-st.session_state["rotation_angle"], expand=True)

        draw = ImageDraw.Draw(img)

        # Draw an ellipse at each coordinate in points
        for point in st.session_state["points"]:
            coords = get_ellipse_coords(point)
            draw.ellipse(coords, fill="red")

        # Afficher l'image avec streamlit_image_coordinates
        value = streamlit_image_coordinates(img, key="pil")

        if value is not None:
            point = value["x"], value["y"]

            if point not in st.session_state["points"]:
                st.session_state["points"].append(point)

    # Attribution des points
    lp = st.session_state["points"].copy()
    
    
    if len(lp) == 13:
        b = lp[-1]
        idx = np.argmin([np.abs(a[0]-b[0])+np.abs(a[1]-b[1]) for a in lp[:-1]])
        st.session_state["points"].remove(lp[idx])
        st.write("Essayez un double click")

        # Vérifier à nouveau la longueur après la suppression
        lp = st.session_state["points"].copy()
        if len(lp) == 12:
            acquisition()

            # Calcul
            long_poro, larg_poro, C00, C20, C30, C40, C50 = ut.calcul(Diam, Long, A1, A2, A3, B2, C1, C2, C3, C4, C5, D2, E2, img, draw)
            
            # Dessiner des annotations pour tous les points
            points_dict = {
                "A1": A1, "A2": A2, "A3": A3, "B1": B1, "B2": B2, 
                "C0" : C0, "C1": C1, "C2": C2, "C3": C3, "C4": C4,
                "C5": C5, "D1": D1, "D2": D2, "E1" : E1, "E2" : E2,
                "E3" : E3, "C00" : C00, "C20": C20, "C30": C30, 
                "C40": C40, "C50": C50
            }
            
            logging.debug(f"points enregistrés : {points_dict}")
            
            for point in points_dict.values():
                coords = get_ellipse_coords(point)
                draw.ellipse(coords, fill="red")
            
            for label, point in points_dict.items():
                draw.text((point[0] + 5, point[1] - 5), label, fill="red")

            ut.plot_line_AB(C00, C20, img, draw, "red")
            ut.plot_line_AB(C00, C30, img, draw, "red")
            ut.plot_line_AB(C00, C40, img, draw, "red")

            # Afficher l'image annotée et les dimensions de la porosité
            st.image(img, caption="Image avec annotations", use_column_width=True)
            st.write(f"longueur poro : {long_poro:.2f}")
            st.write(f"largeur poro : {larg_poro:.2f}")
            
    elif len(lp) == 12:
        acquisition()

        # Calcul
        long_poro, larg_poro, C00, C20, C30, C40, C50 = ut.calcul(Diam, Long, A1, A2, A3, B2, C1, C2, C3, C4, C5, D2, E2, img, draw)
       
        # Dessiner des annotations pour tous les points
        points_dict = {
            "A1": A1, "A2": A2, "A3": A3, "B1": B1, "B2": B2, 
            "C0" : C0, "C1": C1, "C2": C2, "C3": C3, "C4": C4,
            "C5": C5, "D1": D1, "D2": D2, "E1" : E1, "E2" : E2,
            "E3" : E3, "C00" : C00, "C20": C20, "C30": C30, 
            "C40": C40, "C50": C50
        }
        
        logging.debug(f"points enregistrés : {points_dict}")
        
        for point in points_dict.values():
            coords = get_ellipse_coords(point)
            draw.ellipse(coords, fill="blue")
            
        for label, point in points_dict.items():
            draw.text((point[0] + 5, point[1] - 5), label, fill="red")

        ut.plot_line_AB(C00, C20, img, draw, "red")
        ut.plot_line_AB(C00, C30, img, draw, "red")
        ut.plot_line_AB(C00, C40, img, draw, "red")

        # Afficher l'image annotée et les dimensions de la porosité
        st.image(img, caption="Image avec annotations", use_column_width=True)
        st.write(f"longueur poro : {long_poro:.2f}")
        st.write(f"largeur poro : {larg_poro:.2f}")

    else:
        st.write("Veuillez sélectionner exactement 6 points.")

with tab2:
    st.title("Guide")
    st.image(Image.open(r"data/input_4.png"))
    st.image(Image.open(r"data/output_4.png"))

