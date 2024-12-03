import pyglet
from pyglet import shapes
import math

### ear clipping system to get traingles froma a polygon (to draw later)

from typing import List, Tuple

def is_ear(polygon, i):
    """Check if the point polygon[i] is an 'ear' in the polygon."""
    n = len(polygon)
    prev_idx = (i - 1) % n
    next_idx = (i + 1) % n
    a = polygon[prev_idx]
    b = polygon[i]
    c = polygon[next_idx]

    # Check if the triangle is a valid ear (convex and no points inside)
    if not is_convex(a, b, c):
        return False

    # Check if any other point is inside the triangle
    for j in range(n):
        if j != prev_idx and j != i and j != next_idx:
            if point_in_triangle(polygon[j], a, b, c):
                return False
    return True


def is_convex(a, b, c):
    """Check if the angle formed by points a, b, and c is convex."""
    return (c[0] - b[0]) * (a[1] - b[1]) > (a[0] - b[0]) * (c[1] - b[1])


def point_in_triangle(p, a, b, c):
    """Check if point p is inside the triangle formed by a, b, and c."""
    detT = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
    alpha = ((b[1] - c[1]) * (p[0] - c[0]) + (c[0] - b[0]) * (p[1] - c[1])) / detT
    beta = ((c[1] - a[1]) * (p[0] - c[0]) + (a[0] - c[0]) * (p[1] - c[1])) / detT
    gamma = 1 - alpha - beta
    return alpha >= 0 and beta >= 0 and gamma >= 0


def triangulate_polygon(polygon):
    """Triangulate a concave polygon into triangles."""
    triangles = []
    points = polygon[:]

    while len(points) > 3:
        for i in range(len(points)):
            if is_ear(points, i):
                prev_idx = (i - 1) % len(points)
                next_idx = (i + 1) % len(points)
                triangles.append([points[prev_idx], points[i], points[next_idx]])
                points.pop(i)
                break
            print(str(i) + f" {len(points)} points left.")

    # Add the last remaining triangle
    triangles.append(points)
    return triangles


#### to delete

def raycasting(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False

    # Loop through each edge of the polygon
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]  # next vertex

        # Check if the edge intersects the ray from the point
        if min(y1, y2) < y <= max(y1, y2) and x <= max(x1, x2):
            if y1 != y2:  # Avoid division by zero
                x_intersection = (y - y1) * (x2 - x1) / (y2 - y1) + x1
            if x1 == x2 or x <= x_intersection:
                inside = not inside

    return inside


def calculate_centroid(polygon):
    n = len(polygon)
    A = 0  # Area
    C_x = 0  # Coordinata x del baricentro
    C_y = 0  # Coordinata y del baricentro

    for i in range(n):
        x_i, y_i = polygon[i]
        x_next, y_next = polygon[(i + 1) % n]  # Il prossimo punto (ciclico)

        # Calcolo dell'area
        area_component = (x_i * y_next - x_next * y_i)
        A += area_component

        # Calcolo delle coordinate del baricentro
        C_x += (x_i + x_next) * area_component
        C_y += (y_i + y_next) * area_component

    A *= 0.5  # Area finale
    C_x /= (6 * A)  # Coordinata x del baricentro
    C_y /= (6 * A)  # Coordinata y del baricentro

    return (C_x, C_y), A


####### CODICE PER IL CALCOLO CORRETTO DELLA ACCURACY AGGIORNANDO LA LISTA DI PUNTI

def insert_intersections_corrected(line1, line2):
    """
    Trova le intersezioni tra i segmenti di due linee e aggiorna la seconda linea
    inserendo le intersezioni nel punto corretto, gestendo anche intersezioni esatte sugli endpoint.
    """
    def is_intersecting(p1, p2, q1, q2):
        """Calcola se due segmenti si intersecano e il punto di intersezione."""
        det = (p2[0] - p1[0]) * (q2[1] - q1[1]) - (p2[1] - p1[1]) * (q2[0] - q1[0])
        if det == 0:
            return False, None  # Segmenti paralleli o coincidenti

        t = ((q1[0] - p1[0]) * (q2[1] - q1[1]) - (q1[1] - p1[1]) * (q2[0] - q1[0])) / det
        u = ((q1[0] - p1[0]) * (p2[1] - p1[1]) - (q1[1] - p1[1]) * (p2[0] - p1[0])) / det

        if 0 <= t <= 1 and 0 <= u <= 1:
            # Calcolo punto di intersezione
            intersection = (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))
            return True, intersection

        return False, None

    updated_line2 = line2.copy()
    insert_positions = []  # Traccia le posizioni dove inserire gli aggiornamenti

    for i in range(len(line1) - 1):
        p1, p2 = line1[i], line1[i + 1]
        for j in range(len(updated_line2) - 1):
            q1, q2 = updated_line2[j], updated_line2[j + 1]
            intersect, point = is_intersecting(p1, p2, q1, q2)
            if intersect and point not in updated_line2:
                insert_positions.append((j + 1, point))  # Traccia posizione e punto

    # Inserire i punti nella posizione corretta senza interferire con l'iterazione
    for pos, point in sorted(insert_positions, reverse=True):
        updated_line2.insert(pos, point)

    return updated_line2