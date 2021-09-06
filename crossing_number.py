#!/usr/bin/env python3
"""
Fichier du test d'appartenance de point
dans un polygone en utilisant la methode
crossing number
"""
from geo.polygon import Polygon
from geo.point import Point


def crossing_number(point, polygone, quadrant):
    """
    algorithme crossing number
    """
    # On teste si le point appartient ou non au quadrant
    if not(point.point_in_quadrant(quadrant)):
        return 0
    # si il appartient on effectue la methode crossing number
    compteur = 0
    for s in polygone.segments():
        a, b = s.endpoints[0], s.endpoints[1]
        if (a.y <= point.y and b.y > point.y) or\
		 (a.y > point.y and b.y <= point.y):
            vt = (point.y - a.y)/float(b.y - a.y)
            if point.x < a.x + vt * (b.x - a.x):
                compteur += 1
    return compteur % 2


if __name__ == "__main__":
    print(2)
