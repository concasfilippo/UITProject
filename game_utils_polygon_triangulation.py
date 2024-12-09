# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.spatial import Delaunay
# from shapely.geometry import Polygon
#
# # Lista di punti (x, y) che definiscono un poligono concavo
# points = [(0, 0), (2, 0), (2, 2), (1, 1), (0, 2)]
#
# # Creiamo un oggetto Polygon con Shapely
# polygon = Polygon(points)
#
# # Calcoliamo la triangolazione di Delaunay
# triangles = Delaunay(np.array(points))
#
#
# # Funzione per verificare se un triangolo è all'interno del poligono
# def is_triangle_inside_polygon(triangle_points, polygon):
#     triangle = Polygon(triangle_points)
#     return polygon.contains(triangle)
#
#
# # Funzione per disegnare il poligono e i triangoli interni
# def plot_polygon_with_triangles(polygon_points, triangles, polygon):
#     fig, ax = plt.subplots()
#
#     # Disegniamo il poligono
#     polygon_points = np.array(polygon_points + [polygon_points[0]])  # Chiudiamo il poligono
#     ax.plot(polygon_points[:, 0], polygon_points[:, 1], 'k-', label='Poligono')
#
#     # Disegniamo solo i triangoli che sono completamente all'interno del poligono
#     for simplex in triangles.simplices:
#         triangle_points = np.array([points[simplex[0]], points[simplex[1]], points[simplex[2]], points[simplex[0]]])
#
#         # Verifica se il triangolo è all'interno del poligono
#         if is_triangle_inside_polygon(triangle_points, polygon):
#             ax.plot(triangle_points[:, 0], triangle_points[:, 1], 'r-', alpha=0.5)  # Triangolo in rosso
#
#     ax.set_title('Triangolazione del Poligono Concavo (Solo Triangoli Interni)')
#     ax.set_aspect('equal')
#     plt.show()
#
#
# # Visualizziamo il risultato
# plot_polygon_with_triangles(points, triangles, polygon)


import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from shapely.geometry import Polygon
from scipy.interpolate import interp1d
from shapely.geometry import Point, Polygon
from decimal import Decimal

def get_triangles_from_polygon(points):
    """
    Converte una lista di punti di un poligono in una triangolazione, restituendo le triple
    :param points: i punti (es. [(0, 0), (2, 0), (2, 2), (1, 1), (0, 2)])
    :return: nulla
    """
    # Lista di punti (x, y) che definiscono un poligono concavo
    #points = [(0, 0), (2, 0), (2, 2), (1, 1), (0, 2)]

    # Creiamo un oggetto Polygon con Shapely
    polygon = Polygon(points)

    # Calcoliamo la triangolazione di Delaunay
    triangles = Delaunay(np.array(points))

    # Visualizziamo il risultato
    x  =plot_polygon_with_triangles(points, triangles, polygon, points)
    x = [[tuple(coppia) for coppia in sottolista] for sottolista in x]
    #print(x)
    return x


# Funzione per verificare se un triangolo è all'interno del poligono
def is_triangle_inside_polygon(triangle_points, polygon):
    triangle = Polygon(triangle_points)
    return polygon.contains(triangle)


# Funzione per disegnare il poligono e i triangoli interni
def plot_polygon_with_triangles(polygon_points, triangles, polygon, points):
    list_triangles = []
    #fig, ax = plt.subplots()

    # Disegniamo il poligono
    polygon_points = np.array(polygon_points + [polygon_points[0]])  # Chiudiamo il poligono
    #ax.plot(polygon_points[:, 0], polygon_points[:, 1], 'k-', label='Poligono')

    # Disegniamo solo i triangoli che sono completamente all'interno del poligono
    for simplex in triangles.simplices:
        triangle_points = np.array([points[simplex[0]], points[simplex[1]], points[simplex[2]], points[simplex[0]]])

        # Verifica se il triangolo è all'interno del poligono
        if is_triangle_inside_polygon(triangle_points, polygon):
            #ax.plot(triangle_points[:, 0], triangle_points[:, 1], 'r-', alpha=0.5)  # Triangolo in rosso
            #print(triangle_points)
            list_triangles.append(triangle_points.tolist())

    #ax.set_title('Triangolazione del Poligono Concavo (Solo Triangoli Interni)')
    #ax.set_aspect('equal')
    #plt.show()
    return list_triangles


def polygon_area(points):
    """
    Calculate the area of a concave polygon given its vertices.

    Parameters:
    points (list of tuple): A list of (x, y) coordinates of the polygon's vertices
                            in either clockwise or counterclockwise order.

    Returns:
    float: The absolute value of the area of the polygon.
    """
    n = len(points)
    if n < 3:
        raise ValueError("A polygon must have at least 3 points.")

    # Shoelace formula
    area = 0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]  # Wrap around to the first point
        area += x1 * y2 - y1 * x2

    return abs(area) / 2


def polygon_area_decimal(points):
    """
    Calculate the area of a concave polygon given its vertices.

    Parameters:
    points (list of tuple): A list of (x, y) coordinates of the polygon's vertices
                            in either clockwise or counterclockwise order, using Decimal values.

    Returns:
    Decimal: The absolute value of the area of the polygon.
    """
    # Ensure all coordinates are Decimal
    points = [(Decimal(x), Decimal(y)) for x, y in points]

    n = len(points)
    if n < 3:
        raise ValueError("A polygon must have at least 3 points.")

    # Shoelace formula
    area = Decimal(0)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]  # Wrap around to the first point
        area += x1 * y2 - y1 * x2

    return abs(area) / Decimal(2)


def ensure_point_inside_triangle(triangle, point):
    """
    Adjust a point to ensure it lies inside the given triangle.

    Parameters:
    triangle (list of tuple): List of three tuples representing the triangle vertices (x, y).
    point (tuple): The point (x, y) to adjust.

    Returns:
    tuple: The adjusted point coordinates (x, y).
    """


    def barycentric_coords(triangle, point):
        A, B, C = triangle
        Px, Py = point

        # Compute vectors
        v0 = np.array([C[0] - A[0], C[1] - A[1]])
        v1 = np.array([B[0] - A[0], B[1] - A[1]])
        v2 = np.array([Px - A[0], Py - A[1]])

        # Compute dot products
        dot00 = np.dot(v0, v0)
        dot01 = np.dot(v0, v1)
        dot02 = np.dot(v0, v2)
        dot11 = np.dot(v1, v1)
        dot12 = np.dot(v1, v2)

        # Compute barycentric coordinates
        denom = dot00 * dot11 - dot01 * dot01
        v = (dot11 * dot02 - dot01 * dot12) / denom
        w = (dot00 * dot12 - dot01 * dot02) / denom
        u = 1 - v - w
        return u, v, w

    def project_point(triangle, point):
        # Project the point to the closest edge or vertex
        A, B, C = triangle

        def point_to_line_projection(P, Q, R):
            """Project point R onto the line segment PQ."""
            PQ = np.array([Q[0] - P[0], Q[1] - P[1]])
            PR = np.array([R[0] - P[0], R[1] - P[1]])
            length_sq = np.dot(PQ, PQ)
            if length_sq == 0:  # P and Q are the same point
                return P
            t = max(0, min(1, np.dot(PR, PQ) / length_sq))
            projection = (P[0] + t * PQ[0], P[1] + t * PQ[1])
            return projection

        # Check the distance to each edge
        projections = [
            point_to_line_projection(A, B, point),
            point_to_line_projection(B, C, point),
            point_to_line_projection(C, A, point),
        ]
        # Choose the closest projection
        distances = [np.linalg.norm(np.array(p) - np.array(point)) for p in projections]
        return projections[np.argmin(distances)]

    # Check if the point lies inside
    u, v, w = barycentric_coords(triangle, point)
    if u >= 0 and v >= 0 and w >= 0:  # Point is inside
        return point
    else:  # Point is outside
        return project_point(triangle, point)


def triangle_centroid(triangle):
    """
    Calculate the centroid (center point) of a triangle.

    Parameters:
    triangle (list of tuple): A list of three tuples representing the triangle vertices (x, y).

    Returns:
    tuple: The coordinates of the centroid (x_c, y_c).
    """
    if len(triangle) != 3:
        raise ValueError("A triangle must have exactly three vertices.")

    # Extract vertices
    (x1, y1), (x2, y2), (x3, y3) = triangle

    # Calculate the centroid
    x_c = (x1 + x2 + x3) / 3
    y_c = (y1 + y2 + y3) / 3

    return x_c, y_c



### calcolo area per la accuratezza
def interpolate_points(A, B):
    """
    Interpola i punti di B per adattarli alla lunghezza di A.

    Parametri:
    A (list of tuple): Lista di punti A [(x1, y1), (x2, y2), ...]
    B (list of tuple): Lista di punti B [(x1, y1), (x2, y2), ...]

    Ritorna:
    list of tuple: Lista di punti interpolati B in modo che la lunghezza corrisponda a A.
    """
    len_A = len(A)
    len_B = len(B)

    if len_A == len_B:
        return B  # Le due liste hanno già la stessa lunghezza, restituisci B

    if len_B == 1:
        # Se B ha un solo punto, lo ripetiamo per adattarlo alla lunghezza di A
        return [B[0]] * len_A

    # Interpolazione lineare per adattare la lunghezza di B a quella di A
    B = np.array(B)
    x_vals_B = np.linspace(0, len_B - 1, len_B)
    x_vals_A = np.linspace(0, len_B - 1, len_A)

    # Interpolazione separata per ogni coordinata
    interp_x = interp1d(x_vals_B, B[:, 0], kind='linear')
    interp_y = interp1d(x_vals_B, B[:, 1], kind='linear')

    # Calcolare i nuovi punti interpolati
    new_B = np.array([(interp_x(x), interp_y(x)) for x in x_vals_A])

    return new_B


def area_between_lists(A, B):
    """
    Calcola il rapporto tra l'area (approssimazione numerica) tra due liste di punti
    e l'area del bounding box della lista di punti A.

    1) Area tra le curve dei punti A e B, usando il metodo dei trapezi.
    2) Area del bounding box di A.
    3) Calcola il rapporto tra le due aree.

    Parametri:
    A (list of tuple): Lista di punti A [(x1, y1), (x2, y2), ...]
    B (list of tuple): Lista di punti B [(x1, y1), (x2, y2), ...]

    Ritorna:
    float: Il rapporto tra l'area tra A e B e l'area del bounding box di A.
    """

    # Step 1: Interpola i punti di B per adattarli alla lunghezza di A
    B_interpolated = interpolate_points(A, B)

    # Step 2: Calcolare l'area tra i punti A e B usando il metodo dei trapezi
    A = np.array(A)
    B_interpolated = np.array(B_interpolated)

    # Somma dei trapezi tra le curve A e B_interpolated
    x_vals_A = A[:, 0]
    y_vals_A = A[:, 1]
    y_vals_B = B_interpolated[:, 1]

    # Calcolare l'area tra le curve usando il metodo dei trapezi
    area_between = np.trapz(np.abs(y_vals_A - y_vals_B), x_vals_A)

    # Step 3: Calcolare l'area del bounding box di A
    x_min, y_min = np.min(A, axis=0)
    x_max, y_max = np.max(A, axis=0)
    #bbox_area = (x_max - x_min) * (y_max - y_min)
    bbox_area = polygon_area(A)

    # Step 4: Calcolare il rapporto tra l'area tra le curve e l'area del bounding box
    if bbox_area == 0:
        raise ValueError("L'area del bounding box è zero, controlla i punti di A.")

    ratio = area_between / bbox_area
    return ratio


def clamp_point_in_polygon(point, polygon_points):
    """
    Aggiorna la posizione di un punto affinché rimanga all'interno di un poligono.
    Se il punto è già dentro il poligono, non viene modificato.
    Se è fuori, viene spostato sul bordo più vicino.

    Parametri:
    point (tuple): Il punto da verificare (x, y).
    polygon_points (list of tuple): Punti che definiscono il poligono [(x1, y1), (x2, y2), ...].

    Ritorna:
    tuple: La nuova posizione del punto (x, y), assicurata dentro il poligono.
    """
    # Creazione del poligono con Shapely
    polygon = Polygon(polygon_points)
    p = Point(point)

    # Verifica se il punto è dentro il poligono
    if polygon.contains(p):
        return point  # Nessuna modifica necessaria

    # Se il punto è fuori, spostalo sul bordo più vicino
    nearest_point = polygon.exterior.interpolate(polygon.exterior.project(p))
    #print(nearest_point)
    return nearest_point.x, nearest_point.y


##à calcolo metrica ddia ccuracy v2

def align_lists(list1, list2):
    """
    Allinea due liste di punti in modo che inizino e finiscano con le stesse coppie di punti.
    """
    # Converti le liste in array numpy per semplificare le operazioni
    list1 = np.array(list1)
    list2 = np.array(list2)

    # Trova l'indice iniziale e finale dei punti in comune
    start = None
    end = None

    for i in range(len(list2)):
        if np.array_equal(list2[i], list1[0]):
            start = i
        if np.array_equal(list2[i], list1[-1]):
            end = i

    # Se i punti comuni non esistono, restituisci un errore
    if start is None or end is None:
        raise ValueError("Le liste non hanno coppie iniziali e finali in comune.")

    # Ritaglia la seconda lista
    aligned_list2 = list2[start:end + 1]
    return list1, aligned_list2


def interpolate_list(original_list, target_length):
    """
    Interpola una lista di punti in modo che abbia una lunghezza specificata.
    """
    original_list = np.array(original_list)
    original_indices = np.linspace(0, 1, len(original_list))
    target_indices = np.linspace(0, 1, target_length)
    interpolated_list = np.array([
        np.interp(target_indices, original_indices, original_list[:, 0]),
        np.interp(target_indices, original_indices, original_list[:, 1]),
    ]).T
    return interpolated_list


def calculate_area(list1, list2):
    """
    Calcola la somma delle aree tra i segmenti di due liste di punti allineate.
    """
    # Se le liste hanno lunghezza diversa, interpola quella più corta
    if len(list1) != len(list2):
        if len(list1) < len(list2):
            list1 = interpolate_list(list1, len(list2))
        else:
            list2 = interpolate_list(list2, len(list1))

    # Calcolo dell'area tra i segmenti
    area = 0
    for i in range(len(list1) - 1):
        # Vertici del trapezio
        x1, y1 = list1[i]
        x2, y2 = list1[i + 1]
        x3, y3 = list2[i]
        x4, y4 = list2[i + 1]

        # Calcolo dell'area del trapezio usando la formula del determinante
        trapezoid_area = 0.5 * abs((x2 - x1) * (y3 + y4) - (x4 - x3) * (y1 + y2))
        area += trapezoid_area

    return area


def compare_lists(list1, list2):
    """
    Allinea due liste e calcola l'area totale tra i segmenti.
    """
    # Allineare le liste
    aligned_list1, aligned_list2 = align_lists(list1, list2)
    # Calcolare l'area
    total_area = calculate_area(aligned_list1, aligned_list2)
    return total_area


#calcola accuracy


def elimina_codini(lista1, lista2):
    """
    Allinea le due liste in modo che entrambe inizino e finiscano con gli stessi punti.
    Rimuove i punti extra dalla seconda lista.
    """
    # Trova il primo punto in comune
    #print(lista2)
    start_idx = 0
    while start_idx < len(lista2) and lista1[0] != lista2[start_idx]:
        # print(lista2[start_idx + 1])
        # print(lista1[0])
        # print(lista1[0] != lista2[start_idx + 1])
        start_idx += 1
    #print(lista2[start_idx:])
    # Trova l'ultimo punto in comune (partendo dalla fine)
    end_idx = 0 #-1
    # print(lista2)
    # while end_idx >= -len(lista2) and lista1[-1] != lista2[end_idx]:
    #     print(lista2[end_idx])
    #     # print(lista1[-1])
    #     end_idx -= 1

    # Ritorna le due liste accorciate
    #print(lista1)
    #print(lista2[start_idx:])
    return lista1, lista2[start_idx:]


def calcola_area(poligono):
    """
    Calcola l'area di un poligono dato un elenco di punti utilizzando la formula di Gauss (area di un poligono semplice).
    """
    x = [p[0] for p in poligono]
    y = [p[1] for p in poligono]

    area = 0
    n = len(poligono)
    for i in range(n):
        j = (i + 1) % n
        area += x[i] * y[j]
        area -= x[j] * y[i]
        # print(area)
    return abs(area) / 2.0


def calcola_area_totale(lista1, lista2):
    """
    Allinea le due liste, calcola l'area del poligono creato tra le coppie di punti di lista1
    utilizzando i punti corrispondenti di lista2.
    """
    # Allinea le due liste
    #lista1, lista2 = elimina_codini(lista1, lista2)

    area_totale = 0

    # Per ogni coppia di punti consecutivi in lista1
    for i in range(len(lista1) - 1):
        p1 = lista1[i]
        p2 = lista1[i + 1]

        # Trova l'intervallo di punti in lista2 tra p1 e p2
        idx1 = lista2.index(p1)
        idx2 = lista2.index(p2)

        if idx1 < idx2:  # Assicurati che i punti siano nell'ordine giusto
            poligono = lista2[idx1:idx2 + 1]
            area_totale += calcola_area(poligono)

    return area_totale

######## AGIORNAMENTO USO DECIMAL
def calcola_area_decimal(poligono):
    """
    Calcola l'area di un poligono dato un elenco di punti utilizzando la formula di Gauss (area di un poligono semplice).
    """
    x = [p[0] for p in poligono]
    y = [p[1] for p in poligono]

    area = Decimal(0)
    n = len(poligono)
    for i in range(n):
        j = (i + 1) % n
        area += x[i] * y[j]
        area -= x[j] * y[i]
    return abs(area) / Decimal(2)

def calcola_area_totale_decimal(lista1, lista2):
    """
    Allinea le due liste, calcola l'area del poligono creato tra le coppie di punti di lista1
    utilizzando i punti corrispondenti di lista2.
    """
    area_totale = Decimal(0)

    # Per ogni coppia di punti consecutivi in lista1
    for i in range(len(lista1) - 1):
        p1 = lista1[i]
        p2 = lista1[i + 1]

        # Trova l'intervallo di punti in lista2 tra p1 e p2
        idx1 = lista2.index(p1)
        idx2 = lista2.index(p2)

        if idx1 < idx2:  # Assicurati che i punti siano nell'ordine giusto
            poligono = lista2[idx1:idx2 + 1]
            area_totale += calcola_area_decimal(poligono)

    return area_totale



if __name__ == '__main__':
    get_triangles_from_polygon(points=[(0, 0), (2, 0), (2, 2), (1, 1), (0, 2)])


