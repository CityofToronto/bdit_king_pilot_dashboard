DROP TABLE IF EXISTS king_pilot.date_lookup;

CREATE TABLE king_pilot.date_lookup (
	dt date,
	day_type text,
	category text);
	
GRANT ALL ON TABLE king_pilot.periods TO aharpal;
GRANT SELECT ON TABLE king_pilot.periods TO public;