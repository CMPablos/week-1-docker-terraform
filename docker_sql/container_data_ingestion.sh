
TRIP_DATA_URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"
ZONE_DATA_URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
USER=root
PASS=root
HOST=pgdatabase
PORT=5432
DB=ny_taxi

echo "----------Ingesting $TRIP_DATA_URL"
docker run --rm -it \
    --network=week_1_docker_terraform_default \
    taxi_ingest:v001 \
    --user=$USER \
    --password=$PASS \
    --host=$HOST \
    --port=$PORT \
    --db=$DB \
    --table_name=green_taxi_data \
    --url=${TRIP_DATA_URL}

echo "----------Ingesting $ZONE_DATA_URL"
docker run --rm -it \
    --network=week_1_docker_terraform_default \
    taxi_ingest:v001 \
    --user=$USER \
    --password=$PASS \
    --host=$HOST \
    --port=$PORT \
    --db=$DB \
    --table_name=zones \
    --url=${ZONE_DATA_URL}
