#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates
import numpy as np

# Mise en page
st.title("Test image")
file = st.sidebar.file_uploader("Selection image")
Diam = st.sidebar.number_input("Diamètre")

# Définition du session_state
if "points" not in st.session_state:
    st.session_state["points"] = []

# Acquisition des points
def get_ellipse_coords(point: tuple[int, int]) -> tuple[int, int, int, int]:
    center = point
    radius = 5
    return (
        center[0] - radius,
        center[1] - radius,
        center[0] + radius,
        center[1] + radius,
    )

if file is not None:
    img = Image.open(file)
    draw = ImageDraw.Draw(img)

    # Draw an ellipse at each coordinate in points
    for point in st.session_state["points"]:
        coords = get_ellipse_coords(point)
        draw.ellipse(coords, fill="red")

    # Afficher l'image avec streamlit_image_coordinates
    value = streamlit_image_coordinates(img, key="pil")

    if value is not None:
        point = (value["x"], value["y"])
        if point not in st.session_state["points"]:
            st.session_state["points"].append(point)

    # Attribution des points
    lp = st.session_state["points"].copy()
    if len(lp) == 1:
        draw.ellipse((lp[0][0]-50, lp[0][1]-50, lp[0][0]+50, lp[0][1]+50,), fill="red")
        st.session_state["points"] = []  # Reset points after drawing the line
        
    # Afficher l'image mise à jour
    st.image(img, use_column_width=True)
