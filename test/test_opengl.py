from threading import Thread
from orderedset import OrderedSet
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import tkinter as tk


class GlutSpyInputs(Thread):
    def __init__(self, app, *args, **kwargs):
        super().__init__(name="SpyInputs", daemon=True)
        self._app = app
        self._key_pressed = OrderedSet()

        glutInit(*args, *kwargs)
        glutInitDisplayMode(GLUT_SINGLE)

        glutInitWindowSize(800, 400)
        glutInitWindowPosition(100, 100)
        glutCreateWindow("SpyInputs")

        glutKeyboardFunc(self.on_key_press)
        glutKeyboardUpFunc(self.on_key_up)

    def on_key_press(self, key, x, y):
        self._key_pressed.add(key)
        self.on_key_update()

    def on_key_up(self, key, x, y):
        self._key_pressed.remove(key)
        self.on_key_update()

    def on_key_update(self):
        print(" | ".join([v.decode() for v in self._key_pressed]))

    def run(self):
        glutMainLoop()


verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 4),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def rotating_cube():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)
    i = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.key:
                i += 1

        glRotatef(10, 20, 2, 4)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)


key_pressed = set()


def on_key_press(key, x, y):
    key_pressed.add(key)
    for v in key_pressed:
        print(v.decode(), end=" | ")
    print("")


def on_key_up(key, x, y):
    key_pressed.remove(key)


def main(*args, **kwargs):
    glutInit(*args, *kwargs)
    glutInitDisplayMode(GLUT_SINGLE)

    glutInitWindowSize(0, 0)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("SpyInputs")

    glutKeyboardFunc(on_key_press)
    glutKeyboardUpFunc(on_key_up)
    glutMainLoop()


if __name__ == '__main__':
    main()
