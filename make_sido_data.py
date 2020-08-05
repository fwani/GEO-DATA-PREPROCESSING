# coding: utf-8
import os
import pandas as pd
import geopandas as gpd

from shapely import wkt

home = os.getenv('GEO_DATA_HOME')
spark_home = os.getenv('SPARK_HOME')
export_path = os.path.join(home, 'data/dong')

dorocode_df = pd.read_csv(os.path.join(home, 'data/address/개선_도로명코드_전체분.csv'), sep='|', encoding='utf-8')
juso_df = pd.read_csv(os.path.join(home, 'data/address/주소_서울특별시.csv'), sep='|', encoding='utf-8')
jiri_df = pd.read_csv(os.path.join(home, 'data/jiri/서울특별시.csv'), sep='|', encoding='utf-8')
jiri_df['GEOMETRY'] = jiri_df['GEOMETRY'].apply(wkt.loads)
jiri_df = gpd.GeoDataFrame(jiri_df, crs='epsg:4326')

joined_df = pd.merge(dorocode_df, juso_df, on=['도로명코드', '읍면동일련번호'], how='left')
joined_df = pd.merge(joined_df, jiri_df, left_on='기초구역번호', right_on='BAS_ID', how='left')

print(joined_df.dropna(subset=['GEOMETRY']))


'''
sido_list = dorocode_df.select('시도명').distinct().collect()
for sido in sido_list[:1]:
    juso_df = df_reader.load(os.path.join(home, 'data/address/주소_{}.csv'.format(sido['시도명'])))
    jiri_df = df_reader.load(os.path.join(home, 'data/jiri/{}.csv'.format(sido['시도명'])))

    joined_df = dorocode_df \
            .join(
                juso_df,
                ['도로명코드', '읍면동일련번호'])
    joined_df = joined_df.join(
                jiri_df,
                [joined_df['기초구역번호'] == jiri_df['BAS_ID']]).dropna(subset='시도명')
    print(joined_df.count())

    # 읍면동
    select_cols = ['시도명', '시도명_로마자', '시군구명', '시군구명_로마자', '읍면동명', '읍면동명_로마자', '도로명', '기초구역번호', 'GEOMETRY']
    joined_df.select(select_cols)\
        .write.mode('overwrite').format("com.databricks.spark.csv")\
        .option("header", "true")\
        .option("sep", '|')\
        .save(os.path.join(export_path, '{}.csv'.format(sido['시도명'])))
#   joined_df.select(select_cols).toPandas().to_csv(
#           os.path.join(export_path, '{}.csv'.format(sido['시도명'])),
#           sep='|',
#           encoding='utf-8',
#           index=False)
'''
# 시도
'''
select_cols = ['시도명', '시도명_로마자', 'GEOMETRY']
sido_list = dorocode_df.select('시도명').distinct().collect()
print(sido_list)
print(sido_list[0])
df = joined_df.where(F.col('시도명') == sido_list[12]['시도명']).select(select_cols).limit(20)
col = df.selectExpr("ST_Boundary(ST_GeomFromGeoJSON(GEOMETRY)) as GEOMETRY")['GEOMETRY']
df = df.select(['시도명', '시도명_로마자']).distinct().withColumn('GEOMETRY', col)
df.show(truncate=False)
'''
# 시군구
'''
select_cols = ['시도명', '시도명_로마자', '시군구명', '시군구명_로마자', 'GEOMETRY']
sido_gu_list = dorocode_df.select(['시도명', '시군구명']).distinct().collect()
for sigu in sido_gu_list[:1]:
    df = joined_df.where(F.col('시도명') == sigu['시도명'])\
        .where(F.col('시군구명') == sigu['시군구명']) \
        .select(select_cols)
    geo_value = df.dropna(subset='GEOMETRY').selectExpr("ST_Union_Aggr(ST_GeomFromGeoJSON(GEOMETRY)) as GEOMETRY").collect()
    df = df.select(select_cols[:-1]).distinct().withColumn('GEOMETRY', F.lit(geo_value[0]['GEOMETRY'].wkt))

a = df.collect()
print(len(a))
print(a[0]['GEOMETRY'])
'''
