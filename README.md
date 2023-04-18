populate postgres database with osm data:
osm2pgsql -c -d osm -U postgres -W -H localhost czech-republic-latest.osm.pbf

[main.py](main.py) does this:

![map](https://user-images.githubusercontent.com/24635770/232729541-d06f9153-d457-4ac5-b8f4-9639af4e27c1.png)

[main.cpp](main.cpp) does less but without libraries
