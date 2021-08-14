import geojson

file_path = r'C:\Users\Jihyung\Downloads\Traffic_Count_Locations.geojson'
with open(file_path) as f:
    gj = geojson.load(f)