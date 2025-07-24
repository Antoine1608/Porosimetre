import numpy as np
import matplotlib.pyplot as plt
import math

# trace la parallèle à P1P2 passant par P3 - retourne le point d'intersection de la droite avec l'axe y
def parallele_AB_C(P1, P2, P3, img, draw):
    # Calculer la pente de P1P2
    if P2[0] - P1[0] == 0:
        # Si P1P2 est verticale, la parallèle est aussi verticale
        x = P3[0]
        y1 = 0
        y2 = img.height
        # Dessiner la ligne verticale
        draw.line(xy=[(x, y1), (x, y2)], width=1, fill="green")
        return (x, 0)
    else:
        # Calculer la pente de P1P2
        slope_P1P2 = (P2[1] - P1[1]) / (P2[0] - P1[0])
        # La pente de la parallèle est la même que celle de P1P2
        slope = slope_P1P2
        # Calculer l'ordonnée à l'origine (b) de la parallèle passant par P3
        intercept = P3[1] - slope * P3[0]

        # Calculer les points d'intersection de la parallèle avec les bords de l'image
        if slope == 0:
            # Ligne horizontale
            y = intercept
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
        return (0, intercept)

# trace la ligne P1P2
def plot_line_AB(P1, P2, img, draw, color):
    # Calculer la pente de la droite P1P2
    if P2[0] - P1[0] == 0:
        # Si P1P2 est verticale
        x = P1[0]
        y1 = 0
        y2 = img.height
        # Dessiner la ligne verticale
        draw.line(xy=[(x, y1), (x, y2)], width=1, fill=color)
    else:
        # Calculer la pente de la droite P1P2
        slope = (P2[1] - P1[1]) / (P2[0] - P1[0])
        # Calculer l'ordonnée à l'origine (b)
        intercept = P1[1] - slope * P1[0]

        if slope == 0:
            # Si P1P2 est horizontale
            y = intercept
            y1 = intercept
            y2 = intercept
            x1 = 0
            x2 = img.width
        else:
            # Calculer les points d'intersection avec les bords de l'image
            x1 = 0
            y1 = intercept
            x2 = img.width
            y2 = slope * img.width + intercept

        # Dessiner la ligne
        draw.line(xy=[(x1, y1), (x2, y2)], width=1, fill=color)


# retourne les coordonnées du point d'intersection de P1P2 avec P3P4
def intersect_AB_CD(P1, P2, P3, P4):
    # Calcul de la pente et de l'ordonnée à l'origine de la droite P1P2
    if P2[0] - P1[0] == 0:
        # Si P1P2 est verticale
        x1 = P1[0]
        # Équation de la droite verticale : x = x1
    else:
        a1 = (P2[1] - P1[1]) / (P2[0] - P1[0])
        b1 = P1[1] - a1 * P1[0]

    # Calcul de la pente et de l'ordonnée à l'origine de la droite P3P4
    if P4[0] - P3[0] == 0:
        # Si P3P4 est verticale
        x2 = P3[0]
        # Équation de la droite verticale : x = x2
    else:
        a2 = (P4[1] - P3[1]) / (P4[0] - P3[0])
        b2 = P3[1] - a2 * P3[0]

    # Vérification si les droites sont parallèles
    if (P2[0] - P1[0] == 0 and P4[0] - P3[0] == 0) or (P2[0] - P1[0] != 0 and P4[0] - P3[0] != 0 and a1 == a2):
        return None  # Les droites sont parallèles, pas d'intersection

    # Calcul de l'intersection des deux droites
    if P2[0] - P1[0] == 0:
        # P1P2 est verticale, utiliser l'équation de P3P4 pour trouver y
        x = x1
        y = a2 * x + b2
    elif P4[0] - P3[0] == 0:
        # P3P4 est verticale, utiliser l'équation de P1P2 pour trouver y
        x = x2
        y = a1 * x + b1
    else:
        # Les deux droites ne sont pas verticales, calculer l'intersection normale
        x = (b2 - b1) / (a1 - a2)
        y = a1 * x + b1

    return (x, y)

# retourne la distance AB
def distance_A_B(A, B):
    return ((A[0] - B[0])**2 + (A[1] - B[1])**2)**0.5

# trace la médiatrice de AB
def mediatrice_AB(A, B, img, draw):
    # Calculer le milieu de AB
    mid_x = (A[0] + B[0]) / 2
    mid_y = (A[1] + B[1]) / 2

    # Calculer la pente de AB
    if B[0] - A[0] == 0:
        # Si AB est verticale, la médiatrice est horizontale
        slope = 0
        intercept = mid_y
    else:
        slope_AB = (B[1] - A[1]) / (B[0] - A[0])
        # La pente de la médiatrice est l'opposé de l'inverse de la pente de AB
        if slope_AB == 0:
            # Si AB est horizontale, la médiatrice est verticale
            slope = None
            intercept = mid_x
        else:
            slope = -1 / slope_AB
            intercept = mid_y - slope * mid_x

    # Calculer les points d'intersection de la médiatrice avec les bords de l'image
    if slope is None:
        # Ligne verticale
        x = intercept
        y1 = 0
        y2 = img.height
    elif slope == 0:
        # Ligne horizontale
        y1 = intercept
        y2 = intercept
        x1 = 0
        x2 = img.width
    else:
        # Calculer les points d'intersection avec les bords gauche et droit de l'image
        x1 = 0
        y1 = intercept
        x2 = img.width
        y2 = slope * img.width + intercept

    if slope is None:
        # Dessiner la ligne verticale
        draw.line(xy=[(x, y1), (x, y2)], width=1, fill="yellow")
    else:
        # Dessiner la ligne horizontale ou oblique
        draw.line(xy=[(x1, y1), (x2, y2)], width=1, fill="yellow")

# trace la parallèle à AB passant par C
def parallele_AB_C(A, B, C, img, draw):
                # Calculer la pente de la ligne AB
                if B[0] - A[0] == 0:
                    # Ligne verticale
                    x1 = C[0]
                    x2 = C[0]
                    y1 = 0
                    y2 = img.height
                else:
                    slope = (B[1] - A[1]) / (B[0] - A[0])
                    # Calculer l'ordonnée à l'origine de la ligne parallèle passant par C
                    intercept = C[1] - slope * C[0]
                    # Calculer les points d'intersection avec les bords de l'image
                    if slope == 0:
                        # Ligne horizontale
                        y1 = C[1]
                        y2 = C[1]
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
                return (x1, y1)

# retourne les coordonnées du symétrique de A par rapport à BC
def symetric(A, B, C):
    xA, yA = A
    xB, yB = B
    xC, yC = C

    # Calcul de la pente de la droite BC
    if xC == xB:
        # La droite BC est verticale
        x_I = xB
        # Équation de la droite perpendiculaire à BC passant par A
        # La droite perpendiculaire est horizontale
        y_I = yA
    else:
        m_BC = (yC - yB) / (xC - xB)
        # Équation de la droite BC : y = m_BC * x + c_BC
        c_BC = yB - m_BC * xB

        # Calcul de la pente de la droite perpendiculaire à BC
        if m_BC == 0:
            # La droite BC est horizontale, la perpendiculaire est verticale
            x_I = xA
            # Équation de la droite BC : y = c_BC
            y_I = c_BC
        else:
            m_perp = -1 / m_BC
            # Équation de la droite perpendiculaire : y = m_perp * x + c_perp
            c_perp = yA - m_perp * xA

            # Calcul du point d'intersection I
            x_I = (c_perp - c_BC) / (m_BC - m_perp)
            y_I = m_BC * x_I + c_BC

    # Calcul des coordonnées de D
    x_D = 2 * x_I - xA
    y_D = 2 * y_I - yA

    return (x_D, y_D)


# calcul des dimensions de la porosité
def calcul(Diam, Long, A1, A2, A3, B2, C1, C2, C3, C4, C5, D2, E2, img, draw):
    
    # Les points de fuite
    C0 = intersect_AB_CD(A1, A3, C1, C5)
    C00 = parallele_AB_C(A2, E2, C0, img, draw)

    # La ligne de projection
    C50 = parallele_AB_C(A2, E2, C5, img, draw)    
    
    # longueur poro
    C20 = intersect_AB_CD(C00, C2, C5, C50)
    C30 = intersect_AB_CD(C00, C3, C5, C50)
    C40 = intersect_AB_CD(C00, C4, C5, C50)

    long_poro = (distance_A_B(C30, C40)/distance_A_B(C20, C5))*Long
    print ("longueur poro : ", (long_poro))  

    # largeur poro
    B2D2 = distance_A_B(B2, D2)
    A2E2 = distance_A_B(A2, E2)

    larg_poro = (B2D2/A2E2)*Diam
    print ("largeur poro : ", larg_poro)

    return long_poro, larg_poro, C00, C20, C30, C40, C50
