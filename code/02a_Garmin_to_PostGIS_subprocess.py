import subprocess
import os

path = r'..\_garmin_connect_export' # folder of your gpx files

for file in os.listdir(path):
    if file.endswith('.gpx'):
        filename = os.path.join(path, file)
        subprocess.call('ogr2ogr -append -f PostgreSQL "PG:dbname=test host=localhost user=foo password=bar" '+ filename)