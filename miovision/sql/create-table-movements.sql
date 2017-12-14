DROP TABLE IF EXISTS miovision.movements;

CREATE TABLE miovision.movements (
	movement_uid serial,
	movement text,
	location_only boolean);

ALTER TABLE miovision.movements
  OWNER TO aharpal;
GRANT ALL ON TABLE miovision.movements TO rds_superuser WITH GRANT OPTION;
GRANT ALL ON TABLE miovision.movements TO dbadmin;
GRANT SELECT, REFERENCES, TRIGGER ON TABLE miovision.movements TO bdit_humans WITH GRANT OPTION;
GRANT ALL ON TABLE miovision.movements TO aharpal;

INSERT INTO miovision.movements(movement, location_only) VALUES ('Thru', FALSE);
INSERT INTO miovision.movements(movement, location_only) VALUES ('Left', FALSE);
INSERT INTO miovision.movements(movement, location_only) VALUES ('Right', FALSE);
INSERT INTO miovision.movements(movement, location_only) VALUES ('U-Turn', FALSE);
INSERT INTO miovision.movements(movement, location_only) VALUES ('Peds CW', TRUE);
INSERT INTO miovision.movements(movement, location_only) VALUES ('Peds CCW', TRUE);