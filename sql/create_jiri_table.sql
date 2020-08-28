DROP TABLE IF EXISTS 지리_기초구역;

CREATE TABLE IF NOT EXISTS 지리_기초구역 (
    시도명 text,
    시군구명 text,
    기초구역번호 text PRIMARY KEY,
    GEOMETRY text
);
