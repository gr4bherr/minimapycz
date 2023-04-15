#!/usr/bin/env python3
import psycopg2
from shapely import wkb
import shapely


# this file is for storing (and optimizing) large geometry objects


with psycopg2.connect(database='osm', user='postgres', password='fuckme', host='localhost') as conn:
  cur = conn.cursor()

# BOARDER 
# optimized: 123652 -> 966 points (4MB -> 31KB)
cur.execute(f"""SELECT way FROM planet_osm_polygon where boundary='administrative' and  admin_level='2'""")

hex1 = cur.fetchall()
polygon1 = wkb.loads(hex1[0][0], hex=True)

l = list(polygon1.exterior.coords)

# delete 2**-7 points from list
for i in range(7):
  del l[::2]

polygon2 = shapely.Polygon(l)
hex2 = wkb.dumps(polygon2, hex=True)

with open("cache.txt", "w") as f:
  f.write(hex2)
