import glob
import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates
import utils3 as ut
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
            global A1, A2, A3, B1, B2, C0, C1, C2, C3, C4, C5, D1, D2, E1, E2, E3, O1, O2
            A1 = lp[0]
            B1 = lp[1]
            B2 = lp[2]
            C1 = lp[3]
            C3 = lp[4]
            # Dessin auto
           #C2 =(img.size[0],img.size[1])
            D1 = ut.symetric(B1, C1, C3)
            E1 = ut.symetric(A1, C1, C3)
            C2 = ((A1[0] + E1[0])/2, (A1[1] + E1[1])/2)
            D2 = ut.symetric(B2, C1, C3)
            #A2 = ut.parallele_AB_C(B1, B2, A1, img, draw)
            O2 = ut.intersect_AB_CD(B1, B2, C1, C3)
            O1 = ut.symetric_point(O2, C2)
            ut.plot_line_AB(B2, D2, img, draw)
            ut.plot_line_AB(O1, B1, img, draw)
            ut.plot_line_AB(O2, B1, img, draw)
            ut.parallele_D_BC_A(B1, D1, C1, C3, img, draw)
    
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
    
    
    if len(lp) == 6:
        b = lp[-1]
        idx = np.argmin([np.abs(a[0]-b[0])+np.abs(a[1]-b[1]) for a in lp[:-1]])
        st.session_state["points"].remove(lp[idx])
        st.write("Essayez un double click")

        # Vérifier à nouveau la longueur après la suppression
        lp = st.session_state["points"].copy()
        if len(lp) == 5:
            acquisition()
            
            # Dessiner des annotations pour tous les points
            points_dict = {
                "A1": A1, "B1": B1, "B2": B2, 
                "C1": C1, "C2": C2, "C3": C3, 
                "D1": D1, "D2": D2, "E1" : E1,
                "O1": O1, "O2": O2
                           }
            
            logging.debug(f"points enregistrés : {points_dict}")
            
            for point in points_dict.values():
                coords = get_ellipse_coords(point)
                draw.ellipse(coords, fill="blue")
            
            for label, point in points_dict.items():
                draw.text((point[0] + 5, point[1] - 5), label, fill="red")

            # Afficher l'image annotée et les dimensions de la porosité
            st.image(img, caption="Image avec annotations", use_column_width=True)
                       
    elif len(lp) == 5:
        acquisition()
      
        # Dessiner des annotations pour tous les points
        points_dict = {
            "A1": A1, "B1": B1, "B2": B2, 
            "C1": C1, "C2": C2, "C3": C3, 
            "D1": D1, "D2": D2, "E1" : E1,
            "O1": O1, "O2": O2
                       }
        
        logging.debug(f"points enregistrés : {points_dict}")
        
        for point in points_dict.values():
            coords = get_ellipse_coords(point)
            draw.ellipse(coords, fill="blue")
        
        for label, point in points_dict.items():
            draw.text((point[0] + 5, point[1] - 5), label, fill="red")
        

        # Afficher l'image annotée et les dimensions de la porosité
        st.image(img, caption="Image avec annotations", use_column_width=True)

    else:
        st.write("Veuillez sélectionner exactement 12 points.")

with tab2:
    st.title("Guide")
    #st.image(Image.open(r"C:\Users\John\Desktop\jupyter_notebooks\Porosimetre\data\result.png"))
    st.image(Image.open(r"data/result_3.png"))

