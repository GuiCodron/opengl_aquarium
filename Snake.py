from Element import Element
import OpenGL.GL as GL
import OpenGL.GLU as GLU
import numpy as np
import random
import math
from numpy import linalg as LA


def inter_cubes(c1,s1,c2,s2):
    pass

class Snake(Element):
    parts_number = 20
    head_size = 10
    """Snake element """
    def __init__(self, center=None, speed=1.0, head_color=None, parts=None):
        if not parts:
            self.parts = [{'center': center, 'rot_mat': np.identity(4)} if center.any() else
                          {'center': np.zeros(4), 'rot_mat': np.identity(4)} for i in range(self.parts_number)]
        else:
            self.parts = parts
        self.speed = speed
        self.head_color = head_color if head_color else \
            [1.0/float(random.randint(1, 12)), 1.0/float(random.randint(1, 12)), 1.0/float(random.randint(1, 12))]

    def draw(self):

        for i, part in enumerate(self.parts):
            GL.glMatrixMode(GL.GL_MODELVIEW)
            GL.glLoadIdentity()
            GL.glTranslatef(*(part['center'][0:-1]))
            GL.glMultMatrixf(part['rot_mat'])
            GL.glBegin(GL.GL_TRIANGLE_STRIP)

            GL.glColor3f(*((self.parts_number-i)/self.parts_number * k for k in self.head_color))
            GL.glVertex3f(*(np.array([-1, -1, 1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([1, -1, 1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([-1, 1, 1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([1, 1, 1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([-1, 1, -1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([1, 1, -1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([1, 1, 1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([1, -1, 1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([1, -1, -1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([1, 1, -1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([-1, -1, -1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([-1, 1, -1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([-1, -1, 1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([-1, 1, 1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([-1, -1, 1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([-1, -1, -1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([1, -1, 1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))
            GL.glVertex3f(*(np.array([1, -1, -1]) * self.head_size/2 * (self.parts_number-i)/self.parts_number))

            GL.glEnd()

    def place_camera(self):

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(60.0, self.screen_width / self.screen_height, 1.0, 2000.0)

        array = np.dot(np.transpose(self.parts[0]['rot_mat']), np.array([0, 0, 10, 0]))
        back = np.dot(np.transpose(self.parts[0]['rot_mat']), np.array([0, 60, -60, 0]))
        up = np.dot(np.transpose(self.parts[0]['rot_mat']), np.array([0, 1, 0, 0]))

        GLU.gluLookAt(*(self.parts[0]['center'] + back)[0:-1], *(self.parts[0]['center'] + array)[0:-1], *up[:-1])

    def update_mat(self, x, y):
        self.parts[0]['rot_mat'] = self.x_rot(x, self.parts[0]['rot_mat'])
        self.parts[0]['rot_mat'] = self.y_rot(y, self.parts[0]['rot_mat'])

    def update_center(self):
        self.parts[0]['center'] += np.dot(np.transpose(self.parts[0]['rot_mat']), [0, 0, self.speed, 0])
        for i, part in enumerate(self.parts[1:]):
            vect = self.parts[i]['center'] - part['center']
            norm = LA.norm(vect)
            dist = (self.head_size/2 * (2*self.parts_number - 2 * i - 1)/self.parts_number)
            z_axis = np.array([0,0,1])
            axis = np.cross(z_axis, vect[0:-1])
            theta = np.arccos(np.clip(np.dot(z_axis,(vect[0:-1] / norm) if vect.any() else z_axis),-1.0, 1.0))
            part['rot_mat'][0:-1, 0:-1] = rotation_matrix(axis, -theta)
            if norm > dist:
                part['center'] += vect * (norm - dist) / norm


def rotation_matrix(axis, theta):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    """
    axis = np.asarray(axis)
    axis = axis/math.sqrt(np.dot(axis, axis))
    a = math.cos(theta/2.0)
    b, c, d = -axis*math.sin(theta/2.0)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    return np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])