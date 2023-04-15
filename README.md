populate postgres database with osm data:



osm2pgsql -c -d osm -U postgres -W -H localhost czech-republic-latest.osm.pbf


psql --host=localhost --port=5432 --username=postgres             


