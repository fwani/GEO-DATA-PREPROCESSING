import os
import glob
import re
import pathlib
import csv
import psycopg2
import argparse
import json
import geopandas as gpd
import pandas as pd

# 원본 데이터는 cp949 로 포멧팅되어 있음
# 데이터를 읽어 postgresql 서버로 데이터 insert

def insert_table(cur, df, base_insert_sql, table_name):
    df['geometry'].crs = 5179
    df['geometry'] = df['geometry'].to_crs(4326)
    print(df)
    all_rows = []
    print("Create sql query ...")
    for row in df.to_numpy():
        tmp = [r.strip() for r in row[:-1]]
        geometry = row[-1].wkt
        cent = row[-1].centroid.wkt

        row = tmp + [geometry, cent]

        value_format = "(" + ', '.join(['%s'] * len(row)) + ")"
        all_rows.append(cur.mogrify(value_format, row).decode('utf-8'))
    print("Insert Data ...")
    cur.execute(base_insert_sql.format(table_name, ','.join(all_rows)))

def run(args):
    home = os.getenv('GEO_DATA_HOME')
    jiri_files = glob.glob(os.path.join(home, 'data/shape/*기초구역DB_전체분/*/*_simplify.shp'))
    print(jiri_files)

    conn = psycopg2.connect(host=args.host, port=args.port, user=args.user, password=args.password, dbname=args.database)
    cur = conn.cursor()
    conn.autocommit = True

    # create tables
    print("Create tables to [{}]".format(args.database))
    cur.execute(open(os.path.join(home, 'sql/create_and_insert_zipcode_jiri_table_simplify.sql'), 'r').read())
    for jiri_file in jiri_files:
        print(jiri_file)
        jiri_df = gpd.read_file(jiri_file, sep='|', encoding='cp949')[['CTP_KOR_NM', 'SIG_KOR_NM', 'BAS_ID', 'geometry']]
        print(jiri_df[jiri_df['geometry'] == None])

        base_insert_sql = "INSERT INTO {} VALUES {}"
        print(base_insert_sql)

        print("Start insert 지리_우편번호")
        insert_table(cur, jiri_df, base_insert_sql, '지리_우편번호_SIMPLIFY')
'''
    category_columns = {
        'CTP': ['CTPRVN_CD', 'CTP_ENG_NM', 'geometry'],
        'SIG': ['SIG_CD', 'SIG_ENG_NM', 'geometry'],
        'EMD': ['EMD_CD', 'EMD_ENG_NM', 'geometry']
    }

    si_df = gpd.read_file(si_file, sep='|', encoding='cp949')[category_columns['CTP']]
    si_df.loc[si_df['CTP_ENG_NM'] == 'Jellanam-do', 'CTP_ENG_NM'] = 'Jeollanam-do'
    gu_df = gpd.read_file(gu_file, sep='|', encoding='cp949')[category_columns['SIG']]
    dong_df = gpd.read_file(dong_file, sep='|', encoding='cp949')[category_columns['EMD']]

    category_keys = {
        'CTP': '지리_시도',
        'SIG': '지리_시군구',
        'EMD': '지리_읍면동'
    }

    # connect to database
    print("Connect Database [{}]".format(args.database))
    conn = psycopg2.connect(host=args.host, port=args.port, user=args.user, password=args.password, dbname=args.database)
    cur = conn.cursor()
    conn.autocommit = True

    # create tables
    print("Create tables to [{}]".format(args.database))
    cur.execute(open(os.path.join(home, 'sql/create_and_insert_each_jiri_table.sql'), 'r').read())

    base_insert_sql = "INSERT INTO {} VALUES {}"
    print(base_insert_sql)

    print("Start insert 지리_시도")
    insert_table(cur, si_df[['CTP_ENG_NM', 'geometry']], base_insert_sql, category_keys['CTP'])

    result_gu_df = None
    for row in si_df[['CTPRVN_CD', 'CTP_ENG_NM']].to_numpy():
        tmp = gu_df[gu_df['SIG_CD'].str.startswith(row[0])]
        tmp['CTP_ENG_NM'] = row[1]
        if result_gu_df is None:
            result_gu_df = tmp
        else:
            result_gu_df = pd.concat([result_gu_df,tmp], ignore_index=True)
    print("Start insert 지리_시군구")
    insert_table(cur, result_gu_df[['CTP_ENG_NM', 'SIG_ENG_NM', 'geometry']], base_insert_sql, category_keys['SIG'])

    result_dong_df = None
    for row in result_gu_df[['SIG_CD', 'SIG_ENG_NM', 'CTP_ENG_NM']].to_numpy():
        tmp = dong_df[dong_df['EMD_CD'].str.startswith(row[0])]
        tmp['SIG_ENG_NM'] = row[1]
        tmp['CTP_ENG_NM'] = row[2]
        if result_dong_df is None:
            result_dong_df = tmp
        else:
            result_dong_df = pd.concat([result_dong_df,tmp], ignore_index=True)
    print("Start insert 지리_읍면동")
    insert_table(cur, result_dong_df[['CTP_ENG_NM', 'SIG_ENG_NM', 'EMD_ENG_NM', 'geometry']], base_insert_sql, category_keys['EMD'])
'''

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
