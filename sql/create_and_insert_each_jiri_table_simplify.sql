DROP TABLE IF EXISTS 지리_읍면동_SIMPLIFY;
DROP TABLE IF EXISTS 지리_시군구_SIMPLIFY;
DROP TABLE IF EXISTS 지리_시도_SIMPLIFY;

CREATE TABLE IF NOT EXISTS 지리_시도_SIMPLIFY (
    영문시도명 text,
    GEOMETRY text,
    CENTER_COORDINATES text,
    PRIMARY KEY (영문시도명)
);
CREATE TABLE IF NOT EXISTS 지리_시군구_SIMPLIFY (
    영문시도명 text,
    영문시군구명 text,
    GEOMETRY text,
    CENTER_COORDINATES text,
    PRIMARY KEY (영문시도명, 영문시군구명),
    FOREIGN KEY (영문시도명) REFERENCES 지리_시도_SIMPLIFY (영문시도명)
);
CREATE TABLE IF NOT EXISTS 지리_읍면동_SIMPLIFY (
    영문시도명 text,
    영문시군구명 text,
    영문읍면동명 text,
    GEOMETRY text,
    CENTER_COORDINATES text,
    PRIMARY KEY (영문시도명, 영문시군구명, 영문읍면동명),
    FOREIGN KEY (영문시도명, 영문시군구명) REFERENCES 지리_시군구_SIMPLIFY (영문시도명, 영문시군구명)
);
