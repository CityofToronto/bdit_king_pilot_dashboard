DROP MATERIALIZED VIEW IF EXISTS  miovision.volumes_by_dow;

CREATE MATERIALIZED VIEW miovision.volumes_by_dow AS
	WITH vol_by_class AS (
		SELECT	intersection_uid,
			datetime_bin,
			dir,
			leg,
			CASE WHEN classification_uid IN (1,4,5) THEN 'Vehicles' WHEN classification_uid IN (2,7) THEN 'Bicycles' WHEN classification_uid IN (6) THEN 'Pedestrians' END AS class_group,
			SUM(volume) AS total_volume
		FROM 	miovision.volumes_15min
		WHERE 	classification_uid NOT IN (3)
		GROUP BY intersection_uid, datetime_bin, dir, leg, CASE WHEN classification_uid IN (1,4,5) THEN 'Vehicles' WHEN classification_uid IN (2,7) THEN 'Bicycles' WHEN classification_uid IN (6) THEN 'Pedestrians' END
		ORDER BY intersection_uid, datetime_bin, dir, leg
	)


	SELECT 	intersection_uid,
		class_group,
		EXTRACT(isodow FROM datetime_bin) AS dow,
		datetime_bin::time AS time_bin,
		CASE WHEN datetime_bin <= '2017-11-11' THEN 'Baseline' ELSE 'Pilot' END AS count_type,
		dir, 
		leg,
		AVG(total_volume) AS average_volume,
		COUNT(*) AS obs
	FROM 	vol_by_class
	INNER JOIN miovision.valid_intersection_legs USING (intersection_uid, dir, leg, class_group)
	GROUP BY intersection_uid, class_group, EXTRACT(isodow FROM datetime_bin), datetime_bin::time, CASE WHEN datetime_bin <= '2017-11-11' THEN 'Baseline' ELSE 'Pilot' END, dir, leg 
	ORDER BY intersection_uid, class_group, CASE WHEN datetime_bin <= '2017-11-11' THEN 'Baseline' ELSE 'Pilot' END, EXTRACT(isodow FROM datetime_bin), datetime_bin::time, dir, leg


