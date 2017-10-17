DROP sequence king_pilot_dash.corridor_id CASCADE;
--DROP TABLE king_pilot_dash.car_travel_times;
CREATE sequence king_pilot_dash.corridor_id;

CREATE MATERIALIZED VIEW king_pilot_dash.car_travel_times AS
WITH corridors AS(
SELECT nextval('king_pilot_dash.corridor_id') as corridor_id, UNNEST(ARRAY['Dundas', 'Queen', 'Front', 'Adelaide', 'Richmond', 'Wellington']) AS corridor
),
directions AS(
SELECT UNNEST(ARRAY['EB','WB']) AS dir
),
time_periods AS(
SELECT UNNEST(ARRAY['AM','PM']) AS time_period
),
months AS(
SELECT '2017-09-01'::DATE + Interval '1 month' * generate_series(0,3) as mon
)

SELECT corridor_id, corridor, dir, mon, time_period, to_char(random() * 10 + 5, '99.9') as travel_time
FROM corridors
CROSS JOIN directions
CROSS JOIN time_periods
CROSS JOIN months
WHERE NOT( corridor = 'Richmond' AND dir = 'EB') AND NOT( corridor = 'Adelaide' AND dir = 'WB');


DROP sequence IF EXISTS king_pilot_dash.street_car_seg_id CASCADE;
--DROP TABLE king_pilot_dash.car_travel_times;
CREATE sequence king_pilot_dash.street_car_seg_id;

CREATE MATERIALIZED VIEW king_pilot_dash.streetcar_travel_times AS
WITH segments AS(
SELECT nextval('king_pilot_dash.street_car_seg_id') as segment_id, 
UNNEST(ARRAY['Bathurst-Spadina', 'Spadina-University', 'University-Yonge', 'Yonge-Jarvis']) AS segment
),
directions AS(
SELECT UNNEST(ARRAY['EB','WB']) AS dir
),
time_periods AS(
SELECT UNNEST(ARRAY['AM','PM']) AS time_period
),
months AS(
SELECT '2017-09-01'::DATE + Interval '1 month' * generate_series(0,3) as mon
)

SELECT segment_id, segment, dir, mon, time_period, to_char(random() * 8 + 2, '99.9') as travel_time
FROM segments
CROSS JOIN directions
CROSS JOIN time_periods
CROSS JOIN months;


DROP VIEW king_pilot_dash.street_volumes_geojson;

CREATE OR REPLACE VIEW king_pilot_dash.street_volumes_geojson AS 
 SELECT json_build_object('type', 'FeatureCollection', 'features', array_to_json(array_agg(f.*))) AS geojson
   FROM ( SELECT 'Feature' AS type,
            st_asgeojson(street_volumes.geom, 15, 2)::json AS geometry,
            json_build_object('feature_code_desc', street_volumes.feature_code_desc, 'centreline_id', street_volumes.centreline_id, 'linear_name_full', street_volumes.linear_name_full, 'linear_name_id', street_volumes.linear_name_id, 'volume', street_volumes.volume, 'year', street_volumes.year, 'direction', street_volumes.direction, 'oneway_dir_code', street_volumes.oneway_dir_code, 'dir_bin', street_volumes.dir_bin, 'min_zoom', street_volumes.min_zoom, 'id', street_volumes.id, 'pct_change', (random() * 50::double precision - 25::double precision)::integer) AS properties
           FROM ryu4.streets_tiled_kingstreetpilot street_volumes) f;

ALTER TABLE king_pilot_dash.street_volumes_geojson
  OWNER TO rdumas;
GRANT ALL ON TABLE king_pilot_dash.street_volumes_geojson TO rdumas;
GRANT SELECT, REFERENCES ON TABLE king_pilot_dash.street_volumes_geojson TO bdit_humans;



DROP MATERIALIZED VIEW IF EXISTS king_pilot_dash.streetcar_reliability;
CREATE MATERIALIZED VIEW king_pilot_dash.streetcar_reliability AS
WITH directions AS(
SELECT UNNEST(ARRAY['EB','WB']) AS dir
),
time_periods AS(
SELECT UNNEST(ARRAY['AM','PM']) AS time_period
),
months AS(
SELECT '2017-09-01'::DATE + Interval '1 month' * generate_series(0,3) as mon
)

SELECT mon, dir, time_period, to_char(random() * 25 + 50, '99.9') as pct_reliable_headways
FROM directions
CROSS JOIN time_periods
CROSS JOIN months;
