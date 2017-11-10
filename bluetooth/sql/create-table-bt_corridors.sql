DROP TABLE IF EXISTS king_pilot.bt_corridors;

CREATE TABLE king_pilot.bt_corridors (
	corridor_id int NOT NULL,
	corridor_name text,
	street_name text,
	direction text,
	segments int);

GRANT ALL ON TABLE king_pilot.bt_corridors TO aharpal;
GRANT SELECT ON TABLE king_pilot.bt_corridors TO public;