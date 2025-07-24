import numpy as np
import matplotlib.pyplot as plt
# trace la parallèle à P1P2 passant par P3
def parallele_AB_C_(P1, P2, P3):
    # Vérification du cas particulier où le segment AB est vertical
    if P1[0] == P2[0]:
        # La parallèle sera une droite verticale passant par C
        x_vals = np.array([P3[0], P3[0]])  # x reste constant
        y_vals = np.array([P3[1] - 500, P3[1] + 500])  # Étend la droite sur l'axe y
        plt.plot(x_vals, y_vals, '--y')
        return (P3[0],0)
    else:
        # Calcul de la pente de la parallèle
        a = (P2[1] - P1[1])/(P2[0] - P1[0])
        # Calcul de l'ordonnée à l'origine (b)
        b = P3[1] - a * P3[0]
        
        # Générer les valeurs x pour tracer la droite
        x_vals = np.linspace(P3[0]-200, P3[0]+200, 100)  # Etend les x pour un tracé plus long
        y_vals = a * x_vals + b
        plt.plot(x_vals, y_vals, '--y')
        return (0,b)

import numpy as np
import matplotlib.pyplot as plt

def parallele_AB_C(P1, P2, P3, img, draw):
    # Calculer la pente de P1P2
    if P2[0] - P1[0] == 0:
        # Si P1P2 est verticale, la parallèle est aussi verticale
        x = P3[0]
        y1 = 0
        y2 = img.height
        # Dessiner la ligne verticale
        draw.line(xy=[(x, y1), (x, y2)], width=1, fill="yellow")
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


def plot_line_AB_(P1, P2):
    # Calcul de la pente de la droite P1P2
    a = (P2[1] - P1[1])/(P2[0] - P1[0])
    # Calcul de l'ordonnée à l'origine (b)
    b = P1[1] - a * P1[0]
    
    # Générer les valeurs x pour tracer la droite
    x_vals = np.linspace(P1[0]-200, P1[0]+200, 100)  # Etend les x pour un tracé plus long
    y_vals = a * x_vals + b

    # Tracer le segment
    #plt.plot((P1[0], P2[0]), (P1[1], P2[1]), color= 'yellow', marker='+')
    
    # Tracer la droite P1P2
    plt.plot(x_vals, y_vals, '--y')  # Tracé en jaune avec des tirets

import numpy as np

def plot_line_AB(P1, P2, img, draw):
    # Calculer la pente de la droite P1P2
    if P2[0] - P1[0] == 0:
        # Si P1P2 est verticale
        x = P1[0]
        y1 = 0
        y2 = img.height
        # Dessiner la ligne verticale
        draw.line(xy=[(x, y1), (x, y2)], width=1, fill="yellow")
    else:
        # Calculer la pente de la droite P1P2
        slope = (P2[1] - P1[1]) / (P2[0] - P1[0])
        # Calculer l'ordonnée à l'origine (b)
        intercept = P1[1] - slope * P1[0]

        if slope == 0:
            # Si P1P2 est horizontale
            y = intercept
            x1 = 0
            x2 = img.width
        else:
            # Calculer les points d'intersection avec les bords de l'image
            x1 = 0
            y1 = intercept
            x2 = img.width
            y2 = slope * img.width + intercept

        # Dessiner la ligne
        draw.line(xy=[(x1, y1), (x2, y2)], width=1, fill="yellow")


def intersect_AB_CD_(P1, P2, P3, P4):
    # Calcul de la pente de la droite P1P2
    a1 = (P2[1] - P1[1])/(P2[0] - P1[0])
    # Calcul de l'ordonnée à l'origine (b)
    b1 = P1[1] - a1 * P1[0]
    
    # Calcul de la pente de la droite P3P4
    a2 = (P4[1] - P3[1])/(P4[0] - P3[0])
    # Calcul de l'ordonnée à l'origine (b)
    b2 = P3[1] - a2 * P3[0]

    # Vérification si les droites sont parallèles
    if a1 == a2:
        return None  # Les droites sont parallèles, pas d'intersection
    
    # Calcul de l'intersection des deux droites
    x = (b2 - b1) / (a1 - a2)
    y = a1 * x + b1
    
    return (x, y)

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


def perpendiculaire_P1P2_P3_(P1, P2, P3):
    # Vérification du cas particulier où la perpendiculaire est verticale est vertical
    if (P1[1]-P2[1])/(P1[0]-P2[0])==0:
        # La parallèle sera une droite verticale passant par C
        x_vals = np.array([P3[0], P3[0]])  # x reste constant
        y_vals = np.array([P3[1] - 5, P3[1] + 5])  # Étend la droite sur l'axe y
        plt.plot(x_vals, y_vals, '--r')
        return (P3[0],0)
    else:
        # Calcul de la pente de la perpendiculaire
        a = -(P2[0] - P1[0])/(P2[1] - P1[1])
        # Calcul de l'ordonnée à l'origine (b)
        b = P3[1] - a * P3[0]
        
        # Générer les valeurs x pour tracer la droite
        x_vals = np.linspace(P3[0]-5, P3[0]+5, 10)  # Etend les x pour un tracé plus long
        y_vals = a * x_vals + b
        plt.plot(x_vals, y_vals, '--r')
        # Coordonnées d'un deuxième point autre que P3 sur la paralelle
        return (0,b)    

def perpendiculaire_P1P2_P3(P1, P2, P3, img, draw):
    # Vérification du cas particulier où P1P2 est horizontale
    if P2[0] - P1[0] == 0:
        # Si P1P2 est verticale, la perpendiculaire est horizontale
        y = P3[1]
        x1 = 0
        x2 = img.width
        # Dessiner la ligne horizontale
        draw.line(xy=[(x1, y), (x2, y)], width=1, fill="red")
        return (0, y)
    elif P2[1] - P1[1] == 0:
        # Si P1P2 est horizontale, la perpendiculaire est verticale
        x = P3[0]
        y1 = 0
        y2 = img.height
        # Dessiner la ligne verticale
        draw.line(xy=[(x, y1), (x, y2)], width=1, fill="red")
        return (x, 0)
    else:
        # Calcul de la pente de P1P2
        slope_P1P2 = (P2[1] - P1[1]) / (P2[0] - P1[0])
        # La pente de la perpendiculaire est l'opposé de l'inverse de la pente de P1P2
        slope_perp = -1 / slope_P1P2
        # Calcul de l'ordonnée à l'origine (b) de la perpendiculaire passant par P3
        intercept = P3[1] - slope_perp * P3[0]

        # Calculer les points d'intersection de la perpendiculaire avec les bords de l'image
        if slope_perp == 0:
            # Ligne horizontale
            y = intercept
            x1 = 0
            x2 = img.width
        else:
            # Calculer les points d'intersection avec les bords gauche et droit de l'image
            x1 = 0
            y1 = intercept
            x2 = img.width
            y2 = slope_perp * img.width + intercept

        # Dessiner la ligne perpendiculaire
        draw.line(xy=[(x1, y1), (x2, y2)], width=1, fill="red")
        return (0, intercept)


def distance_A_B(A, B):
    return ((A[0] - B[0])**2 + (A[1] - B[1])**2)**0.5

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

def calcul(Diam, Long, A, B, C, D, E, F, G, H, I, P, Q, R, S, img, draw):
    
    # Etape 2 : longueur poro
    
    J = intersect_AB_CD(A, H, B, I)
    print ("J : ", J)
    K = parallele_AB_C(A, B, J, img, draw)
    print ("K : ", K)
    L = parallele_AB_C(A, B, G, img, draw)
    M = intersect_AB_CD(K, D, G, L)
    N = intersect_AB_CD(K, E, G, L)
    O = intersect_AB_CD(K, F, G, L)
    long_poro = (distance_A_B(N, O)/distance_A_B(M, G))*Long
    print ("longueur poro : ", (distance_A_B(N, O)/distance_A_B(M, G))*Long)
    
    # Etape 3 : largeur poro
    
    T = intersect_AB_CD(K, P, G, L)
    U = intersect_AB_CD(K, Q, G, L)
    V = intersect_AB_CD(K, R, G, L)
    W = intersect_AB_CD(K, S, G, L)
    coef = distance_A_B(C, G)/distance_A_B(P, Q)
    larg_poro = (distance_A_B(V, W)/distance_A_B(M, G))*Long*coef**2    
    print ("largeur poro : ", (distance_A_B(V, W)/distance_A_B(M, G))*Long*coef**2)
    #larg_poro = (distance_A_B(V, W)/distance_A_B(T, U))*Diam
    #print ("largeur poro : ", (distance_A_B(V, W)/distance_A_B(T, U))*Diam)
    print("coef : ", coef)
    print("PQ : ", distance_A_B(P, Q))
    print("CG : ", distance_A_B(C, G))
    return long_poro, larg_poro, J, K, M, T, N, V, W, O, U
