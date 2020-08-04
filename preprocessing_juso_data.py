import os
import glob
import re
import pathlib

from pyspark.sql import SparkSession

# 원본 데이터는 cp949 로 포멧팅되어 있음
# 서비스에 올리기 위해 utf-8 로 변경

home = os.getenv('GEO_DATA_HOME')
downloaded_files = glob.glob(os.path.join(home, 'data/address_cp949/*.txt'))
export_path = os.path.join(home, 'data/address')

pathlib.Path(export_path).mkdir(parents=True, exist_ok=True)

dorocode = '도로명코드_'
juso = '주소_'
jibeon = '지번_'
buga = '부가정보_'

dorocode_fields = [
    '도로명코드',
    '도로명',
    '도로명_로마자',
    '읍면동일련번호',
    '시도명',
    '시도명_로마자',
    '시군구명',
    '시군구명_로마자',
    '읍면동명',
    '읍면동명_로마자',
    '읍면동구분',
    '읍면동코드',
    '사용여부',
    '변경사유',
    '변경이력정보',
    '고시일자',
    '말소일자'
]
juso_fields = [
    '관리번호',
    '도로명코드',
    '읍면동일련번호',
    '지하여부',
    '건물본번',
    '건물부번',
    '기초구역번호',
    '변경사유코드',
    '고시일자',
    '변경전도로명주소',
    '상세주소부여여부'
]
jibeon_fields = [
    '관리번호',
    '일련번호',
    '법정동코드',
    '시도명',
    '시군구명',
    '법정읍면동명',
    '법정리명',
    '산여부',
    '지번본번',
    '지번부번',
    '대표여부'
]
buga_fields = [
    '관리번호',
    '행정동코드',
    '행정동명',
    '우편번호',
    '우편번호일련번호',
    '다량배달처명',
    '건축물대장건물명',
    '시군구건물명',
    '공동주택여부'
]

spark = SparkSession.builder \
    .master("local") \
    .appName("format converter") \
    .getOrCreate()

df_reader = spark.read.format('csv') \
        .option('header', False) \
        .option('delimiter', '|') \
        .option('encoding', 'cp949')

for f_path in downloaded_files:

    print(f_path)
    if dorocode in f_path:
        df = df_reader.load(f_path).toDF(*dorocode_fields)
    elif juso in f_path:
        df = df_reader.load(f_path).toDF(*juso_fields)
    elif jibeon in f_path:
        df = df_reader.load(f_path).toDF(*jibeon_fields)
    elif buga in f_path:
        df = df_reader.load(f_path).toDF(*buga_fields)
    else:
        continue

    df2 = df.toPandas().to_csv(
            os.path.join(export_path, f_path.rsplit('/')[-1].replace('.txt', '.csv')),
            sep='|',
            encoding='utf-8',
            index=False)


