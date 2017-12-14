DROP TABLE IF EXISTS miovision.volumes_15min;

CREATE TABLE miovision.volumes_15min
(
	volume_15min_uid serial NOT NULL,
	intersection_uid integer,
	datetime_bin timestamp without time zone,
	classification_uid integer,
	leg text,
	movement_uid integer,
	volume integer
);
ALTER TABLE miovision.volumes_15min
  OWNER TO aharpal;
GRANT ALL ON TABLE miovision.volumes_15min TO rds_superuser WITH GRANT OPTION;
GRANT ALL ON TABLE miovision.volumes_15min TO dbadmin;
GRANT SELECT, REFERENCES, TRIGGER ON TABLE miovision.volumes_15min TO bdit_humans WITH GRANT OPTION;
GRANT ALL ON TABLE miovision.volumes_15min TO aharpal;