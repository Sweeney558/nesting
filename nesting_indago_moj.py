# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 18:29:06 2023

@author: Dora
"""

import numpy as np
import math
from shapely.geometry import Polygon
from shapely.affinity import rotate
from shapely.affinity import translate
import matplotlib.pyplot as plt
from shapely.ops import unary_union
from indago import PSO # ...or any other Indago method

V = np.concatenate([np.random.uniform(2, 28, 20), np.random.uniform(0, 360, 10)])
N = V

# funkcija koja generira poligone
def generate_polygons(coordinates):    
    x_coords = coordinates[:10]
    y_coords = coordinates[10:20]
    angles = coordinates[20:]
    gap_size = 0.2
    sf1 = (3+gap_size)/3
    sf2 = (4+gap_size)/4
    polygons = []
    for i in range(5):
        x, y, angle = x_coords[i], y_coords[i], angles[i]
        triangle_points = [(x-3/2*sf1, y-3*math.sqrt(3)/6*sf1), (x+3/2*sf1, y-3*math.sqrt(3)/6*sf1), (x, y+3*math.sqrt(3)/3*sf1)]
        polygon = Polygon(triangle_points)
        polygon = rotate(polygon, angle, origin=polygon.centroid)
        polygons.append(polygon.buffer(-gap_size))
        
    for i in range(5, 8):
        x, y, angle = x_coords[i], y_coords[i], angles[i]
        square_points = [(x-1.5*sf1, y-1.5*sf1), (x+1.5*sf1, y-1.5*sf1), (x+1.5*sf1, y+1.5*sf1), (x-1.5*sf1, y+1.5*sf1)]
        polygon = Polygon(square_points)
        polygon = rotate(polygon, angle, origin=polygon.centroid)
        polygons.append(polygon.buffer(-gap_size))
        
    for i in range(8, 10):
        x, y, angle = x_coords[i], y_coords[i], angles[i]
        rect_points = [(x-1.5*sf1, y-2*sf2), (x+1.5*sf1, y-2*sf2), (x+1.5*sf1, y+2*sf2),(x-1.5*sf1, y+2*sf2)]
        polygon = Polygon(rect_points)
        polygon = rotate(polygon, angle, origin=polygon.centroid)
        polygons.append(polygon.buffer(-gap_size))
    return polygons

# Evaluation function
def goalfun(x):
    constr1 = 0
    obj = 0
    polygons = generate_polygons(x)      
   
    #prvi constraint
    union = unary_union(polygons)
    constr1 = sum(p.area for p in polygons) - union.area
    
    bounds = union.bounds
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]

    obj = width*height
    return obj, constr1

# Initialize the chosen method
optimizer = PSO()

# Optimization variables settings
optimizer.dimensions = 30 
optimizer.lb = [0] * 20 + [0] * 10  
optimizer.ub = [10] * 20 + [360] * 10  


# Set evaluation function
optimizer.evaluation_function = goalfun  

# Objectives and constraints settings
optimizer.objectives = 1 
optimizer.constraints = 1
optimizer.iterations = 5000

# Run optimization
result = optimizer.optimize()  # (using default parameters of the method)
optimized_coordinates = result.X

polygons = generate_polygons(N)

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
union = unary_union(polygons)

union = unary_union(polygons)
bounds = union.bounds

translated_polygons = []
for polygon in polygons:
    translated_polygons.append(translate(polygon, xoff=-bounds[0], yoff=-bounds[1]))

if (sum(p.area for p in polygons) - union.area)<0:  
    print("Poligoni se preklapaju")

# Priprema za plot   
fig, ax = plt.subplots(figsize=(9, 9))
ax.set_xlim(0, 17)
ax.set_ylim(0, 17)
plt.title("Optimized")

for polygon in translated_polygons:
        x, y = polygon.exterior.xy
        ax.plot(x, y)
plt.show()
