#!/usr/bin/env python3
"""
Tracage de performances de chaque algorithme
"""
from geo.point import Point
from geo.polygon import Polygon, couples
from random import randint
from time import time
from matplotlib.pyplot import plot, show, scatter, subplot, xlabel, ylabel, xlim, ylim
from crossing_number import crossing_number
from quadrant_product import quadrant_product
from cutting_triangle import cutting_triangle



def point_segment(p1, p2, p):
    """
    Determine si le point p est à gauche ou
    à droite du segment defini par les points p1 et p2
    """
    return ((p2.x-p1.x)*(p.y-p1.y)-(p2.y-p1.y)*(p.x-p1.x))>0

def enveloppe_inc(points):
    """
    Trace l'enveloppe convexe qui lie une liste de points
    """
    def cle(P):
        return P.x
    points.sort(key=cle)
    N = len(points)
    enveloppe = [points[0], points[1]]
    for i in range(2, N):
        enveloppe.append(points[i])
        valide = False
        while not(valide) and len(enveloppe) > 2:
            p3 = enveloppe.pop()
            p2 = enveloppe.pop()
            p1 = enveloppe.pop()
            if point_segment(p1, p2, p3):
                enveloppe.append(p1)
                enveloppe.append(p3)
            else:
                enveloppe.append(p1)
                enveloppe.append(p2)
                enveloppe.append(p3)
                valide = True
    enveloppe.append(points[N-2])
    for i in range(N-3, -1, -1):
        enveloppe.append(points[i])
        valide = False
        while not(valide) and len(enveloppe) > 2:
            p3 = enveloppe.pop()
            p2 = enveloppe.pop()
            p1 = enveloppe.pop()
            if point_segment(p1, p2, p3):
                enveloppe.append(p1)
                enveloppe.append(p3)
            else:
                enveloppe.append(p1)
                enveloppe.append(p2)
                enveloppe.append(p3)
                valide = True
    return enveloppe


def main_1(n, temps_1, fonction):
    """
    Genere n points aleatoires et trace leur enveloppe convexe
    Stocke les performances dans un tableau temps_1
    """
    points = [Point((randint(5, 995), randint(5, 995))) for _ in range(n)]
    polygon_points = enveloppe_inc(points)
    polygone = Polygon(polygon_points)
    quadrant = polygone.bounding_quadrant()
    point_test = Point((200, 200))
    start_1 = time()
    print(int(fonction(point_test, polygone, quadrant)))
    end_1 = time()
    temps_1.append(10000*(end_1 - start_1))



temps_1 = [] # Liste pour stocker les performances
nombre = list(range(5, 10000, 10)) # Liste contenant les differents valeurs de n
# Remplit la liste temps_1 pour chaque valeur de n
for i in range(5, 10000, 10):
    main_1(i, temps_1, crossing_number)


# Trace l'évolution des performances en fonction du nombre de
# sommets du polygone en choisissant un algorithme
subplot()
scatter(nombre, temps_1, edgecolor="none", c="skyblue", s=25)
xlim(-1, 10001)
ylim(-1, 2001)
xlabel('Nombre de points du polygone')
ylabel("Temps d'exécution")
show()
