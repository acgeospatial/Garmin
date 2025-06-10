import pandas as pd
import geopandas as gpd
import os
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:mypassword@localhost:5432/mydatabase")

path = r'..\garmin_connect_export'
data = []

for file in os.listdir(path):
    if file.endswith('.gpx'):
        filename = os.path.join(path, file)
        activity_number = file.replace('activity_', '')
        gdf = gpd.read_file(filename, layer = 'tracks')  
        gdf['activity'] = activity_number[:-4]
        data.append(gdf[['activity', 'name', 'type', 'geometry']])

track_df = pd.concat(data, ignore_index=True)
track_gdf = gpd.GeoDataFrame(track_df, geometry='geometry')
track_gdf = track_gdf.to_crs('EPSG:32630')
track_gdf.to_postgis("activity_track", engine)