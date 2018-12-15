def aac(s, c, p, r):  # draws a circle
    import pygame.gfxdraw as gfx
    gfx.filled_circle(s, p[0], p[1], r, c)


def aal(s, c, p1, p2):  # draws a line
    import pygame
    pygame.draw.aaline(s, c, p1, p2)


def aal_edge(s, c, arr, e1, e2):  # draws an edge
    aal(s, c, (arr[e1, 0], arr[e1, 1]), (arr[e2, 0], arr[e2, 1]))
