DROP TABLE IF EXISTS 행정구역_읍면동;
DROP TABLE IF EXISTS 행정구역_시군구;
DROP TABLE IF EXISTS 행정구역_시도;

CREATE TABLE IF NOT EXISTS 행정구역_시도 (
    시도명 text,
    시도명_로마자 text,
    PRIMARY KEY (시도명)
);
CREATE TABLE IF NOT EXISTS 행정구역_시군구 (
    시도명 text,
    시도명_로마자 text,
    시군구명 text,
    시군구명_로마자 text,
    PRIMARY KEY (시도명, 시군구명),
    FOREIGN KEY (시도명) REFERENCES 행정구역_시도 (시도명)
);
CREATE TABLE IF NOT EXISTS 행정구역_읍면동 (
    시도명 text,
    시도명_로마자 text,
    시군구명 text,
    시군구명_로마자 text,
    읍면동명 text,
    읍면동명_로마자 text,
    PRIMARY KEY (시도명, 시군구명, 읍면동명),
    FOREIGN KEY (시도명, 시군구명) REFERENCES 행정구역_시군구 (시도명, 시군구명)
);

INSERT INTO 행정구역_시도 (시도명, 시도명_로마자)
SELECT DISTINCT 시도명, 시도명_로마자
FROM 도로명코드
;
INSERT INTO 행정구역_시군구 (시도명, 시도명_로마자, 시군구명, 시군구명_로마자)
SELECT DISTINCT 시도명, 시도명_로마자, 시군구명, 시군구명_로마자
FROM 도로명코드
WHERE 시군구명 IS NOT NULL
;
INSERT INTO 행정구역_읍면동 (시도명, 시도명_로마자, 시군구명, 시군구명_로마자, 읍면동명, 읍면동명_로마자)
SELECT DISTINCT 시도명, 시도명_로마자, 시군구명, 시군구명_로마자, 읍면동명, 읍면동명_로마자
FROM 도로명코드
WHERE 읍면동명 IS NOT NULL
;
