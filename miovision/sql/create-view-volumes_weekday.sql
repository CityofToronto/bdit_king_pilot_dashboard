DROP MATERIALIZED VIEW IF EXISTS miovision.volumes_weekday;

CREATE MATERIALIZED VIEW miovision.volumes_weekday AS
SELECT intersection_uid, class_group, dir, leg, time_bin, AVG(B.average_volume) AS baseline_vol, AVG(P.average_volume) AS pilot_vol
FROM 	(SELECT * FROM miovision.volumes_by_dow WHERE count_type = 'Baseline') B
INNER JOIN (SELECT * FROM miovision.volumes_by_dow WHERE count_type = 'Pilot') P USING (intersection_uid, class_group, dow, time_bin, dir, leg)
WHERE dow <= 5 AND time_bin >= '6:00' AND time_bin < '22:00'
GROUP BY intersection_uid, class_group, dir, leg, time_bin;
