INSERT INTO miovision.baseline_dates(intersection_uid, day_type, dt)
SELECT intersection_uid, 'Weekday' AS day_type, datetime_bin::date AS dt
FROM miovision.volumes_15min
WHERE EXTRACT(ISODOW FROM datetime_bin) < 6
GROUP BY intersection_uid, datetime_bin::date
ORDER BY intersection_uid, datetime_bin::date;