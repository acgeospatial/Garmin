import os
import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine, text, inspect

engine = create_engine("postgresql://postgres:mypassword@localhost:5432/mydatabase")

path = r'..\garmin_connect_export'

# Check if the table exists
inspector = inspect(engine)

if inspector.has_table('activity_track'):
    with engine.begin() as conn:
        existing_ids = {
            int(row[0]) for row in conn.execute(text("SELECT DISTINCT activity_id FROM activity_track"))
        }
else:
    existing_ids = set()

data = []

for file in os.listdir(path):
    if file.endswith('.gpx'):
        filename = os.path.join(path, file)
        activity_number = int(file.replace('activity_', '')[:-4])

        if activity_number in existing_ids:
            continue

        gdf = gpd.read_file(filename, layer='tracks')
        gdf['activity_id'] = activity_number
        gdf['name'] = gdf.get('name', None)
        gdf['type'] = gdf.get('type', None)

        data.append(gdf[['activity_id', 'name', 'type', 'geometry']])

if data:
    track_df = pd.concat(data, ignore_index=True)
    track_gdf = gpd.GeoDataFrame(track_df, geometry='geometry')
    track_gdf = track_gdf.to_crs('EPSG:32630')

    # Create table if it doesn't exist
    track_gdf.to_postgis("activity_track", engine, if_exists='append', index=False)
    print(f"Inserted {len(track_gdf)} new activities.")
else:
    print("No new activities to insert.")
