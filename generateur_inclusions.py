#!/usr/bin/env python3
"""
Fichier pour tracer la courbe de comparaisons
des trois algorithmes pour différentes listes
de polygones
"""
import sys
from tycat import read_instance
from geo.point import Point
from geo.polygon import Polygon, couples
from time import time
from matplotlib.pyplot import plot, show, legend, subplot, xlabel, ylabel, xlim, ylim
from crossing_number import crossing_number
from quadrant_product import quadrant_product
from cutting_triangle import cutting_triangle


def main(polygones, fonction):
    """
    fonction retournant les inclusions en choisissant
    un des trois algorithmes
    """
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

# Initier des listes
nombre_poly = [] # Liste pour varier le nombre de polygones
time_1 = [] # Liste de performances pour crossing_number
time_2 = [] # Liste de performances pour quadrant_product
time_3 = [] # Liste de performances pour cutting_triangle
for fichier in sys.argv[1:]:
    polygones = read_instance(fichier)
    for i in range(1, 3001, 20):
        poly = polygones[:i]
        nombre_poly.append(len(poly))
        start = time()
        print(len(main(poly, crossing_number)))
        end = time()
        time_1.append(end - start)
        start_2 = time()
        print(len(main(poly, quadrant_product)))
        end_2 = time()
        time_2.append(end_2 - start_2)
        start_3 = time()
        print(len(main(poly, cutting_triangle)))
        end_3 = time()
        time_3.append(end_3 - start_3)


# Traçage des courbes performances en fonction du nombre de 
subplot()
plot(nombre_poly, time_1, c="black")
plot(nombre_poly, time_2, c="red")
plot(nombre_poly, time_3, c="skyblue")
xlabel('Nombre de polygones')
ylabel("Temps d'exécution")
show()
