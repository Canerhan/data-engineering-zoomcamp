~~~shell
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest_data.py \
  --table_name=yellow_taxi_trips \
  --url=${URL}
#   --user=root \
#   --password=root \
#   --host=localhost \
#   --port=5432 \
#   --db=ny_taxi \

~~~