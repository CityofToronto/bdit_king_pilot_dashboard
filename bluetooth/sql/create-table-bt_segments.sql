DROP TABLE IF EXISTS king_pilot.bt_segments;

CREATE TABLE king_pilot.bt_segments (
	bt_id int NOT NULL,
	analysis_id bigint NOT NULL,
	street_name text,
	direction text,
	from_intersection text,
	to_intersection text);