INSERT INTO miovision.baseline_dates(intersection_uid, day_type, dt)
SELECT intersection_uid, 'Weekday' AS day_type, datetime_bin::date AS dt
FROM miovision.volumes_15min
WHERE EXTRACT(ISODOW FROM datetime_bin) < 6 AND datetime_bin::date <= '2017-11-11'
GROUP BY intersection_uid, datetime_bin::date
ORDER BY intersection_uid, datetime_bin::date;

DELETE FROM miovision.baseline_dates WHERE intersection_uid = 1 AND dt IN ('2017-10-11','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 2 AND dt IN ('2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 3 AND dt IN ('2017-10-13','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 4 AND dt IN ('2017-10-12','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 5 AND dt IN ('2017-10-12','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 6 AND dt IN ('2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 7 AND dt IN ('2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 8 AND dt IN ('2017-10-31','2017-11-03','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 9 AND dt IN ('2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 10 AND dt IN ('2017-10-03','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 11 AND dt IN ('2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 12 AND dt IN ('2017-11-06','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 13 AND dt IN ('2017-11-03','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 14 AND dt IN ('2017-10-31','2017-11-03','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 15 AND dt IN ('2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 16 AND dt IN ('2017-10-31','2017-11-03','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 17 AND dt IN ('2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 18 AND dt IN ('2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 19 AND dt IN ('2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 20 AND dt IN ('2017-10-04','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 21 AND dt IN ('2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 22 AND dt IN ('2017-10-11','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 23 AND dt IN ('2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 24 AND dt IN ('2017-10-13','2017-11-03','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 25 AND dt IN ('2017-10-31','2017-11-03','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 26 AND dt IN ('2017-10-13','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 27 AND dt IN ('2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 28 AND dt IN ('2017-10-13','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 29 AND dt IN ('2017-10-12','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 30 AND dt IN ('2017-10-31','2017-11-03','2017-11-07');
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 31 AND dt IN ('2017-10-13','2017-11-07');