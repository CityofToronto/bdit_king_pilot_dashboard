DROP TABLE IF EXISTS king_pilot.bt_corridor_segments;

CREATE TABLE king_pilot.bt_corridor_segments (
	corridor_segment_id int NOT NULL,
	corridor_id int,
	bt_id int,
	order_id int);
	
GRANT ALL ON TABLE king_pilot.bt_corridor_segments TO aharpal;
GRANT SELECT ON TABLE king_pilot.bt_corridor_segments TO public;