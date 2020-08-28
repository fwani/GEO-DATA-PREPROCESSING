# coding: utf-8
import os
import sys
import glob
import pathlib
import csv
import json
import shapely
import pandas as pd
import geopandas as gpd
import numpy as np

from itertools import repeat
from multiprocessing import cpu_count
from multiprocessing import Pool


def union_by_condition(data):
    df = data[0]
    category = data[1]
    last = data[2]

    if category['dong']:
        si_cols = ['시도명', '시도명_로마자']
        gu_cols = ['시군구명', '시군구명_로마자']
        dong_cols = ['읍면동명', '읍면동명_로마자']
        geo_col = ['geometry']

        df = df[si_cols + gu_cols + dong_cols + geo_col]
        result_df = df[si_cols + gu_cols + dong_cols].drop_duplicates()
        result_geo = []
        for row in result_df.iterrows():
            print(os.getpid(), row[1][0], row[1][2], row[1][4])
            condition = (df[si_cols[0]] == row[1][0]) & (df[si_cols[1]] == row[1][1]) \
                    & (df[gu_cols[0]] == row[1][2]) & (df[gu_cols[1]] == row[1][3]) \
                    & (df[dong_cols[0]] == row[1][4]) & (df[dong_cols[1]] == row[1][5])

            if last:
                result_geo.append(json.dumps(shapely.geometry.mapping(df[condition]['geometry'].unary_union)))
            else:
                result_geo.append(df[condition]['geometry'].to_crs(4326).unary_union.wkt)
        result_df['geometry'] = result_geo
    elif category['gu']:
        si_cols = ['CTP_KOR_NM']
        gu_cols = ['SIG_KOR_NM']
        geo_col = ['geometry']

        df = df[si_cols + gu_cols + geo_col]
        result_df = df[si_cols + gu_cols].drop_duplicates()
        result_geo = []
        for row in result_df.iterrows():
            # print(os.getpid(), row[1][0], row[1][2])
            # condition = (df[si_cols[0]] == row[1][0]) & (df[si_cols[1]] == row[1][1]) \
            #         & (df[gu_cols[0]] == row[1][2]) & (df[gu_cols[1]] == row[1][3])
            print(os.getpid(), row[1][0], row[1][1])
            condition = (df[si_cols[0]] == row[1][0]) & (df[gu_cols[0]] == row[1][1])
            if last:
                result_geo.append(json.dumps(shapely.geometry.mapping(df[condition]['geometry'].unary_union)))
            else:
                result_geo.append(df[condition]['geometry'].to_crs(4326).unary_union.wkt)
        result_df['geometry'] = result_geo
    elif category['si']:
        si_cols = ['CTP_KOR_NM']
        geo_col = ['geometry']

        df = df[si_cols + geo_col]
        result_df = df[si_cols].drop_duplicates()
        result_geo = []
        for row in result_df.iterrows():
            print(os.getpid(), row[1][0])
            condition = (df[si_cols[0]] == row[1][0])  # & (df[si_cols[1]] == row[1][1])
            if last:
                result_geo.append(json.dumps(shapely.geometry.mapping(df[condition]['geometry'].unary_union)))
            else:
                result_geo.append(df[condition]['geometry'].to_crs(4326).unary_union.wkt)
        result_df['geometry'] = result_geo

    return result_df


def parallelize_union_geometry(df, **kwargs):
    print('parall main')
    print(kwargs)
    
    num_cores = cpu_count()
    df_split = np.array_split(df, num_cores)
    pool = Pool(num_cores)
    df = pd.concat(pool.map(union_by_condition, list(zip(df_split, repeat(kwargs), repeat(False)))))
    pool.close()
    pool.join()
    geometry = df['geometry'].map(shapely.wkt.loads)
    df = gpd.GeoDataFrame(df, crs='epsg:4326', geometry=geometry)
    df = union_by_condition([df, kwargs, True])
    return df


def run(si=False, gu=False, dong=False):
    home = os.getenv('GEO_DATA_HOME')
    if dong:
        export_path = os.path.join(home, 'data/dong_test')
    elif gu:
        export_path = os.path.join(home, 'data/gu')
    elif si:
        export_path = os.path.join(home, 'data/si')
    else:
        raise Exception('select si, gu, dong')
    pathlib.Path(export_path).mkdir(parents=True, exist_ok=True)

    kwargs = {'si':si, 'gu':gu, 'dong':dong}

    if dong:
        shape_files = glob.glob(os.path.join(home, 'data/shape/*/*.shp'))
        print(shape_files)

        dorocode_df = pd.read_csv(os.path.join(home, 'data/address/개선_도로명코드_전체분.csv'), sep='|', encoding='utf-8', dtype=str)
        
        for shape_file in shape_files:
            si_name = shape_file.rsplit('/', 2)[1]
            print(si_name)

            juso_df = pd.read_csv(os.path.join(home, 'data/address/주소_{}.csv'.format(si_name)), sep='|', encoding='utf-8', dtype=str)
            jiri_df = gpd.read_file(shape_file, sep='|')

            joined_df = pd.merge(dorocode_df, juso_df, on=['도로명코드', '읍면동일련번호'], how='left')
            joined_df = pd.merge(jiri_df, joined_df, left_on='BAS_ID', right_on='기초구역번호', how='left')
            joined_df['geometry'].crs = 5179

            result_df = parallelize_union_geometry(joined_df, **kwargs)
            result_df.to_csv(
                    os.path.join(export_path, '{}.csv'.format(si_name)),
                    sep='|',
                    encoding='utf-8',
                    quoting=csv.QUOTE_NONE,
                    index=False)
    else:
        if gu:
            # file_paths = glob.glob(os.path.join(home, 'data/dong/*.csv'))
            file_paths = glob.glob(os.path.join(home, 'data/shape/*/*.shp'))
        elif si:
            file_paths = glob.glob(os.path.join(home, 'data/gu/*.csv'))

        for f_path in file_paths:
            if gu:
                si_name = f_path.rsplit('/', 2)[1]
                print(si_name)
                df = gpd.read_file(f_path, sep='|')
                df['geometry'].crs = 5179
            else:
                si_name = f_path.rsplit('/', 1)[-1].replace('.csv', '')
                print(si_name)
                df = pd.read_csv(f_path, sep='|', encoding='utf-8', dtype=str)
                geometry = df['geometry'].map(json.loads)
                geometry = geometry.map(shapely.geometry.shape)
                df = gpd.GeoDataFrame(df, crs='epsg:4326', geometry=geometry)
                #result_df = union_by_condition([df, kwargs, True])
            result_df = parallelize_union_geometry(df, **kwargs)

            result_df.to_csv(
                os.path.join(export_path, '{}.csv'.format(si_name)),
                sep='|',
                encoding='utf-8',
                quoting=csv.QUOTE_NONE,
                index=False)


if __name__ == '__main__':
    print('hello')
    if len(sys.argv) > 1:
        category = sys.argv[1]
    if category == 'dong':
        run(dong=True)
    elif category == 'gu':
        run(gu=True)
    elif category == 'si':
        run(si=True)
