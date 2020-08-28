DROP TABLE IF EXISTS 행정구역_읍면동;
DROP TABLE IF EXISTS 행정구역_시군구;
DROP TABLE IF EXISTS 행정구역_시도;

CREATE TABLE IF NOT EXISTS 행정구역_시도 (
    시도명 text,
    영문시도명 text,
    GEOMETRY text,
    PRIMARY KEY (시도명)
);
CREATE TABLE IF NOT EXISTS 행정구역_시군구 (
    시도명 text,
    영문시도명 text,
    시군구명 text,
    영문시군구명 text,
    GEOMETRY text,
    PRIMARY KEY (시도명, 시군구명),
    FOREIGN KEY (시도명) REFERENCES 행정구역_시도 (시도명)
);
CREATE TABLE IF NOT EXISTS 행정구역_읍면동 (
    시도명 text,
    영문시도명 text,
    시군구명 text,
    영문시군구명 text,
    읍면동명 text,
    영문읍면동명 text,
    GEOMETRY text,
    PRIMARY KEY (시도명, 시군구명, 읍면동명),
    FOREIGN KEY (시도명, 시군구명) REFERENCES 행정구역_시군구 (시도명, 시군구명)
);

INSERT INTO 행정구역_시도 (시도명, 영문시도명, GEOMETRY)
SELECT 시도명, A.영문시도명, GEOMETRY
FROM (
    SELECT DISTINCT 시도명, 영문시도명
    FROM 도로명코드
) as A, 지리_시도 as B
WHERE A.영문시도명 = B.영문시도명
;

INSERT INTO 행정구역_시군구 (시도명, 영문시도명, 시군구명, 영문시군구명, GEOMETRY)
SELECT 시도명, A.영문시도명, 시군구명, A.영문시군구명, GEOMETRY
FROM (
    SELECT DISTINCT 시도명, 영문시도명, 시군구명, 영문시군구명
    FROM 도로명코드
    WHERE 시군구명 IS NOT NULL
) as A, 지리_시군구 as B
WHERE A.영문시도명 = B.영문시도명
    and A.영문시군구명 = B.영문시군구명
;

INSERT INTO 행정구역_읍면동 (시도명, 영문시도명, 시군구명, 영문시군구명, 읍면동명, 영문읍면동명, GEOMETRY)
SELECT 시도명, A.영문시도명, 시군구명, A.영문시군구명, 읍면동명, A.영문읍면동명, GEOMETRY
FROM (
    SELECT DISTINCT 시도명, 영문시도명, 시군구명, 영문시군구명, 읍면동명, 영문읍면동명
    FROM 도로명코드
    WHERE 시군구명 IS NOT NULL
) as A, 지리_읍면동 as B
WHERE A.영문시도명 = B.영문시도명
    and A.영문시군구명 = B.영문시군구명
    and A.영문읍면동명 = B.영문읍면동명
;
