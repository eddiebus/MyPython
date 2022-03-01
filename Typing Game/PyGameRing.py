"""
Something to render rings (idek...)
"""
import pygame
import math


def RenderRing(surface = pygame.Surface,colour = pygame.Color,
               startAngle = 0, endAngle = 0,
               innerRadius = 0,
               outerRadius = 100
               ):
    if innerRadius < 0:
        innerRadius = 0

    if outerRadius < innerRadius:
        outerRadius = innerRadius + 1


    pass