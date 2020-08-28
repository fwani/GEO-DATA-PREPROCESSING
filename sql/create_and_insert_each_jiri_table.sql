DROP TABLE IF EXISTS 지리_읍면동;
DROP TABLE IF EXISTS 지리_시군구;
DROP TABLE IF EXISTS 지리_시도;

CREATE TABLE IF NOT EXISTS 지리_시도 (
    영문시도명 text,
    GEOMETRY text,
    PRIMARY KEY (영문시도명)
);
CREATE TABLE IF NOT EXISTS 지리_시군구 (
    영문시도명 text,
    영문시군구명 text,
    GEOMETRY text,
    PRIMARY KEY (영문시도명, 영문시군구명),
    FOREIGN KEY (영문시도명) REFERENCES 지리_시도 (영문시도명)
);
CREATE TABLE IF NOT EXISTS 지리_읍면동 (
    영문시도명 text,
    영문시군구명 text,
    영문읍면동명 text,
    GEOMETRY text,
    PRIMARY KEY (영문시도명, 영문시군구명, 영문읍면동명),
    FOREIGN KEY (영문시도명, 영문시군구명) REFERENCES 지리_시군구 (영문시도명, 영문시군구명)
);
