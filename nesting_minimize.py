# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 18:29:06 2023

@author: Dora
"""

import numpy as np
import math
from shapely.geometry import Polygon
from shapely.affinity import rotate
from shapely.ops import unary_union
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from shapely.affinity import translate


V = np.concatenate([np.random.uniform(2, 28, 20), np.random.uniform(0, 360, 10)])

#funkcija koja generira poligone    
def generate_polygons(coordinates):    
    x_coords = coordinates[:10]
    y_coords = coordinates[10:20]
    angles = coordinates[20:]
    polygons = []
    for i in range(2):
        x, y, angle = x_coords[i], y_coords[i], angles[i]
        rect_points = [(x-1, y-1.5), (x+1, y-1.5), (x+1, y+1.5),(x-1, y+1.5)]
        polygon = Polygon(rect_points)
        polygon = rotate(polygon, angle, origin=polygon.centroid)
        polygons.append(polygon)
        
    for i in range(2, 5):
        x, y, angle = x_coords[i], y_coords[i], angles[i]
        square_points = [(x-1.2, y-1.2), (x+1.2, y-1.2), (x+1.2, y+1.2), (x-1.2, y+1.2)]
        polygon = Polygon(square_points)
        polygon = rotate(polygon, angle, origin=polygon.centroid)
        polygons.append(polygon)
        
    for i in range(5, 10):
        x, y, angle = x_coords[i], y_coords[i], angles[i]
        triangle_points = [(x-3/2, y-3*math.sqrt(3)/6), (x+3/2, y-3*math.sqrt(3)/6), (x, y+3*math.sqrt(3)/3)]
        polygon = Polygon(triangle_points)
        polygon = rotate(polygon, angle, origin=polygon.centroid)
        polygons.append(polygon)
    return polygons
#funkcija koja računa površinu koju zauzimaju poligoni (uključujući penale za preklapanje)
def calc_area(coordinates):
    polygons = generate_polygons(coordinates)
    union = unary_union(polygons)
    overlap = sum(p.area for p in polygons) - union.area
    if overlap > 0:
        return (union.area + overlap * 25, )
    else:
        return (union.area, )
    
def optimize_placement(coordinates):
    bounds = [(0,9)] * 20 + [(0, 360)] * 10
    result = minimize(calc_area, coordinates, bounds=bounds)
    return result

result = optimize_placement(V)
optimized_coordinates = result.x
polygons = generate_polygons(V)

# Priprema za plot   
fig, ax = plt.subplots(figsize=(9, 9))
ax.set_xlim(0,30)
ax.set_ylim(0,30)
plt.title("Original")

for polygon in polygons:
    x, y = polygon.exterior.xy
    ax.plot(x, y)

plt.show()

polygons = generate_polygons(optimized_coordinates)

# Priprema za plot   
fig, ax = plt.subplots(figsize=(9, 9))
ax.set_xlim(0, 12)
ax.set_ylim(0, 12)
plt.title("Optimized")

union = unary_union(polygons)
bounds = union.bounds
translated_polygons = []
for polygon in polygons:
    translated_polygons.append(translate(polygon, xoff=-bounds[0]+0.1, yoff=-bounds[1]+0.1))
    
for polygon in translated_polygons:
    x, y = polygon.exterior.xy
    ax.plot(x, y)

plt.show()
