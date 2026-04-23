CREATE TABLE states(
state_code INT PRIMARY KEY,
state_name VARCHAR(100)
);

CREATE TABLE districts(
district_code INT PRIMARY KEY,
state_code INT,
district_name VARCHAR(100)
);

CREATE TABLE subdistricts(
subdistrict_code INT PRIMARY KEY,
district_code INT,
subdistrict_name VARCHAR(100)
);

CREATE TABLE villages(
village_code BIGINT PRIMARY KEY,
subdistrict_code INT,
village_name VARCHAR(150)
);