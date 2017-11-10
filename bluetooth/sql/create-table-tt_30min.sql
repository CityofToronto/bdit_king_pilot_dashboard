DROP TABLE IF EXISTS king_pilot.tt_30min;

CREATE TABLE king_pilot.tt_30min (
	bt_id int,
	dt date,
	time_bin time without time zone,
	tt numeric,
	obs bigint );
	
GRANT ALL ON TABLE king_pilot.tt_30min TO aharpal;
GRANT SELECT ON TABLE king_pilot.tt_30min TO public;