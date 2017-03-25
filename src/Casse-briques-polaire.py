#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import sin, cos
from tkinter import *
from random import random, randrange
from math import pi as PI
import time

# import PIL
# from PIL import Image, ImageTk

import os
chemin_absolu = os.path.abspath(__file__)
nom_dossier = os.path.dirname(chemin_absolu)
os.chdir(nom_dossier)




fen = Tk() # On crée la fenêtre
fen.title("Y'a qu'a casser des briques") # On nomme la fenêtre

largeur_fen = 700
hauteur_fen = 700

# On définit les dimensions de la zone de jeu.
largeur_jeu = 600 # qui est aussi la largeur de l'image
hauteur_jeu = 700 # qui est aussi la hauteur de l'image

fen.geometry(str(largeur_fen) + "x" + str(hauteur_fen) + "+0+0") # on redimensionne la fenêtre
# et on l'affiche au premier plan
fen.lift()
fen.attributes('-topmost', 1)
fen.after(25, lambda: fen.attributes('-topmost', 0))

# On crée un canvas
fond = Canvas(fen, width=largeur_fen, height=hauteur_fen, bg='#b0bec5', bd=3)
fond.place(x=0, y=0)

# On ouvre notre image qui sera le fond du canvas.
# chemin_image_fond = os.getcwd() + '/../img/isn2.png'
# image_fond = PIL.ImageTk.PhotoImage(PIL.Image.open(chemin_image_fond))
# fond.create_image(0, 0, anchor=NW, image=image_fond)






def jouer():
    global jeu_en_cours
    jeu_en_cours = True

# On crée les boutons
Bouton_jouer = Button(fen, text='Jouer', command=jouer)
Bouton_jouer.place(x=largeur_jeu + 20,y=590)

B2 = Button(fen,text='Quitter', command=fen.destroy)
B2.place(x=largeur_jeu + 15,y=650)






# TODO afficher les vies restantes
# TODO afficher les points

# Informations à propos du joueur
joueur_vies_restantes = 3
jeu_en_cours = False # Le jeu commence quand la fonction jouer est appelée (bouton).

def marche_arrêt():
    global jeu_en_cours
    jeu_en_cours = not jeu_en_cours

    if jeu_en_cours == True:
        bouton_marche_arrêt.config(text='Pause')

    else:
        bouton_marche_arrêt.config(text='Continuer')





bouton_marche_arrêt = Button(fen,text='Pause', command=marche_arrêt)
bouton_marche_arrêt.place(x=largeur_fen - 75,y=25)


joueur_points = 42 # TODO












balle_rayon = 15
balle_x_initial = largeur_jeu / 2
balle_y_initial = hauteur_jeu - 100

# Vecteur vitesse en coordonnées polaires.
balle_vitesse = .4 # vitesse (unité ?)
balle_direction = 32 # 90° = vers la droite

balle = fond.create_oval(balle_x_initial, balle_y_initial,
                        balle_x_initial + 2*balle_rayon, balle_y_initial + 2*balle_rayon,
                        fill='#e91e63', width=1) # #9c27b0




# On crée la barre qui nous servira à jouer
barre_largeur = (largeur_jeu/2) * balle_vitesse
barre_hauteur = 15

barre_départ_x, barre_départ_y = (largeur_fen - barre_largeur)/2, hauteur_fen - 25 - barre_hauteur
# Au départ :
# - la barre est au milieu en abscisse
# - la barre est séparée du bas de la fenêtre par 25 pixels

barre = fond.create_rectangle(
    barre_départ_x, barre_départ_y,
    barre_départ_x + barre_largeur, barre_départ_y + barre_hauteur,
    fill='#3f51b5', width=0
)




## Initialisation des briques
# liste briques_duretés = [Entiers…] # 1 dimension
# liste briques_rect = [Rectangles (élements de canvas)…]
# liste briques_coords = [Tuples…]

briques_duretés = []
briques_rect    = []
briques_coords  = []

# Modèle de grille vs. pixels
# On n'utilise pas les vraies coords des briques, mais plutôt une grille virtuelle qu'on transformera.

# La largeur d'une brique est calculée en fonction de la largeur de l'écran de jeu,
# auquel on retire une espacement sur tous les côtés (2×8px).
brique_largeur = (largeur_jeu - 2*8) / 10 # soit 10 briques de largeur
brique_hauteur = (hauteur_jeu - 2*8) / 25 # soit 25 briques de hauteur

def couleur_dureté(dureté):
    if dureté == 0:
        return '#fdd'
    elif dureté == 1:
        return '#f88'
    elif dureté == 2:
        return '#f44'
    elif dureté == 3:
        return '#f00'
    else:
        return '#ff0'

# `ligne` et `colonne` sont les coordonnées des briques en coordonnées de grille (et non pas en pixels)
def créer_brique(ligne, colonne, dureté=1, couleur="#d32f2f"):
    # TODO: couleur en fonction de la dureté
    couleur = couleur_dureté(dureté)

    # Si `ligne` est impair, alors on décale les briques d'une demi-brique vers la gauche (`colonne`)
    if ligne % 2 == 1: # opérateur modulo, soit ici le reste de la division euclidienne par 2
        colonne -= 0.5 # on retire une demi-brique horizontalement

    # On calcule les coordonnées réelles en pixels,
    # et on ajoute une légère marge avec les bords de la fenêtre (+8px)
    x, y = colonne * brique_largeur + 8, ligne * brique_hauteur + 8
    x2, y2 = x + brique_largeur, y + brique_hauteur,
    brique = fond.create_rectangle(x, y, x2, y2, fill=couleur, width=2)

    # On ajoute un 4-uplets (x, y, x+larg, y+haut) à la liste des dimensions
    briques_rect.append(brique)
    briques_duretés.append(dureté)
    briques_coords.append( (x, y, x2, y2) )

# `ligne` commence à 1 pour permettre à la balle d'aller au-dessus des briques
# (et donc permettre une mécanique de jeu plus stratégique, ou le but sera alors
# de placer la balle au-dessus des briques pour faire un maximum de points
# en diminuant le risque de perdre une balle).
for ligne in range(1, 15):
    for colonne in range(1, 10):
        créer_brique(ligne, colonne, dureté=randrange(0,4))

    # Si le numéro de ligne est impair, on ajoute une brique de plus en largeur pour compléter le motif créé par décalage d'une demi-brique vers la gauche.
    if ligne % 2 == 1:
        créer_brique(ligne, 10)

# créer_brique(12.5, 4.5)



# NOTE : à retirer on attend pas que le joueur clique sur [Jouer]
jouer()







def déplacer_barre(event):
    xS, yS = event.x, event.y # on récupère les coordonnées de la souris

    # On calcule la nouvelle position x de la barre :
    # xA = xS - barre_largeur/2 : on définit la position de la souris comme le milieu de la barre
    # xA + barre_largeur == xS + barre_largeur/2
    xA = xS - barre_largeur/2
    '''
       xA     xS    (xA + largeur)
        +------------+
        |            |
        +------------+
    '''


    if xA < 0: # si la barre est trop à gauche
        xA = 0
    elif xA > largeur_jeu - barre_largeur: # si la barre est trop à gauche
        '''
                 xA +
            |       [===-===]|
                    + larg_fen - larg_barre
        '''
        xA = largeur_jeu - barre_largeur
    # en hauteur, aucun problème évidemment

    fond.coords(barre, (xA, barre_départ_y, xA + barre_largeur, barre_départ_y + barre_hauteur)) # on déplace la barre


def gestion_collisions_balle_briques():
    global balle_direction

    # Variables utilisées plus bas (collision)
    Mink_largeur, Mink_longueur = (2*balle_rayon + brique_largeur)/2, (2*balle_rayon + brique_hauteur)/2

    for index, brique_coords in enumerate(briques_coords):
        # if briques_duretés[index] == 0:
        #     continue # ne pas gérer les briques détruites
        #     # ceci ne pose pas de problèmes de performances,
        #     # puisqu'il n'y a, au maximum, que 200-300 briques.

        balle_x, balle_y, balle_x2, balle_y2 = fond.coords(balle)
        brique_x, brique_y, brique_x2, brique_y2 = brique_coords

        # On détecte de quel côté s'est produit la collision à l'aide de la somme de Minkowski
        # https://fr.wikipedia.org/wiki/Somme_de_Minkowski
        # On considère la balle comme un rectangle.
        # On calcule la somme de Minkowski des rectangles `balle` et `brique`, qui est un nouveau rectangle.
        # On regarde où le centre du rectangle 'balle` est par rapport au nouveau rectangle (pour savoir s'il y a eu collision) et par rapport aux diagonales du nouveau rectangle (pour déterminer où la collision s'est produite).

        Mink_diff_x = (balle_x + balle_x2)/2 - (brique_x + brique_x2)/2
        Mink_diff_y = (balle_y + balle_y2)/2 - (brique_y + brique_y2)/2

        # collision = (brique_x < balle_x < balle_x2 < brique_x2) and (brique_y < balle_y < balle_y2 < brique_y2)
        collision = (abs(Mink_diff_x) <= Mink_largeur) and (abs(Mink_diff_y) <= Mink_longueur)

        # Gestion du rebond
        if collision:
            Mink_larg_transversale = Mink_largeur * Mink_diff_y
            Mink_haut_transversale = Mink_longueur * Mink_diff_x

            if (Mink_larg_transversale > Mink_haut_transversale):
                if (Mink_larg_transversale > -Mink_haut_transversale):
                    # print('bas')
                    balle_direction = 180 - balle_direction
                else:
                    # print('gauche')
                    balle_direction = -balle_direction
            else:
                if (Mink_larg_transversale > -Mink_haut_transversale):
                    # print('droite')
                    balle_direction = -balle_direction
                else:
                    # print('haut')
                    balle_direction = 180 - balle_direction

        # Gestion de la brique
        if collision:
            # destruction de la brique si elle n'a plus de dureté
            if briques_duretés[index] == 0:
                fond.delete(briques_rect[index])
                briques_rect.pop(index)
                briques_duretés.pop(index)
                briques_coords.pop(index)

            # sinon perte d'une vie et changement de couleur
            else:
                briques_duretés[index] -= 1
                fond.itemconfig(briques_rect[index], fill=couleur_dureté(briques_duretés[index]))

    # briques_rect
    # briques_duretés  # briques_coords

def déplacer_balle(dt):
    # global balle_vitesse_x, balle_vitesse_y, joueur_vies_restantes
    global balle_direction, joueur_vies_restantes
    x, y, x2, y2 = fond.coords(balle)

    # Gestion des rebonds avec la barre
    barre_x, barre_y, barre_x2, barre_y2 = fond.coords(barre)
    '''
                y
        x[==============]x2
                y2
    '''

    # Il ne peut y avoir collision entre la balle et la barre que
    # - si la balle a une abscisse entre x1 et x2
    # - si la balle a une ordonnée entre y1 et y2

    collision_barre_x = barre_x <= x2 and barre_x2 >= x
    collision_barre_y = y2 >= barre_y and y < barre_y + balle_vitesse

    if collision_barre_x and collision_barre_y:
        balle_direction = 180 - balle_direction

        # TODO: À corriger
        # False si la collision se fait du côté droit, True si du côté gauche
        # collision_barre_milieu = barre_x - balle_rayon < (x + x2)/2 < barre_x + barre_largeur/2 - balle_rayon
        # if collision_barre_milieu == False:
        #     print(balle_direction)
        #     balle_direction = -balle_direction



    # Gestion des rebonds avec le cadre
    # On traite chaque cas séparement pour replacer la balle au bon endroit si elle sort du cadre.
    # En effet, si elle sort du cadre, alors le vecteur vitesse peut la forcer à rester en dehors.

    if x < balle_rayon:
        balle_direction = -balle_direction
        x = balle_rayon

    if x > largeur_jeu - balle_rayon:
        balle_direction = -balle_direction
        x = largeur_jeu - balle_rayon

    if y < balle_rayon:
        balle_direction = 180 - balle_direction # π - θ
        y = balle_rayon

    if y > hauteur_jeu - balle_rayon:
        balle_direction = 180 - balle_direction
        y = hauteur_jeu - balle_rayon


        # À DÉPLACER
        marche_arrêt() # pause
        joueur_vies_restantes -= 1 # le joueur perd une vie

        balle_direction = (random() - 0.5) * 90
        x, y = balle_x_initial, balle_y_initial

        if joueur_vies_restantes == 0:
            # message=fond.create_text('oooo')
            Bouton_jouer.config(text='Rejouer')
            #a refaire pour que ça fonctionne
            #bouton_marche_arrêt(state=DISABLED)

        # TODO gestion de la défaite (joueur_vies_restantes == 0)
        # TODO Afficher message pour relancer la balle
        # NOTE On ne remet pas les briques déjà touchées quand le joueur perd une vie




    # Gestion des collisions avec les briques
    # for brique in briques:
        # brique_x, brique_y = …
        # if collision(…):
            # la brique perd une vie -> matrices des vies de chaque brique

    gestion_collisions_balle_briques()





    # Application du vecteur vitesse
    # Pas d'accélération ici, on ne se place pas dans des conditions réelles (pas de gravité)
    # Ici, le dt sert à conserver une animation fluide (en théorie)

    # balle_direction = balle_direction % 360


    # Conversion degrés -> radians : α = θ * 2π/360° = θ * π/180°
    # Transformation pour que l'angle corresponde à la mesure principale
    # dans le cercle trigonométrique: β = -α + π/2
    # On obtient les coordonnées du vecteur selon :
    # v_x = ||v⃗|| × cos(β)
    # v_y = ||v⃗|| × sin(β)
    # Puis on les ajoute à la position de la balle
    x_nouveau = x + balle_vitesse * cos(balle_direction * PI/180 + PI/2) * dt
    y_nouveau = y + balle_vitesse * sin(balle_direction * PI/180 + PI/2) * dt
    fond.coords(balle, (x_nouveau, y_nouveau, x_nouveau + 2*balle_rayon, y_nouveau + 2*balle_rayon)) # on déplace la balle sur l'écran

temps_actuel = time.time() # Sert à garder la valeur de temps, de l'image (frame) précédente.
def boucle_de_jeu():
    # On relance une boucle de jeu, qui sera exécutée plus tard.
    # On vise ici 100 images par seconde
    fen.after(round(1000/100), boucle_de_jeu)


    global temps_actuel

    # On calcule la différence de temps ∆t afin de simuler la physique de manière fluide.
    dt = 1000 * (temps_actuel - time.time()) # en millisecondes
    temps_actuel = time.time()

    # si le jeu est en pause, on ne déplace pas la balle
    if jeu_en_cours == False:
        return # on quitte la fonction

    # fond.move(barre, +3, 0)
    déplacer_balle(dt)


fen.after(round(1000/60), boucle_de_jeu)

# On attache l'événement associé au déplacement de la souris
# au gestionnaire du déplacement de la barre de jeu.
fen.bind('<Motion>', déplacer_barre)

def événement_clic(event):
    if jeu_en_cours == False:
        marche_arrêt()

fen.bind("<Button-1>", événement_clic)


fen.mainloop()
