INSERT INTO miovision.baseline_dates(intersection_uid, day_type, dt)
SELECT intersection_uid, 'Weekday' AS day_type, datetime_bin::date AS dt
FROM miovision.volumes_15min
WHERE EXTRACT(ISODOW FROM datetime_bin) < 6 AND datetime_bin::date <= '2017-11-11'
GROUP BY intersection_uid, datetime_bin::date
ORDER BY intersection_uid, datetime_bin::date;

DELETE FROM miovision.baseline_dates WHERE intersection_uid = 1 AND dt = '2017-10-11';
DELETE FROM miovision.baseline_dates WHERE intersection_uid = 1 AND dt = '2017-11-07';