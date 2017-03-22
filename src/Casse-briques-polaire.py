#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import sin, cos
from tkinter import *
from random import random
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



# On crée la barre qui nous servira à jouer
barre_largeur = 100
barre_hauteur = 10

barre_départ_x, barre_départ_y = (largeur_fen - barre_largeur)/2, hauteur_fen - 25 - barre_hauteur
# Au départ :
# - la barre est au milieu en abscisse
# - la barre est séparée du bas de la fenêtre par 25 pixels

barre = fond.create_rectangle(
    barre_départ_x, barre_départ_y,
    barre_départ_x + barre_largeur, barre_départ_y + barre_hauteur,
    fill='#3f51b5', width=2
)







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
bouton_marche_arrêt.place(x=25,y=25)


joueur_points = 42 # TODO








balle_rayon = 15
balle_x_initial = largeur_jeu / 2
balle_y_initial = hauteur_jeu - 100

# Vecteur vitesse en coordonnées polaires.
balle_vitesse = .5 # vitesse en pixels par image (*frame* en anglais)
balle_direction = 45 # 0° = vers la droite, comme pour le cercle trigonométrique standard

balle = fond.create_oval(balle_x_initial, balle_y_initial,
                        balle_x_initial, balle_y_initial,
                        fill='#9c27b0', width=balle_rayon)





# Initialisation des briques
# liste briques_vies = [] # 1 dimension
# liste briques = [élements de canvas: Rectangle…] # 1 dimension
# liste briques_coords = [Tuple…] # (x, y)
# -> NOTE peut-être implémenter un modèle de grille
#         c'est-à-dire on n'utilise pas les vraies coords des briques
#         mais plutôt une grille virtuelle qu'on transformera

'''
         42 pixels
         3 colonnes            => largeur colonne = 42 / 3 pixels
    <----------------->
    | 1,1 | 1,2 | 1,3 | …
    | 2,1 | 2,2 | 2,3 | …
    | 3,1 | 3,2 | 3,3 | …
'''

brique_largeur = 70
brique_hauteur = 30
def créer_brique(x, y, dureté=1, couleur="#d32f2f"):
    fond.create_rectangle(
        x, y,
        x + brique_largeur, y + brique_hauteur,
        fill=couleur, width=2)

for x in range(50, largeur_jeu - 50, int((largeur_jeu - 2*50)/5)):
    créer_brique(x, 60)
    créer_brique(x, 160)
    créer_brique(x+50, 110)    
    créer_brique(x+50, 210)





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


def déplacer_balle(dt):
    # global balle_vitesse_x, balle_vitesse_y, joueur_vies_restantes
    global balle_direction, joueur_vies_restantes
    x, y, x2, y2 = fond.coords(balle)

    # Gestion des rebonds avec la barre
    barre_x1, barre_y1, barre_x2, barre_y2 = fond.coords(barre)
    '''
        y1 -
        x1[===============]x2
        y2 -
    '''

    # Il ne peut y avoir collision entre la balle et la barre que
    # - si la balle a une abscisse entre x1 et x2
    # - si la balle a une ordonnée entre y1 et y2

    if (barre_x1 - balle_rayon/2 < x < barre_x2 + balle_rayon/2) and (barre_y1 - balle_rayon/2 < y < barre_y2):
        # balle_vitesse_y = -balle_vitesse_y
        # y = barre_y1 - balle_rayon/2

        balle_direction = 180 - balle_direction



    # Gestion des rebonds avec le cadre

    # On traite chaque cas séparement pour replacer la balle au bon endroit si elle sort du cadre.
    # En effet, si elle sort du cadre, alors le vecteur vitesse peut la forcer à rester en dehors.

    if x < balle_rayon/2:
        balle_direction = -balle_direction
        x = balle_rayon/2

    if x > largeur_jeu - balle_rayon/2:
        balle_direction = -balle_direction
        x = largeur_jeu - balle_rayon/2

    if y < balle_rayon/2:
        balle_direction = 180 - balle_direction # π - θ
        y = balle_rayon/2

    if y > hauteur_jeu - balle_rayon/2:
        balle_direction = 180 - balle_direction
        y = hauteur_jeu - balle_rayon/2


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
    x2 = x + balle_vitesse * cos(balle_direction * -PI/180 + PI/2) * dt
    y2 = y + balle_vitesse * sin(balle_direction * -PI/180 + PI/2) * dt
    fond.coords(balle, (x2, y2, x2, y2)) # on déplace la balle sur l'écran


    # fond.coords(balle, (x2, y2, x2, y2)) # on déplace la balle

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
