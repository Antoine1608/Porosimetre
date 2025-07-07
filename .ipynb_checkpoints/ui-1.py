import glob
import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates
import utils as ut
import numpy as np

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
    
    # Liste des fichiers dans le dossier data
    image_files = [f for f in glob.glob("data/*.jpg")]
    
    # Bouton pour sélectionner une image
    selected_image = st.sidebar.selectbox("Sélectionnez une image:", image_files)
    
    # Champs pour enregistrer diamètre et longueur du cylindre
    Diam = st.sidebar.number_input("Diamètre")
    Long = st.sidebar.number_input("Longueur")
    
    # Affichage de l'image et enregistrement du click
    #st.write("## Image")
    
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
        C = [e for e in lp if e[1] == min([x[1] for x in lp])][0]
        G = [e for e in lp if e[1] == max([x[1] for x in lp])][0]
        P = [e for e in lp if e[0] == min([x[0] for x in lp])][0]
        Q = [e for e in lp if e[0] == max([x[0] for x in lp])][0]
        lp.remove(C)
        lp.remove(G)
        lp.remove(P)
        lp.remove(Q)
        H = [e for e in lp if e[0] == min([x[0] for x in lp])][0]
        I = [e for e in lp if e[0] == max([x[0] for x in lp])][0]
        lp.remove(H)
        lp.remove(I)
        A = [e for e in lp if e[0] == min([x[0] for x in lp])][0]
        B = [e for e in lp if e[0] == max([x[0] for x in lp])][0]
        lp.remove(A)
        lp.remove(B)
        D = [e for e in lp if e[1] == min([x[1] for x in lp])][0]
        lp.remove(D)
        R = [e for e in lp if e[0] == min([x[0] for x in lp])][0]
        S = [e for e in lp if e[0] == max([x[0] for x in lp])][0]
        E = [e for e in lp if e[1] == min([x[1] for x in lp])][0]
        F = [e for e in lp if e[1] == max([x[1] for x in lp])][0]
    
        long_poro, larg_poro, J, K, M, T, N, V, W, O, U = ut.calcul(Diam, Long, A, B, C, D, E, F, G, H, I, P, Q, R, S)
    
        # Dessiner des annotations pour tous les points
        points_dict = {
            "C": C, "G": G, "P": P, "Q": Q,
            "H": H, "I": I, "A": A, "B": B,
            "D": D, "R": R, "S": S, "E": E, 
            "F": F, "J": J, "K": K, "M": M,
            "T": T, "N": N, "V": V, "W": W,
            "O": O, "U": U
        }
    
        for label, point in points_dict.items():
            draw.text((point[0] + 5, point[1] - 5), label, fill="red")
    
        draw.line(xy=[C, G], width=1, fill="yellow")

        # Fonction pour tracer une parallèle
        def parallele_AB_C(A, B, C):
            # Calculer la pente de la ligne AB
            if B[0] - A[0] == 0:
                # Ligne verticale
                x = C[0]
                y1 = 0
                y2 = img.height
            else:
                slope = (B[1] - A[1]) / (B[0] - A[0])
                # Calculer l'ordonnée à l'origine de la ligne parallèle passant par C
                intercept = C[1] - slope * C[0]
                # Calculer les points d'intersection avec les bords de l'image
                if slope == 0:
                    # Ligne horizontale
                    y = C[1]
                    x1 = 0
                    x2 = img.width
                else:
                    # Calculer les points d'intersection avec les bords gauche et droit de l'image
                    x1 = 0
                    y1 = intercept
                    x2 = img.width
                    y2 = slope * img.width + intercept
            # Dessiner la ligne parallèle
            draw.line(xy=[(x1, y1), (x2, y2)], width=1, fill="yellow")
    
        # Tracer les parallèles à DB et DA passant par G
        parallele_AB_C(D, B, G)
        parallele_AB_C(D, A, G)
    
        # Afficher l'image annotée et les dimensions de la porosité
        st.image(img, caption="Image avec annotations", use_column_width=True)    
        st.write(f"longeur poro : {long_poro:.2f}")
        st.write(f"largeur poro : {larg_poro:.2f}")
    
    elif len(lp) == 14:
        b = lp[-1]
        idx = np.argmin([np.abs(a[0]-b[0])+np.abs(a[1]-b[1]) for a in lp[:-1]])
        st.session_state["points"].remove(lp[idx])
        lp = st.session_state["points"].copy()
        st.write("Essayez un double click")
        print(len(st.session_state["points"]))
        print(st.session_state["points"])    
    else:
        st.write("Veuillez sélectionner exactement 13 points.")

with tab2 :
    st.title("Guide")
    st.image(Image.open(r"C:\Users\John\Desktop\jupyter_notebooks\Porosimetre\data\result.png"))