DROP TABLE IF EXISTS 부가정보;
DROP TABLE IF EXISTS 지번;
DROP TABLE IF EXISTS 도로명주소;
DROP TABLE IF EXISTS 도로명코드;

CREATE TABLE IF NOT EXISTS 도로명코드 (
    도로명코드 text,
    도로명 text,
    도로명_로마자 text,
    읍면동일련번호 text,
    시도명 text,
    시도명_로마자 text,
    시군구명 text,
    시군구명_로마자 text,
    읍면동명 text,
    읍면동명_로마자 text,
    읍면동구분 text,	
    읍면동코드 text,	
    사용여부 text,
    변경사유 text,
    변경이력정보 text,
    고시일자 text,
    말소일자 text,
    PRIMARY KEY (도로명코드, 읍면동일련번호)
);
CREATE TABLE IF NOT EXISTS 도로명주소 (
    관리번호 text PRIMARY KEY,
    도로명코드 text,
    읍면동일련번호 text,
    지하여부 text,
    건물본번 integer,
    건물부번 integer,
    기초구역번호 text,
    변경사유_코드 text,
    고시일자 text,
    변경전_도로명주소 text,
    상세주소_부여여부 text,
    FOREIGN KEY (도로명코드, 읍면동일련번호) REFERENCES 도로명코드 (도로명코드, 읍면동일련번호)
);
CREATE TABLE IF NOT EXISTS 지번 (
    관리번호 text REFERENCES 도로명주소,
    일련번호 integer,
    법정동코드 text,
    시도명 text,
    시군구명 text,
    법정읍면동명 text,
    법정리명 text,
    산여부 text,
    지번본번 integer,
    지번부번 integer,
    대표여부 text,
    PRIMARY KEY (관리번호, 일련번호)
);
CREATE TABLE IF NOT EXISTS 부가정보 (
    관리번호 text PRIMARY KEY REFERENCES 도로명주소,
    행정동_코드 text,
    행정동명 text,
    우편번호 text,
    우편번호일련번호 text,
    다량배달처명 text,
    건축물대장_건물명 text,
    시군구_건물명 text,
    공동주택여부 text
);

