DROP TABLE IF EXISTS 행정구역_우편번호;

CREATE TABLE IF NOT EXISTS 행정구역_우편번호 (
    시도명 text,
    시군구명 text,
    읍면동명 text,
    우편번호 text,
    건축물대장_건물명 text,
    상세건물명 text,
    시군구용_건물명 text,
    GEOMETRY text,
    CENTER_COORDINATES text
);

INSERT INTO 행정구역_우편번호
SELECT A.시도명, A.시군구명, A.행정동명, A.우편번호, A.건축물대장_건물명, A.상세건물명, A.시군구용_건물명, GEOMETRY, CENTER_COORDINATES
FROM (
    SELECT DISTINCT 시도명, 시군구명, 행정동명, 우편번호, 건축물대장_건물명, 상세건물명, 시군구용_건물명
    FROM 건물정보
    WHERE 건축물대장_건물명 is not null
) as A, 지리_우편번호 as B
WHERE A.우편번호 = B.기초구역번호
;
