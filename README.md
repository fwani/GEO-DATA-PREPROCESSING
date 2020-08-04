# GEO-DATA-PREPROCESSING

## Developer Setup

### 1. Install jdk & Clone angora git
```bash
$ git clone https://github.com/fwani/GEO-DATA-PREPROCESSING.git
$ cd GEO-DATA-PREPROCESSING
```

### 2. Install virtualenv
```bash
$ virtualenv --no-site-packages --distribute --python=python3.6 venv
```

### 3. Activate virtualenv
```bash
$ source venv/bin/activate
```

### 4. Set environment key & value
```bash
$ source env.sh
```

### 5. Download python library
```bash
$ pip install -r requirements.txt
```

## 주소DB Data 포멧 변환

1. [주소DB](https://www.juso.go.kr/addrlink/addressBuildDevNew.do?menu=match) 에서 다운로드한 데이터 unzip 명령어 실행
  - 파일은 `$GEO_DATA_HOME/data/address_cp949/` 경로에 압축해제 됨

```bash
$ data_unzip.sh <downloaded juso data>
```

2. unzip 한 파일들을 `cp949` 포멧에서 `utf-8`의 csv 파일로 변환

```bash
$ python preprocessing_juso_data.py
```

## 전자지도 전처리
- [기초구역도](https://www.juso.go.kr/addrlink/addressBuildDevNew.do?menu=bsin) 에서 다운로드한 데이터를 이용해 생성한 geojson 파일을 csv 파일로 변환 하는 과정
  - 다운로드 시에는 `.shp` 등의 파일이 있음
  - `qgis` 와 같은 프로그램을 이용해 해당 파일을 로드하여 geojson 으로 export

```bash
$ python preprocessing_geojson_to_csv.py
```
