#!/usr/bin/env python3

from geo.point import Point
from geo.polygon import Polygon


def eliminer_doublons(points):
    """
    elimine les doublons dans un iterable
    de points
    """
    new_points = [points[0]]
    for i in range(1, len(points)):
        booleen = False
        for point in new_points:
            if point.distance_to(points[i]) == 0:
                booleen = True
        if booleen == True:
            continue
        else:
            new_points.append(points[i])
    return new_points


def point_in_triangle(point, triangle):
    """
    teste si un point appartient au triangle ou non
    """
    new_triangle = triangle.orient()
    s = list(new_triangle.segments())
    return (s[0].product_segment_pt(point)>= 0) and \
            (s[1].product_segment_pt(point)>= 0) and \
             (s[2].product_segment_pt(point)>= 0)


def localiser_point(point, areas):
    """
    localise le point
    """
    for area in areas:
        if area[0] <= point.y < area[1]:
            return area


def cutting_triangle(point, polygone, quadrant):
    """
    utilisation de cutting_triangle
    """
    # Si le point est à l'extérieur du quadrant
    # alors il est systématiquement à l'extérieur du polygone
    if not(point.point_in_quadrant(quadrant)):
        return 0
    # Sinon on procède selon une division par quadrants de segments
    # diviser le polygone
    areas = polygone.divide_areas()
    # Localiser le point
    if areas[0][0] >= point.y or areas[-1][1] <= point.y:
        return 0
    else:
        area = localiser_point(point, areas)
        # Segment inclus dans l'area
        segments = []
        for segment in polygone.segments():
            if segment.partition_segment(area) is not None:
                segments.append(segment.partition_segment(area))
        formes_geo = []
        triangles = []
        for i in range(0, len(segments), 2):
            point_1 = segments[i].endpoints[0]
            point_2 = segments[i].endpoints[1]
            point_3 = segments[i+1].endpoints[0]
            point_4 = segments[i+1].endpoints[1]
            points = [point_1, point_2, point_3, point_4]
            formes_geo.append(Polygon(eliminer_doublons(points)))
        for forme in formes_geo:
            if len(forme.points) == 3:
                triangles.append(forme)
            if len(forme.points) == 4:
                points_1 = [forme.points[0], forme.points[1], forme.points[2]]
                points_2 = [forme.points[0], forme.points[2], forme.points[3]]
                triangles.append(Polygon(points_1))
                triangles.append(Polygon(points_2))
        for triangle in triangles:
            if point_in_triangle(point, triangle):
                return 1
        return 0


if __name__ == "__main__":
    print(3)
