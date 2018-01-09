DROP TABLE IF EXISTS miovision.baselines_agg;

CREATE TABLE miovision.baselines_agg (
	baseline_agg_uid serial NOT NULL,
	intersection_uid integer,
	classification_uid integer,
	leg text,
	dir text,
	period_id integer,
	total_volume numeric
	);
	