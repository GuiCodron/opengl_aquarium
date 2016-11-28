import sys

import OpenGL.GL as GL
import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
import math
import numpy as np
import random
from Ship import Ship
from Snake import Snake
from Element import Element


# fonction 'init' regroupant des appels de fonction a n'executer qu'une fois au
# demarrage du programme.
def init():
    # nettoyage du buffer image :
    GL.glClearColor(0.0, 0.0, 0.0, 0.0)
    # on autorise l'interpolation de couleur :
    GL.glShadeModel(GL.GL_SMOOTH)
    # on autorise le test en profondeur :
    GL.glEnable(GL.GL_DEPTH_TEST)
    timerFunc()
    key_update()


# fonction reshape de GLUT. Executee a chaque modification de la fenetre de rendu.
def reshape(width, height):
    # parametrage du viewport :
    GL.glViewport(0, 0, width, height)
    # reinitialisation de la projection :
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    # projection perspective :
    fAspect = width / height
    # utilisation de la fonction gluPerspective de GLU (voir documentation).
    # Les deux derniers parametres sont les plans de clipping (near, far) et sont
    # des valeurs positives. Note: 'near' ne doit pas etre nul.
    GLU.gluPerspective(60.0, fAspect, 1.0, 2000.0)
    # placement de la camera :
    # on utilise la fonction gluLookAt de GLU.
    GLU.gluLookAt(0, 0.0, 180.0, 0.0, 0.0, 0.0, 0, 1, 0)


# fonction display de GLUT. Contient le code a executer pour faire un nouveau rendu.
def display():

    # nettoyage des buffers d'image et de profondeur :
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    ############################## A COMPLETER ################################

    myShip.place_camera()
    myShip.draw()

    for enemy in enemies:
        enemy.draw()

    ###########################################################################

    # on force OpenGL a executer toutes les commandes :
    GL.glFlush()
    # ligne suivante a decommenter pour echanger les deux buffers d'image
    GLUT.glutSwapBuffers()
    # on force la fonction display a etre executee a nouveau
    GLUT.glutPostRedisplay()


def keyboard_up(key, x, y):
    global pressed_key
    key = key.decode('utf-8')
    pressed_key.remove(key)


# fonction keyboard pour la gestion des evenements clavier.
def keyboard(key, x, y):
    key = key.decode('utf-8')
    global myShip

    pressed_key.add(key)

    if key == chr(27):
        exit(0)

    if key == 'r':
        myShip = Ship(center=[0.0 for i in range(4)], speed=0, bottom_color=(1, 0, 0), head_color=(1, 1, 1))


def key_update(dummy = None):

    global da
    x = y = 0
    if 'o' in pressed_key:
        da += 1.0
    if 'p' in pressed_key:
        da -= 1.0
    if 'z' in pressed_key or 'w' in pressed_key:
        x = da
    if ' ' in pressed_key:
        myShip.speed += 2

    if 's' in pressed_key:
        x = -da
    if 'd' in pressed_key:
        y = da
    if 'q' in pressed_key or 'a' in pressed_key:
        y = -da
    if x != 0 or y != 0:
        myShip.update_mat(x, y)
    GLUT.glutTimerFunc(10, key_update, None)


def timerFunc(dummy = None):
    # on modifie les variables de position

    myShip.update_center()
    myShip.speed = myShip.speed*0.90 if myShip.speed > 1 else myShip.speed - 0.001 if myShip.speed > 0 else 0
    
    # Move enemies
    for enemy in enemies:   # type:Ship
        enemy.update_center()
        enemy.update_mat(3, random.randint(-5, 5))
        enemy.speed += max(-enemy.speed, random.randint(-1, 1))

    # on lance a nouveau un timer
    GLUT.glutTimerFunc(10, timerFunc, 10)


if __name__ == "__main__":
    pressed_key = set()
    da = 5.0
    myShip = Snake(center=np.zeros(4), speed=0, head_color=(0, 1, 1))
    enemies = []
    num_e = 100

    for i in range(num_e):
        enemies.append(Ship())
    initWindowWidth = 1200  # unit: pixels
    initWindowHeight = 1000  # unit: pixels
    Element.screen_width = initWindowWidth
    Element.screen_height = initWindowHeight
    initWindowPosition_X = 100  # unit: pixels
    initWindowPosition_Y = 100  # unit: pixels

    GLUT.glutInit(sys.argv)
    # Caracterisation de la fenetre d'affichage
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGBA | GLUT.GLUT_DEPTH)
    # Taille de la fenetre de rendu
    GLUT.glutInitWindowSize(initWindowWidth, initWindowHeight)
    # Position de la fenetre
    GLUT.glutInitWindowPosition(initWindowPosition_X, initWindowPosition_Y)
    # creation de la fenetre
    GLUT.glutCreateWindow('BE OpenGL Supelec')

    # appel de la fonction d'initialisation
    init()
    # declaration des fonctions GLUT :
    GLUT.glutDisplayFunc(display)
    GLUT.glutReshapeFunc(reshape)
    GLUT.glutKeyboardFunc(keyboard)
    GLUT.glutKeyboardUpFunc(keyboard_up)

    # Boucle infinie d'interaction
    GLUT.glutMainLoop()


