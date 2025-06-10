import os
from qgis.core import QgsVectorLayer, QgsProject

# Path to your GPX directory
gpx_dir = r".\YYYY-MM-DD_garmin_connect_export"

# Loop through all .gpx files
for filename in os.listdir(gpx_dir):
   if filename.lower().endswith('.gpx'):
      gpx_path = os.path.join(gpx_dir, filename)

      # 'tracks' layer
      track_lyr = f"{gpx_path}|layername=tracks"
      layer = QgsVectorLayer(track_lyr, f"Tracks - {filename}", "ogr")

      if layer.isValid():
         QgsProject.instance().addMapLayer(layer)
         print(f"Loaded 'tracks' layer from {filename}")
      else:
         print(f"Failed to load 'tracks' from {filename}")