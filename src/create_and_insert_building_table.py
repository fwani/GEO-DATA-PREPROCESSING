import os
import glob
import re
import pathlib
import csv
import psycopg2
import argparse
import json

# 원본 데이터는 cp949 로 포멧팅되어 있음
# 데이터를 읽어 postgresql 서버로 데이터 insert

def run(args):
    home = os.getenv('GEO_DATA_HOME')
    downloaded_files = glob.glob(os.path.join(args.data_path, '*.txt'))

    prefix = {
        0: 'road_code_',
        1: 'build_',
        2: 'jibun_',
    }

    sorted_files = []
    for f in downloaded_files:
        for k, v in prefix.items():
            if re.search(v, f) is not None:
                sorted_files.append((k, f))

    sorted_files = sorted(sorted_files, key=lambda x: x[0])

    # connect to database
    if args.database is not None:
        dbname = args.database
    else:
        conn = psycopg2.connect(host=args.host, port=args.port, user=args.user, password=args.password)
        conn.autocommit = True
        cur = conn.cursor()
        dbname = 'build_db'
        print("Drop Database [{}]".format(dbname))
        cur.execute("""
            DROP DATABASE IF EXISTS {}
        """.format(dbname))
        print("Create Database [{}]".format(dbname))
        cur.execute("""
            CREATE DATABASE {}
            ENCODING 'UTF8'
        """.format(dbname))
    print("Connect Database [{}]".format(dbname))
    conn = psycopg2.connect(host=args.host, port=args.port, user=args.user, password=args.password, dbname=dbname)
    cur = conn.cursor()
    conn.autocommit = True

    # create tables
    print("Create tables to [{}]".format(dbname))
    cur.execute(open(os.path.join(home, 'sql/create_building_tables.sql'), 'r').read())

    base_insert_sql = "INSERT INTO {0} VALUES {1}"
    print(base_insert_sql)

    for k, f_path in sorted_files:
        print("Read file from [{}]".format(f_path))
        if k == 0:
            table = '도로명코드'
        elif k == 1:
            table = '건물정보'
        elif k == 2:
            table = '관련지번'
        else:
            continue

        csv_reader = csv.reader(open(f_path, 'r', encoding='cp949'), delimiter='|')
        all_rows = []
        print("Create sql query ...")
        for row in csv_reader:
            row = [None if r == '' else r.strip() for r in row]
            #print(row)
            #print(json.dumps(row))
            #print(base_insert_sql.format(table, json.dumps(row)))
            #print(base_insert_sql.format(table, "'" + "', '".join(row) + "'"))
            value_format = "(" + ', '.join(['%s'] * len(row)) + ")"
            all_rows.append(cur.mogrify(value_format, row).decode('utf-8'))
        print("Insert Data ...")
        cur.execute(base_insert_sql.format(table, ','.join(all_rows)))
    cur.execute("""
        UPDATE 도로명코드
        SET 시군구명 = ''
        WHERE 시도명 = '세종특별자치시'
    """)


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
                        required=False,
                        type=str,
                        help='PostgreSQL database name')
    parser.add_argument('--data-path',
                        required=True,
                        type=str,
                        help='Inserted data path')

    parsed_args = parser.parse_args()
    print(parsed_args)
    run(parsed_args)
