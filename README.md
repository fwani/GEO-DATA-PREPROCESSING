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

## 전처리
### 1. 주소 Data 포멧 변환

1. [주소DB](https://www.juso.go.kr/addrlink/addressBuildDevNew.do?menu=match) 에서 다운로드한 데이터 unzip 명령어 실행
  - 파일은 `$GEO_DATA_HOME/data/address_cp949/` 경로에 압축해제 됨

```bash
$ data_unzip.sh <downloaded juso data>
```

2. unzip 한 파일들을 `cp949` 포멧에서 `utf-8`의 csv 파일로 변환
  - 변환된 파일은 `$GEO_DATA_HOME/data/address/` 경로에 저장됨

```bash
$ python preprocessing_juso_data.py
```

### 2. 전자지도 전처리
1. [기초구역도](https://www.juso.go.kr/addrlink/addressBuildDevNew.do?menu=bsin) 데이터 다운로드
2. `.shp` 데이터를 이용해 geojson 파일 생성
  - 제공되는 데이터의 좌표계는 `EPSG:102080`
  - geojson으로 만들때는 `EPSG:4326` 으로 변경
  - `qgis` 와 같은 프로그램을 사용하여 geojson 으로 export 할 수 있음
3. 생성한 geojson 파일을 `$GEO_DATA_HOME/data/geojson` 경로에 저장
4. 아래 명령어를 실행하여 geojson -> csv 로 변경
  - csv 파일은 `$GEO_DATA_HOME/data/jiri/` 경로에 저장됨

```bash
$ python preprocessing_geojson_to_csv.py
```

## 시도, 시군구, 읍면동 데이터로 데이터 조인&분리

