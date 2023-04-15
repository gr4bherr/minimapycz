#!/usr/bin/env python3
import psycopg2
from psycopg2.extras import NamedTupleCursor
from shapely import wkb
import matplotlib.pyplot as plt
import time

def showpoint(inp):
  x, y = [], []
  for data in rows:
    tmp = wkb.loads(data[0], hex=True)
    x.append(tmp.x)
    y.append(tmp.y)
  plt.scatter(x,y)

def showline(inp):
  x, y = [], []
  for data in inp:
    tmp = wkb.loads(data[0], hex=True)
    if (tmp.geom_type == "LineString"):
      l = list(tmp.coords)
    if (tmp.geom_type == "Polygon"):
      l = list(tmp.exterior.coords)
    x.append([i[0] for i in l])
    y.append([i[1] for i in l])
  for i in range(len(x)):
    plt.plot(x[i],y[i])

# CACHE
# 0: boarder
cache = []
with open("cache.txt", "r") as f:
  for line in f:
    cache.append(line)
# show boarder
showline([[cache[0]]])

# UI
# todo: when input, matplot wont show all points
#print("enter house number")
#num = input()
num = 3


# QUERY 
with psycopg2.connect(database='osm', user='postgres', password='fuckme', host='localhost') as conn:
  cur = conn.cursor()
  #cur = conn.cursor(cursor_factory=NamedTupleCursor)

cur.execute(f"""SELECT way FROM planet_osm_point where "addr:housenumber"='{num}'""")
rows = cur.fetchall()
print(f"found {len(rows)} results")
showpoint(rows)



plt.show()









#cur.execute("""SELECT * FROM planet_osm_point where "addr:housenumber" IS NOT NULL limit 100""")
#cur.execute("""SELECT * FROM planet_osm_point where "addr:housenumber"='210' limit 10000""")
#cur.execute("""SELECT way FROM planet_osm_point where amenity='pub'""")

#cur.execute(f"""SELECT way FROM planet_osm_polygon where boundary='administrative' and  admin_level='2'""")
#cur.execute(f"""SELECT way FROM planet_osm_polygon limit 1""")