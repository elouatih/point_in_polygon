#!/usr/bin/env python3
"""
fichier comparaison des trois algorithmes
pour un ensemble donné de polygones
"""
from crossing_number import crossing_number
from quadrant_product import quadrant_product
from cutting_triangle import cutting_triangle
from tycat import read_instance
import sys
from time import time
from geo.polygon import Polygon
from geo.point import Point


def trouve_inclusions(polygones, fonction):
    output = [-1 for _ in range(len(polygones))]
    new = sorted(polygones, key=lambda x:abs(x.area()))
    quadrants = [p.bounding_quadrant() for p in new]
    for i in range(len(new)):
        point = new[i].points[0]
        for j in range(len(new)):
            if i == j:
                continue
            else:
                if not(fonction(point, new[j], quadrants[j])):
                    continue
                else:
                    output[polygones.index(new[i])] = polygones.index(new[j])
                    break
    return output


for fichier in sys.argv[1:]:
    polygones = read_instance(fichier)
    print("crossing_number: ")
    start_1 = time()
    print(trouve_inclusions(polygones, crossing_number))
    end_1 = time()
    print(end_1 - start_1)
    print("quadrant_product: ")
    start_2 = time()
    print(trouve_inclusions(polygones, quadrant_product))
    end_2 = time()
    print(end_2 - start_2)
    print("cutting_triangle: ")
    start_3 = time()
    print(trouve_inclusions(polygones, cutting_triangle))
    end_3 = time()
    print(end_3 - start_3)
