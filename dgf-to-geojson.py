import re


def dgf_to_geojson(file_path):
    """
    Returns a Geojson Format Feature Collection. Only Valid for Point data at the moment
    :param file_path:
    :return: 
    """
    geojson = {"type": "FeatureCollection", "features": []}
    with open(file_path) as dgf:
        content = dgf.read()
    columns = [x.split(',')[0] for x in re.findall(r'COLUMN = (.*);', content)]
    data_arr = [x.split(',') for x in re.findall(r'DATA = (.*);', content)]
    point_arr = [x.split(',') for x in re.findall(r'POINT = (.*);', content)]
    geom_type = re.findall(r'TYPE = [a-zA-Z]+;', content)[0]
    features_raw = zip(point_arr, data_arr)
    if data_arr and geom_type == 'TYPE = POINT;':
        if len(data_arr[0]) == len(columns):
            for point, data in features_raw:
                geometry = {"type": "Point", "coordinates": [float(point[0]), float(point[1])]}
                properties = dict(zip(columns, data))
                geojson['features'].append({"type": "Feature", "geometry": geometry, "properties": properties})
    return geojson
