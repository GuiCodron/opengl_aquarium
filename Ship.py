from Element import Element
import OpenGL.GL as GL
import OpenGL.GLU as GLU
import numpy as np
import random
import math


class Ship(Element):
    """Ship element """
    def __init__(self, center=None, speed=1.0, rot_mat=np.identity(4), bottom_color=None, head_color=None):
        self.center = center if center != None else [random.randint(-10,10), random.randint(-10,10), random.randint(-10,10), 0]
        self.speed = speed
        self.rot_mat = rot_mat
        self.bottom_color = bottom_color if bottom_color else \
            [1.0/float(random.randint(1, 12)), 1.0/float(random.randint(1, 12)), 1.0/float(random.randint(1, 12))]
        self.head_color = head_color if head_color else \
            [1.0/float(random.randint(1, 12)), 1.0/float(random.randint(1, 12)), 1.0/float(random.randint(1, 12))]
        self.i = 0

    def draw(self):
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

        GL.glTranslatef(*self.center[0:-1])
        GL.glMultMatrixf(self.rot_mat)

        GL.glBegin(GL.GL_TRIANGLES)

        GL.glColor3f(*self.bottom_color)
        GL.glVertex3f(-3, 3, 0)
        GL.glVertex3f(-3, -3, 0)
        GL.glVertex3f(3, 3, 0)

        GL.glVertex3f(3, -3, 0)
        GL.glVertex3f(-3, -3, 0)
        GL.glVertex3f(3, 3, 0)

        GL.glColor3f(*self.head_color)
        GL.glVertex3f(0, 0, 10)
        GL.glColor3f(*self.bottom_color)
        GL.glVertex3f(-3, -3, 0)
        GL.glVertex3f(-3, 3, 0)

        GL.glColor3f(*self.head_color)
        GL.glVertex3f(0, 0, 10)
        GL.glColor3f(*self.bottom_color)
        GL.glVertex3f(3, 3, 0)
        GL.glVertex3f(3, -3, 0)

        GL.glColor3f(*self.head_color)
        GL.glVertex3f(0, 0, 10)
        GL.glColor3f(*self.bottom_color)
        GL.glVertex3f(3, 3, 0)
        GL.glVertex3f(-3, 3, 0)

        GL.glColor3f(*self.head_color)
        GL.glVertex3f(0, 0, 10)
        GL.glColor3f(*self.bottom_color)
        GL.glVertex3f(-3, -3, 0)
        GL.glVertex3f(3, -3, 0)

        GL.glEnd()

    def place_camera(self):

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(60.0, self.screen_width / self.screen_height, 1.0, 2000.0)

        array = np.dot(np.transpose(self.rot_mat), np.array([0, 0, 10, 0]))
        back = np.dot(np.transpose(self.rot_mat), np.array([0, 45, -45, 0]))
        up = np.dot(np.transpose(self.rot_mat), np.array([0, 1, 0, 0]))

        GLU.gluLookAt(*(self.center + back)[0:-1], *(self.center + array)[0:-1], *up[:-1])

    def update_mat(self, x, y):
        self.rot_mat = self.x_rot(x, self.rot_mat)
        self.rot_mat = self.y_rot(y, self.rot_mat)

    def update_center(self):
        self.center = np.add(np.dot(np.transpose(self.rot_mat), [0, 0, self.speed, 0]), self.center)
