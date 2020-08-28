import os
import glob
import re
import pathlib
import csv
import psycopg2
import argparse
import json
import geopandas as gpd

# 원본 데이터는 cp949 로 포멧팅되어 있음
# 데이터를 읽어 postgresql 서버로 데이터 insert

def run(args):
    home = os.getenv('GEO_DATA_HOME')
    downloaded_files = glob.glob(os.path.join(home, 'data/shape/*/*/*.shp'))

    # connect to database
    print("Connect Database [{}]".format(args.database))
    conn = psycopg2.connect(host=args.host, port=args.port, user=args.user, password=args.password, dbname=args.database)
    cur = conn.cursor()
    conn.autocommit = True

    # create tables
    print("Create tables to [{}]".format(args.database))
    cur.execute(open(os.path.join(home, 'sql/create_jiri_table.sql'), 'r').read())

    base_insert_sql = "INSERT INTO 지리_기초구역 VALUES {}"
    print(base_insert_sql)

    for f_path in downloaded_files:
        print("Read file from [{}]".format(f_path))

        df = gpd.read_file(f_path, sep='|')
        df = df[['BAS_ID', 'geometry']]
        df['geometry'].crs = 5179
        df['geometry'] = df['geometry'].to_crs(4326)
        all_rows = []
        print("Create sql query ...")
        for row in df.to_numpy():
            row[0] = row[0].strip()
            row[1] = row[1].wkt
            #print(row)
            #print(json.dumps(row))
            #print(base_insert_sql.format(table, json.dumps(row)))
            #print(base_insert_sql.format(table, "'" + "', '".join(row) + "'"))
            value_format = "(" + ', '.join(['%s'] * len(row)) + ")"
            all_rows.append(cur.mogrify(value_format, row).decode('utf-8'))
        print("Insert Data ...")
        cur.execute(base_insert_sql.format(','.join(all_rows)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Insert juso data to PostgreSQL')

    parser.add_argument('--host',
                        required=True,
                        type=str,
                        help='PostgreSQL host')
    parser.add_argument('--port',
                        required=True,
                        type=str,
                        help='PostgreSQL port')
    parser.add_argument('--user',
                        required=True,
                        type=str,
                        help='PostgreSQL user')
    parser.add_argument('--password',
                        required=True,
                        type=str,
                        help='PostgreSQL password')
    parser.add_argument('--database',
                        required=True,
                        type=str,
                        help='PostgreSQL database name')

    parsed_args = parser.parse_args()
    print(parsed_args)
    run(parsed_args)
