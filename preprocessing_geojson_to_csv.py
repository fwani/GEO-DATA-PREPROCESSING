import os
import glob
import json
import pathlib
import csv


home = os.getenv('GEO_DATA_HOME')
file_paths = glob.glob(os.path.join(home, 'data/geojson/*.geojson'))
export_path = os.path.join(home, 'data/jiri')

pathlib.Path(export_path).mkdir(parents=True, exist_ok=True)

for f_path in file_paths:
    print(f_path)
    tmp = json.loads(open(f_path).read())
    name = tmp['name']
    keys = list(tmp['features'][0]['properties'].keys())
    keys.append('GEOMETRY')
    values = []
    for feature in tmp['features']:
        val_tmp = list(feature['properties'].values())
        val_tmp.append(json.dumps(feature['geometry'], ensure_ascii=False))
        values.append(val_tmp)

    with open(os.path.join(home, export_path, '{}.csv'.format(name)), 'w', encoding='utf-8') as f:
        cw = csv.writer(f, delimiter='|', quotechar="'")
        cw.writerow(keys)
        cw.writerows(values)
