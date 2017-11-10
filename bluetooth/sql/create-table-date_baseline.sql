DROP TABLE IF EXISTS king_pilot.date_baseline;

CREATE TABLE king_pilot.date_baseline (
	bt_id int,
	day_type text,
	dt date);
	
GRANT ALL ON TABLE king_pilot.date_baseline TO aharpal;
GRANT SELECT ON TABLE king_pilot.date_baseline TO public;