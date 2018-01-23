DROP VIEW IF EXISTS miovision.volumes_monthly;
CREATE MATERIALIZED VIEW miovision.volumes_monthly AS

SELECT date_trunc('month', A.datetime_bin) AS month_bin, B.day_type, A.intersection_uid, A.classification_uid, A.datetime_bin::time without time zone as time_bin, A.leg, A.dir, AVG(A.volume*1.0) as volume
FROM miovision.volumes_15min A
INNER JOIN king_pilot.date_lookup B ON B.dt = A.datetime_bin::date
WHERE A.datetime_bin::date >= '2017-12-01'
GROUP BY date_trunc('month', A.datetime_bin), B.day_type, A.intersection_uid, A.classification_uid, A.datetime_bin::time without time zone, A.leg, A.dir
ORDER BY date_trunc('month', A.datetime_bin), A.intersection_uid, A.classification_uid, A.leg, A.dir, A.datetime_bin::time without time zone, day_type;