populate postgres database with osm data:<br>
osm2pgsql -c -d osm -U postgres -W -H localhost czech-republic-latest.osm.pbf

[main.py](main.py) does this:<br>
(every house in czechia with the house number 3)

![map](https://user-images.githubusercontent.com/24635770/232731933-cf5555f8-ef5d-4414-994e-e58983807792.png)

[main.cpp](main.cpp) does less but without libraries
