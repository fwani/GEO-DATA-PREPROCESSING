import os
import glob
import re
import pathlib
import csv
import psycopg2
import argparse
import json

# PostgreSQL 서버에 있는 테이블 (도로명코드, 도로명주소, 지번, 부가정보) 을 이용해 행정구역 테이블 생성
# 행정구역 테이블 종류 : 행정구역_시도, 행정구역_시군구, 행정구역_읍면동

def run(args):
    # connect to database
    home = os.getenv('GEO_DATA_HOME')

    print("Connect Database [{}]".format(args.database))
    conn = psycopg2.connect(host=args.host, port=args.port, user=args.user, password=args.password, dbname=args.database)
    cur = conn.cursor()
    conn.autocommit = True

    # create 행정구역 tables
    print("Create tables to [{}]".format(args.database))
    cur.execute(open(os.path.join(home, 'create_dministrative_district_table.sql'), 'r').read())


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
