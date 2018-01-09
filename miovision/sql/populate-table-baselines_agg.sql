TRUNCATE miovision.baselines_agg;

INSERT INTO miovision.baselines_agg (intersection_uid, classification_uid, leg, dir, period_id, total_volume)
SELECT A.intersection_uid, A.classification_uid, A.leg, A.dir, B.period_id, SUM(volume) AS total_volume

FROM	miovision.baselines A
INNER JOIN miovision.periods B USING (day_type)

WHERE A.time_bin <@ B.period_range
GROUP BY A.intersection_uid, A.classification_uid, A.leg, A.dir, B.period_id
ORDER BY A.intersection_uid, A.classification_uid, A.leg, A.dir, B.period_id