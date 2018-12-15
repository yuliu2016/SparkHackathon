def aac(s, c, p, r):  # draws a circle
    import pygame.gfxdraw as gfx
    gfx.filled_circle(s, round(p[0]), round(p[1]), round(r), c)


def aal(s, c, p1, p2):  # draws a line
    import pygame
    pygame.draw.aaline(s, c, p1, p2)


def aal_edge(s, c, arr, e1, e2):  # draws an edge
    aal(s, c, (arr[e1, 0], arr[e1, 1]), (arr[e2, 0], arr[e2, 1]))


def c(r, g, b):
    return b | g << (1 << 3) | r << (1 << 4)


cWHITE = c(255, 255, 255)
cBLACK = c(0, 0, 0)
cBLUE = c(0, 0, 255)
cGREEN = c(0, 255, 0)