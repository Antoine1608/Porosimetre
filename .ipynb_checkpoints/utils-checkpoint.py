import numpy as np
import matplotlib.pyplot as plt

# fonction pour tracer une médiatrice d'un segment AB
def plot_mediatrice_AB(A, B):
    # Calcul du milieu du segment AB
    I = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    
    # Vérification du cas particulier où le segment AB est vertical
    if A[0] == B[0]:
        # La médiatrice sera une droite horizontale passant par le milieu
        x_vals = np.array([I[0] - 5, I[0] + 5])  # Étend la droite sur l'axe x
        y_vals = np.array([I[1], I[1]])  # x reste constant

    else:
        # Calcul de la pente de la médiatrice
        a = -(B[0] - A[0]) / (B[1] - A[1])
        # Calcul de l'ordonnée à l'origine (b)
        b = I[1] - a * I[0]
        
        # Générer les valeurs x pour tracer la droite
        x_vals = np.linspace(A[0]+700, B[0]-700, 100)  # Etend les x pour un tracé plus long
        y_vals = a * x_vals + b

    # Tracer la médiatrice
    plt.plot(x_vals, y_vals, '--y')  # Tracé en rouge avec des tirets

# trace la parallèle à P1P2 passant par P3
def parallele_AB_C(P1, P2, P3):
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

def plot_line_AB(P1, P2):
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

def intersect_AB_CD(P1, P2, P3, P4):
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

def perpendiculaire_P1P2_P3(P1, P2, P3):
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

def distance_A_B(A, B):
    return ((A[0] - B[0])**2 + (A[0] - B[0])**2)**0.5

def calcul(Diam, Long, A, B, C, D, E, F, G, H, I, P, Q, R, S):
    
    # Etape 2 : longueur poro
    
    J = intersect_AB_CD(A, H, B, I)
    print ("J : ", J)
    K = parallele_AB_C(A, B, J)
    print ("K : ", K)
    L = parallele_AB_C(A, B, G)
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
    larg_poro = (distance_A_B(V, W)/distance_A_B(T, U))*Diam
    print ("largeur poro : ", (distance_A_B(V, W)/distance_A_B(T, U))*Diam)
    return long_poro, larg_poro, J, K, M, T, N, V, W, O, U


