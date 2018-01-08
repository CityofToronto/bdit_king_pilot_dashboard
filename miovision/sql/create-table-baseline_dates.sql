DROP TABLE IF EXISTS miovision.baseline_dates;

CREATE TABLE miovision.baseline_dates (
	baseline_dates_uid serial,
	intersection_uid integer,
	day_type text,
	dt date
	);