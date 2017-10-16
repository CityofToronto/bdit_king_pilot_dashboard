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
SELECT UNNEST(ARRAY['2017-10-01', '2017-11-01']) as mon
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
SELECT UNNEST(ARRAY['2017-10-01', '2017-11-01']) as mon
)

SELECT segment_id, segment, dir, mon, time_period, to_char(random() * 8 + 2, '99.9') as travel_time
FROM segments
CROSS JOIN directions
CROSS JOIN time_periods
CROSS JOIN months;


CREATE VIEW king_pilot_dash.street_volumes_geojson AS

SELECT json_build_object('type','FeatureCollection', 'features', array_to_json(array_agg(f))) as geojson
FROM(

	SELECT 'Feature' AS type, ST_ASGeoJSON(geom)::json AS geometry, row_to_json((feature_code_desc, centreline_id, linear_name_full, linear_name_id, 
	       volume, year,  direction, oneway_dir_code, dir_bin, min_zoom, 
	       id, pct_change)) as properties
	  FROM king_pilot_dash.street_volumes
	) f

;

CREATE MATERIALIZED VIEW king_pilot_dash.streetcar_reliability AS
WITH directions AS(
SELECT UNNEST(ARRAY['EB','WB']) AS dir
),
time_periods AS(
SELECT UNNEST(ARRAY['AM','PM']) AS time_period
),
months AS(
SELECT UNNEST(ARRAY['2017-10-01', '2017-11-01']) as mon
)

SELECT mon, dir, time_period, to_char(random() * 25 + 50, '99.9') as pct_reliable_headways
FROM directions
CROSS JOIN time_periods
CROSS JOIN months;
