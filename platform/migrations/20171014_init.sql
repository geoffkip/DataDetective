DROP TABLE IF EXISTS data_points;

CREATE TABLE data_points (
  id SERIAL,
  data_set_id integer,
  county text,
  date date,
  measures json
);
