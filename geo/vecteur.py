#!/usr/bin/env python3
"""
vecteurs
"""
from geo.point import Point


class Vecteur:
    """
    vecteur est defini par un point d'origine, direction,
    sens et norme
    Dans notre cas, le vecteur serait defini par
    un point d'origine et un point d'arrivee
    """
    def __init__(self, point_1, point_2):
        self.begin = point_1
        self.end = point_2

    def coordonnees_vecteur(self):
        """
        retourne les coordonnees du vecteur
        """
        return (self.end.x - self.begin.x, self.end.y - self.begin.y)

    def produit_vectoriel(self, autre_vecteur):
        """
        effectue le produit vectoriel entre
        self et un autre vecteur
        Normalement, le resultat doit etre un vecteur
        mais puisque on travaille en 2D on ne donne que
        la coordonnee z du vecteur.
        """
        x_1, y_1 = self.coordonnees_vecteur()
        x_2, y_2 = autre_vecteur.coordonnees_vecteur()
        return x_1 * y_2 - x_2 * y_1

    def produit_scalaire(self, autre_vecteur):
        """
        effectue le produit scalaire entre
        self et un autre vecteur
        """
        x_1, y_1 = self.coordonnees_vecteur()
        x_2, y_2 = autre_vecteur.coordonnees_vecteur()
        return x_1 * x_2 + y_2 * y_1
