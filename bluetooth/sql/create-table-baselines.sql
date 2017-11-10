DROP TABLE IF EXISTS king_pilot.baselines;

CREATE TABLE king_pilot.baselines (
	bt_id int,
	day_type text,
	time_bin time without time zone,
	tt numeric,
	obs bigint );
	
GRANT ALL ON TABLE king_pilot.baselines TO aharpal;
GRANT SELECT ON TABLE king_pilot.baselines TO public;