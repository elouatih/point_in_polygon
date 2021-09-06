#!/usr/bin/env python3
"""
Fichier principal pour la détection
d'inclusions de polygones en utilisant
l'algorithme crossing_number
"""
from crossing_number import crossing_number
from tycat import read_instance
import sys
from geo.polygon import Polygon
from geo.point import Point


def trouve_inclusions(polygones):
    output = [-1 for _ in range(len(polygones))]
    new = sorted(polygones, key=lambda x:abs(x.area()))
    quadrants = [p.bounding_quadrant() for p in new]
    for i in range(len(new)):
        point = new[i].points[0]
        for j in range(len(new)):
            if i == j:
                continue
            else:
                if not(crossing_number(point, new[j], quadrants[j])):
                    continue
                else:
                    output[polygones.index(new[i])] = polygones.index(new[j])
                    break
    return output


if __name__ == "__main__":
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        print(trouve_inclusions(polygones))
