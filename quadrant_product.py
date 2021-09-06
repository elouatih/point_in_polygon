#!/usr/bin/env python3
"""
Fichier qui teste l'appartenance d'un point
dans un polygone en utilisant l'algorithme
quadrant product
"""
from geo.point import Point
from geo.polygon import Polygon


def quadrant_product(point, polygone, quadrant):
    """
    utilisation de quadrant_product
    """
    # Si le point est à l'extérieur du quadrant
    # alors il est systématiquement à l'extérieur du polygone
    if not(point.point_in_quadrant(quadrant)):
        return 0
    # Sinon on procède selon une division par quadrants de segments
    polygone = polygone.orient()
    segments = list(polygone.segments())
    b_q = [s.bounding_quadrant() for s in segments]
    for i in range(len(b_q)):
        if point.point_in_quadrant(b_q[i]):
            segment = segments[i]
            return segment.product_segment_pt(point)>0
    point_proche = sorted(polygone.points, key=lambda x:x.distance_to(point))[0]
    segment_1 = list(filter(lambda x:x.endpoints[1]==point_proche, segments))[0]
    segment_2 = list(filter(lambda x:x.endpoints[0]==point_proche, segments))[0]
    if segment_1.product_segment_other(segment_2)>0:
        return segment_1.product_segment_pt(point)>0 and\
                segment_2.product_segment_pt(point)>0
    else:
        return segment_1.product_segment_pt(point)>0 or\
                segment_2.product_segment_pt(point)>0

if __name__ == "__main__":
    print(2)
