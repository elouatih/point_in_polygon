"""
segment between two points.
"""
from geo.quadrant import Quadrant
from geo.point import Point
from geo.vecteur import Vecteur

class Segment:
    """
    oriented segment between two points.
    for example:
    - create a new segment between two points:
        segment = Segment([point1, point2])
    - create a new segment from coordinates:
        segment = Segment([Point([1.0, 2.0]), Point([3.0, 4.0])])
    - compute intersection point with other segment:
        intersection = segment1.intersection_with(segment2)
    """
    def __init__(self, points):
        """
        create a segment from an array of two points.
        """
        self.endpoints = points

    def __eq__(self, other):
        return self.endpoints == other.endpoints

    def copy(self):
        """
        return duplicate of given segment (no shared points with original,
        they are also copied).
        """
        return Segment([p.copy() for p in self.endpoints])

    def segment_to_vector(self):
        """
        retourne le vecteur dirigeant le segment
        """
        return Vecteur(*self.endpoints)

    def length(self):
        """
        return length of segment.
        example:
            segment = Segment([Point([1, 1]), Point([5, 1])])
            distance = segment.length() # distance is 4
        """
        return self.endpoints[0].distance_to(self.endpoints[1])

    def bounding_quadrant(self):
        """
        return min quadrant containing self.
        """
        quadrant = Quadrant.empty_quadrant(2)
        for point in self.endpoints:
            quadrant.add_point(point)
        return quadrant

    def is_vertical(self):
        """
        return if we are a truely vertical segment.
        """
        return self.endpoints[0].x == self.endpoints[1].x

    def is_horizontal(self):
        """
        retourne si le segment est horizontal.
        """
        return self.endpoints[0].y == self.endpoints[1].y

    def svg_content(self):
        """
        svg for tycat.
        """
        return '<line x1="{}" y1="{}" x2="{}" y2="{}"/>\n'.format(
            *self.endpoints[0].coordinates,
            *self.endpoints[1].coordinates)

    def endpoint_not(self, point):
        """
        return first endpoint which is not given point.
        """
        if self.endpoints[0] == point:
            return self.endpoints[1]

        return self.endpoints[0]

    def contains(self, possible_point):
        """
        is given point inside us ?
        be careful, determining if a point is inside a segment is a difficult problem
        (it is in fact a meaningless question in most cases).
        you might get wrong results for points extremely near endpoints.
        """
        distance = sum(possible_point.distance_to(p) for p in self.endpoints)
        return abs(distance - self.length()) < 0.000001

    def __str__(self):
        return "Segment([" + str(self.endpoints[0]) + ", " + \
            str(self.endpoints[1]) + "])"

    def __repr__(self):
        return "[" + repr(self.endpoints[0]) + ", " + \
            repr(self.endpoints[1]) + "])"

    def __hash__(self):
        return hash(tuple(self.endpoints))

    def equation_segment(self):
        """
        retourne l'equation de la droite
        porteuse du segment
        Elle retourne la pente et l'ordonnee a l'origine
        pre_condition : le segment n'est pas vertical
        """
        pointA = self.endpoints[0]
        pointB = self.endpoints[1]
        assert pointA.x != pointB.x
        pente = (pointA.y - pointB.y)/(pointA.x - pointB.x)
        ordonnee = pointA.y - pente * pointA.x
        return (pente, ordonnee)

    def oriented_segment(self, vecteur_base):
        """
        verifie si le segment est orienté selon la
        direction du vecteur base
        """
        return (self.segment_to_vector().produit_scalaire(vecteur_base)>0)

    def orient_segment(self, vecteur_base):
        """
        oriente le segment selon un vecteur de base
        """
        if self.oriented_segment(vecteur_base):
            return self
        else:
            ptA = self.endpoints[0]
            ptB = self.endpoints[1]
            return Segment([ptB, ptA])

    def product_segment_pt(self, point):
        """
        produit vectoriel du vecteur dirigeant le segment
        et le vecteur du premier sommet vers le point
        """
        ptA = self.endpoints[0]
        vecteur = self.segment_to_vector()
        vecteur_p = Vecteur(ptA, point)
        return vecteur.produit_vectoriel(vecteur_p)

    def product_segment_other(self, other):
        """
        produit vectoriel du vecteur dirigeant le segment
        et un autre vecteur dirigeant un autre segment
        """
        vecteur = self.segment_to_vector()
        vecteur_2 = other.segment_to_vector()
        return vecteur.produit_vectoriel(vecteur_2)

    def partition_segment(self, area):
        """
        prend juste la partie du edge
        delimitee par la partition
        """
        y_i, y_j = area[0], area[1]
        ptA = self.endpoints[0]
        ptB = self.endpoints[1]
        # Garder l'orientation du segment
        vecteur = self.segment_to_vector()
        # definir le point bas et le point haut du segment
        if ptA.y < ptB.y:
            pt_min, pt_max = ptA, ptB
        else:
            pt_min, pt_max = ptB, ptA
        # On nomine les abscisses des deux points definis auparavant
        x_min, x_max = pt_min.x, pt_max.x
        # On nomine les ordonnees des deux points definis auparavant
        y_min, y_max = pt_min.y, pt_max.y
        # Les cas particuliers
        if (y_min <= y_i and y_max <= y_i) or (y_max >= y_j and y_min >= y_j) or self.is_horizontal():
            return None
        else:
            y_min_nv = max(y_i, y_min)
            y_max_nv = min(y_j, y_max)
            if self.is_vertical():
                pt_min_nv = Point((x_min, y_min_nv))
                pt_max_nv = Point((x_min, y_max_nv))
            else:
                pente, ordonnee = self.equation_segment()
                x_min_nv = (y_min_nv - ordonnee)/pente
                x_max_nv = (y_max_nv - ordonnee)/pente
                pt_min_nv = Point((x_min_nv, y_min_nv))
                pt_max_nv = Point((x_max_nv, y_max_nv))
            new_edge = Segment([pt_min_nv, pt_max_nv])
            return new_edge.orient_segment(vecteur)
