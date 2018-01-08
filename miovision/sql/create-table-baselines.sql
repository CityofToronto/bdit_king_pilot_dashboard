DROP TABLE IF EXISTS miovision.baselines;

CREATE TABLE miovision.baselines (
	baseline_uid serial,
	intersection_uid integer,
	day_type text,
	time_bin time without time zone,
	leg text,
	dir text,
	volume
	);