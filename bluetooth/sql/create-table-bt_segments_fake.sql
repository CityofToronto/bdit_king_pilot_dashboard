DROP TABLE IF EXISTS king_pilot.bt_segments_fake;

CREATE TABLE king_pilot.bt_segments_fake (
	bt_id int NOT NULL,
	analysis_id bigint NOT NULL,
	street_name text,
	direction text,
	from_intersection text,
	to_intersection text);
	
GRANT ALL ON TABLE king_pilot.bt_segments_fake TO aharpal;
GRANT SELECT ON TABLE king_pilot.bt_segments_fake TO public;