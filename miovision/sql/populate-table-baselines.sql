TRUNCATE TABLE miovision.baselines;

INSERT INTO miovision.baselines (intersection_uid, classification_uid, day_type, time_bin, leg, dir, volume)
SELECT A.intersection_uid, A.classification_uid, 'Weekday' as day_type, A.datetime_bin::time without time zone as time_bin, A.leg, A.dir, AVG(A.volume*1.0) as volume
FROM miovision.volumes_15min A
INNER JOIN miovision.baseline_dates B ON A.datetime_bin::date = B.dt
GROUP BY A.intersection_uid, A.classification_uid, A.datetime_bin::time without time zone, A.leg, A.dir
ORDER BY A.intersection_uid, A.classification_uid, A.leg, A.dir, A.datetime_bin::time without time zone;