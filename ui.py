import glob
import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates
import utils as ut
import numpy as np

# Configuration de Streamlit
st.set_page_config(page_title="Mesure de porosité", page_icon="🎯", layout="wide")

def get_ellipse_coords(point):
    center = point
    radius = 3
    return (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius)

def find_point(lp, condition):
    return [e for e in lp if condition(e)][0]

def annotate_image(img, draw, points_dict):
    for label, point in points_dict.items():
        draw.text((point[0] + 5, point[1] - 5), label, fill="red")

def draw_lines(img, draw, C, G, D, A, B, K, O, V, W, N):
    draw.line(xy=[C, G], width=1, fill="yellow")
    ut.parallele_AB_C(D, B, G, img, draw)
    ut.parallele_AB_C(D, A, G, img, draw)
    ut.mediatrice_AB(A, B, img, draw)
    draw.line(xy=[K, O], width=1, fill="yellow")
    draw.line(xy=[K, V], width=1, fill="green")
    draw.line(xy=[K, W], width=1, fill="green")
    draw.line(xy=[K, N], width=1, fill="yellow")

def process_points(lp, img, draw, Diam, Long):
    C = find_point(lp, lambda x: x[1] == min([p[1] for p in lp]))
    G = find_point(lp, lambda x: x[1] == max([p[1] for p in lp]))
    P = find_point(lp, lambda x: x[0] == min([p[0] for p in lp]))
    Q = find_point(lp, lambda x: x[0] == max([p[0] for p in lp]))
    lp.remove(C)
    lp.remove(G)
    lp.remove(P)
    lp.remove(Q)

    H = find_point(lp, lambda x: x[0] == min([p[0] for p in lp]))
    I = find_point(lp, lambda x: x[0] == max([p[0] for p in lp]))
    lp.remove(H)
    lp.remove(I)

    A = find_point(lp, lambda x: x[0] == min([p[0] for p in lp]))
    B = find_point(lp, lambda x: x[0] == max([p[0] for p in lp]))
    lp.remove(A)
    lp.remove(B)

    D = find_point(lp, lambda x: x[1] == min([p[1] for p in lp]))
    lp.remove(D)

    R = find_point(lp, lambda x: x[0] == min([p[0] for p in lp]))
    S = find_point(lp, lambda x: x[0] == max([p[0] for p in lp]))
    E = find_point(lp, lambda x: x[1] == min([p[1] for p in lp]))
    F = find_point(lp, lambda x: x[1] == max([p[1] for p in lp]))

    long_poro, larg_poro, J, K, M, T, N, V, W, O, U = ut.calcul(Diam, Long, A, B, C, D, E, F, G, H, I, P, Q, R, S, img, draw)

    points_dict = {
        "C": C, "G": G, "P": P, "Q": Q, "H": H, "I": I, "A": A, "B": B,
        "D": D, "R": R, "S": S, "E": E, "F": F, "J": J, "K": K, "M": M,
        "T": T, "N": N, "V": V, "W": W, "O": O, "U": U
    }

    annotate_image(img, draw, points_dict)
    draw_lines(img, draw, C, G, D, A, B, K, O, V, W, N)

    st.image(img, caption="Image avec annotations", use_column_width=True)
    st.write(f"longueur poro : {long_poro:.2f}")
    st.write(f"largeur poro : {larg_poro:.2f}")

tab1, tab2 = st.tabs(["appli", "guide"])

with tab1:
    st.title(":dart: Mesure de porosités")

    if "points" not in st.session_state:
        st.session_state["points"] = []
    if "rotation_angle" not in st.session_state:
        st.session_state["rotation_angle"] = 0

    st.header("Cliquez sur l'image")

    image_files = [f for f in glob.glob("data/*.jpg")]
    selected_image = st.sidebar.selectbox("Sélectionnez une image:", image_files)
    Diam = st.sidebar.number_input("Diamètre")
    Long = st.sidebar.number_input("Longueur")

    with Image.open(selected_image) as img:
        width, height = img.size
        new_width = 500
        new_height = int((new_width / width) * height)
        img = img.resize((new_width, new_height))

        if st.sidebar.button("Rotation"):
            st.session_state["rotation_angle"] = (st.session_state["rotation_angle"] + 90) % 360

        img = img.rotate(-st.session_state["rotation_angle"], expand=True)
        draw = ImageDraw.Draw(img)

        for point in st.session_state["points"]:
            coords = get_ellipse_coords(point)
            draw.ellipse(coords, fill="red")

        value = streamlit_image_coordinates(img, key="pil")
        if value is not None:
            point = value["x"], value["y"]
            if point not in st.session_state["points"]:
                st.session_state["points"].append(point)

        lp = st.session_state["points"].copy()
        if len(lp) == 14:
            b = lp[-1]
            idx = np.argmin([np.abs(a[0]-b[0])+np.abs(a[1]-b[1]) for a in lp[:-1]])
            st.session_state["points"].remove(lp[idx])
            st.write("Essayez un double click")
            lp = st.session_state["points"].copy()

        if len(lp) == 13:
            process_points(lp, img, draw, Diam, Long)
        else:
            st.write("Veuillez sélectionner exactement 13 points.")

with tab2:
    st.title("Guide")
    st.image(Image.open(r"C:\Users\John\Desktop\jupyter_notebooks\Porosimetre\data\result.png"))
