import OpenGL.GLU as GLU
import math
import numpy as np

class Element:
    screen_width = 1
    screen_height = 1

    def draw(self):
        pass

    def x_rot(self, ang, vect):
        if ang == 0:
            return vect
        ang = float(ang)
        rotx = np.array([[1, 0, 0, 0], [0, math.cos(ang / 180 * 3.14), -math.sin(ang / 180 * 3.14), 0],
                         [0, math.sin(ang / 180 * 3.14), math.cos(ang / 180 * 3.14), 0], [0, 0, 0, 1]])
        return np.dot(rotx, vect)

    def y_rot(self, ang, vect):
        if ang == 0:
            return vect
        ang = float(ang)
        roty = np.array([[math.cos(ang / 180 * 3.14), 0, math.sin(ang / 180 * 3.14), 0], [0, 1, 0, 0],
                         [-math.sin(ang / 180 * 3.14), 0, math.cos(ang / 180 * 3.14), 0], [0, 0, 0, 1]])
        return np.dot(roty, vect)


