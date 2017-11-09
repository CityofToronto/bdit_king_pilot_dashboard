DROP TABLE IF EXISTS king_pilot.periods;

CREATE TABLE king_pilot.periods (
	period_id int NOT NULL,
	day_type text,
	period_name text,
	period_range timerange);
	
GRANT ALL ON TABLE king_pilot.periods TO aharpal;
GRANT SELECT ON TABLE king_pilot.periods TO public;