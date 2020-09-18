DROP TABLE IF EXISTS 지리_우편번호_SIMPLIFY;

CREATE TABLE IF NOT EXISTS 지리_우편번호_SIMPLIFY (
    시도명 text,
    시군구명 text,
    기초구역번호 text,
    GEOMETRY text,
    CENTER_COORDINATES text,
    PRIMARY KEY (기초구역번호)
);
