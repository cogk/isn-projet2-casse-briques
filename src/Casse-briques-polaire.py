#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO afficher les vies restantes


from math import sin, cos
from tkinter import *
from random import random, randrange
from math import pi as PI
import time

import PIL
from PIL import Image, ImageTk

import os
chemin_absolu = os.path.abspath(__file__) # où est situé ce fichier
nom_dossier = os.path.dirname(chemin_absolu) # dans quel dossier
os.chdir(nom_dossier) # on se déplace dans ce dossier-là




fen = Tk() # On crée la fenêtre
fen.title("Y'a qu'a casser des briques") # On nomme la fenêtre

# largeur_fen = 700
# hauteur_fen = 700

# On définit les dimensions de la zone de jeu.
largeur_fen = largeur_jeu = 600 # qui est aussi la largeur de l'image
hauteur_fen = hauteur_jeu = 700 # qui est aussi la hauteur de l'image

fen.geometry(str(largeur_fen) + "x" + str(hauteur_fen) + "+0+0") # on redimensionne la fenêtre

# fen.attributes('-topmost', 1) # et on l'affiche au premier plan

# On crée un canvas
fond = Canvas(fen, width=largeur_fen, height=hauteur_fen, bg='#b0bec5', bd=3)
fond.place(x=0, y=0)

# On ouvre notre image qui sera le fond du canvas.
chemin_image_fond = os.getcwd() + '/../img/isn2.png'
image_fond = PIL.ImageTk.PhotoImage(PIL.Image.open(chemin_image_fond))
fond.create_image(0, 0, anchor=NW, image=image_fond)






def jouer():
    global jeu_en_cours
    jeu_en_cours = True

# On crée les boutons
# Bouton_jouer = Button(fen, text='Jouer', command=jouer)
# Bouton_jouer.place(x=largeur_jeu + 20, y=590)

# Bouton_quitter = Button(fen,text='Quitter', command=fen.destroy)
# Bouton_quitter.place(x=largeur_jeu + 15, y=650)


jeu_en_cours = False # Le jeu commence quand la fonction jouer est appelée (bouton).
def marche_arrêt():
    global jeu_en_cours
    jeu_en_cours = not jeu_en_cours

#     if jeu_en_cours == True:
#         bouton_marche_arrêt.config(text='Pause')
#
#     else:
#         bouton_marche_arrêt.config(text='Continuer')
#
#
# bouton_marche_arrêt = Button(fen,text='Pause', command=marche_arrêt)
# bouton_marche_arrêt.place(x=largeur_fen - 75,y=25)



# Informations à propos du joueur
joueur_vies_restantes = 3
Label_vies = Label(fen, text='Vies: %i' % joueur_vies_restantes, fg="#3f51b5", font=(None, 20))
Label_vies.place(x=10, y=10)


def nouvelle_partie():
    global joueur_vies_restantes, balle_direction
    joueur_vies_restantes = 3
    jeu_en_cours = False
    Label_vies.config(text='Vies: %i' % joueur_vies_restantes)
    Bouton_rejouer.pack_forget()
    Label_perdu.pack_forget()
    Label_gagné.pack_forget()

    balle_direction = (random() - 0.5) * 90
    x, y = balle_x_initial, balle_y_initial
    fond.coords(balle, (x, y, x + 2*balle_rayon, y + 2*balle_rayon))

    créer_briques()

Bouton_rejouer = Button(fen, text='Rejouer', command=nouvelle_partie)
Bouton_rejouer.pack_forget()

Label_perdu = Label(fen, text='Perdu :(', fg="red", font=(None, 30))
Label_perdu.pack_forget()

Label_gagné = Label(fen, text='Gagné !', fg="green", font=(None, 30))
Label_gagné.pack_forget()

def partie_perdue():
    Bouton_rejouer.pack()
    Label_perdu.pack(side = BOTTOM)

def partie_gagnée():
    Bouton_rejouer.pack()
    Label_gagné.pack(side = BOTTOM)


balle_rayon = 15
balle_x_initial = largeur_jeu / 2
balle_y_initial = hauteur_jeu - 100

# Vecteur vitesse en coordonnées polaires.
balle_vitesse = 0.5 # vitesse (unité ?)
balle_direction = 32 # 90° = vers la droite

balle = fond.create_oval(balle_x_initial, balle_y_initial,
                        balle_x_initial + 2*balle_rayon, balle_y_initial + 2*balle_rayon,
                        fill='#e91e63', width=1) # #9c27b0




# On crée la barre qui nous servira à jouer
barre_largeur = 150
barre_hauteur = 15

barre_départ_x, barre_départ_y = (largeur_jeu - barre_largeur)/2, hauteur_jeu - 25 - barre_hauteur
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
        return '#944'
    elif dureté == 1:
        return '#733'
    elif dureté == 2:
        return '#522'
    elif dureté == 3:
        return '#400'
    else:
        return '#f00'

# `ligne` et `colonne` sont les coordonnées des briques en coordonnées de grille (et non pas en pixels)
def créer_brique(ligne, colonne, dureté=1):
    couleur = couleur_dureté(dureté)

    # Si `ligne` est impair, alors on décale les briques d'une demi-brique vers la gauche (`colonne`)
    # pour avoir un effet "mur".
    if ligne % 2 == 1: # opérateur modulo, soit ici le reste de la division euclidienne par 2 #SpécialitéMaths
        colonne -= 0.5 # on retire une demi-brique horizontalement

    # On calcule les coordonnées réelles en pixels (en fonction de la grille),
    # et on ajoute une légère marge avec les bords de la fenêtre (+8px).
    x, y = colonne * brique_largeur + 8, ligne * brique_hauteur + 8
    x2, y2 = x + brique_largeur, y + brique_hauteur
    brique = fond.create_rectangle(x, y, x2, y2, fill=couleur, width=2)

    # On ajoute l'objet Tkinter à la liste des rectangles Tkinter.
    briques_rect.append(brique) # pourquoi ? -> pour supprimer le rectangle quand la brique est cassée

    # On ajoute la dureté de la brique à une autre liste.
    briques_duretés.append(dureté)

    # On ajoute un 4-uplet (x, y, x+larg, y+haut) à la liste des coordonnées, pour simplifier le travail plus bas #collision.
    briques_coords.append( (x, y, x2, y2) )


def créer_briques(l_min = 3, l_max = 13, c_min = 1, c_max = 9):
    for ligne in range(l_min, l_max):
        for colonne in range(c_min, c_max):
            créer_brique(ligne, colonne, dureté=randrange(0,4))

            # Si le numéro de ligne est impair, on ajoute une brique de plus en largeur pour compléter le motif créé par décalage d'une demi-brique vers la gauche.
            if ligne % 2 == 1:
                créer_brique(ligne, c_max)

nouvelle_partie()





















# Cette fonction est appelée à chaque déplacement de la souris.
def déplacer_barre(event):
    x_souris, y_souris = event.x, event.y # on récupère les coordonnées de la souris

    # On calcule la nouvelle position x de la barre :
    # xA = x_souris - barre_largeur/2 : on définit la position de la souris comme le milieu de la barre
    # xA + barre_largeur == x_souris + barre_largeur/2
    xA = x_souris - barre_largeur/2
    '''     x_souris
       xA      +      (xA + largeur)
        +-------------+
        |             |  barre
        +-------------+
    '''


    if xA < 0: # si la barre est trop à gauche
        xA = 0
    elif xA > largeur_jeu - barre_largeur: # si la barre est trop à droite
        '''
                 xA +
            |       [===-===]|
                    + larg_fen - larg_barre
        '''
        xA = largeur_jeu - barre_largeur

    # en hauteur, aucun problème évidemment

    fond.coords(barre, (xA, barre_départ_y, xA + barre_largeur, barre_départ_y + barre_hauteur)) # on déplace la barre


# Cette fonction détecte le côté où se produit la collision, et fait rebondir la balle.
def gestion_collisions_balle_briques():
    global balle_direction # Il nous faut la directon de la balle pour la changer.
    balle_x, balle_y, balle_x2, balle_y2 = fond.coords(balle)

    # Variables utilisées plus bas (collision)
    Mink_largeur, Mink_longueur = (2*balle_rayon + brique_largeur)/2, (2*balle_rayon + brique_hauteur)/2

    for index, brique_coords in enumerate(briques_coords):
        brique_x, brique_y, brique_x2, brique_y2 = brique_coords

        # On détecte de quel côté s'est produit la collision à l'aide de la somme de Minkowski
        # https://fr.wikipedia.org/wiki/Somme_de_Minkowski
        # http://allenchou.net/wp-content/uploads/2013/12/Minkowski-Sum-Circle-Rect.png
        # On considère la balle comme un rectangle.
        # On calcule la somme de Minkowski des rectangles `balle` et `brique`, qui est un nouveau rectangle.
        # On regarde où le centre du rectangle `balle` est par rapport au nouveau rectangle (pour savoir s'il y a eu collision) et par rapport aux diagonales du nouveau rectangle (pour déterminer où la collision s'est produite).

        centre_balle_x, centre_balle_y = (balle_x + balle_x2)/2, (balle_y + balle_y2)/2
        centre_brique_x, centre_brique_y = (brique_x + brique_x2)/2, (brique_y + brique_y2)/2

        Mink_diff_x = centre_balle_x - centre_brique_x
        Mink_diff_y = centre_balle_y - centre_brique_y

        # collision = (brique_x < balle_x < balle_x2 < brique_x2) and (brique_y < balle_y < balle_y2 < brique_y2)
        collision = (abs(Mink_diff_x) <= Mink_largeur) and (abs(Mink_diff_y) <= Mink_longueur)

        # Gestion du rebond
        if collision:
            Mink_diagonale_x = Mink_largeur * Mink_diff_y
            Mink_diaonale_y = Mink_longueur * Mink_diff_x

            if (Mink_diagonale_x > Mink_diaonale_y):
                if (Mink_diagonale_x > -Mink_diaonale_y):
                    # print('bas')
                    balle_direction = 180 - balle_direction
                else:
                    # print('gauche')
                    balle_direction = -balle_direction
            else:
                if (Mink_diagonale_x > -Mink_diaonale_y):
                    # print('droite')
                    balle_direction = -balle_direction
                else:
                    # print('haut')
                    balle_direction = 180 - balle_direction

        # Gestion de la brique
        if collision:
            # perte d'un point de dureté et changement de couleur si elle a encore de la dureté
            if briques_duretés[index] > 0:
                briques_duretés[index] -= 1
                fond.itemconfig(briques_rect[index], fill=couleur_dureté(briques_duretés[index]))

            # destruction de la brique si elle n'a plus de dureté
            else:
                fond.delete(briques_rect[index]) # on détruit le rectangle Tkinter (qui est affiché)
                # On retire la brique de toutes les listes.
                briques_rect.pop(index)
                briques_duretés.pop(index)
                briques_coords.pop(index)

                if len(briques_rect) == 0: # fonctionne aussi avec les autres listes
                    partie_gagnée()





def déplacer_balle(dt):
    # global balle_vitesse_x, balle_vitesse_y, joueur_vies_restantes
    global balle_direction, joueur_vies_restantes
    x, y, x2, y2 = fond.coords(balle)


    # Vas-y joues tout seul
    # class Struct:
    #     def __init__(self, **entries):
    #         self.__dict__.update(entries)
    # _coords = {'x': x, 'y':0}
    # event = Struct(**_coords)
    # déplacer_barre(event)

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

        # Perte d'une vie
        marche_arrêt() # pause
        joueur_vies_restantes -= 1 # le joueur perd une vie

        # On remet la balle à sa place initiale
        balle_direction = (random() - 0.5) * 90
        x, y = balle_x_initial, balle_y_initial

        Label_vies.config(text='Vies: %d' % joueur_vies_restantes)

        if joueur_vies_restantes == 0:
            partie_perdue()

    # Gestion des collisions avec les briques
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

    # Si le jeu est en pause, on ne déplace pas la balle.
    if jeu_en_cours == False or joueur_vies_restantes == 0:
        return # on quitte la fonction

    déplacer_balle(dt)


fen.after(5, boucle_de_jeu) # On lance le jeu

# On attache l'événement associé au déplacement de la souris
# au gestionnaire du déplacement de la barre de jeu.
fen.bind('<Motion>', déplacer_barre)

def événement_clic(event):
    if jeu_en_cours == False:
        marche_arrêt()

fen.bind("<Button-1>", événement_clic)


fen.mainloop()
