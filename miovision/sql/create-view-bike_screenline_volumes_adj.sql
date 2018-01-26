DROP VIEW IF EXISTS miovision.bike_screenline_volumes_adj;
CREATE VIEW miovision.bike_screenline_volumes_adj AS 
	WITH valid_dates AS (
		WITH valid_bins AS (
			SELECT street_cross, datetime_bin, dir
			FROM miovision.bike_screenline_volumes
			INNER JOIN miovision.intersections USING (intersection_uid)
			GROUP BY street_cross, datetime_bin, dir
			HAVING COUNT(*) = 5
			ORDER BY street_cross, datetime_bin, dir
			)
		

		SELECT street_cross, datetime_bin::date AS dt, dir, COUNT(*)
		FROM miovision.bike_screenline_volumes
		INNER JOIN miovision.intersections USING (intersection_uid)
		INNER JOIN valid_bins USING (street_cross, datetime_bin, dir)
		WHERE datetime_bin::time >= '06:00' AND datetime_bin::time < '20:00' AND EXTRACT(isodow FROM datetime_bin) <= 5
		GROUP BY street_cross, datetime_bin::date, dir
		HAVING COUNT(*) >= 200
		)
	
SELECT street_cross, street_main, dt, tm, A.dir, COALESCE(D.total_volume, AVG(E.total_volume)) AS total_volume
FROM valid_dates A
INNER JOIN miovision.intersections B USING (street_cross)
CROSS JOIN
	(	SELECT x::time AS tm
		FROM generate_series('2000-01-01 6:00'::timestamp, '2000-01-01 19:45', '15 minutes'::interval) AS X
	) C
LEFT JOIN miovision.bike_screenline_volumes D ON D.intersection_uid = B.intersection_uid AND D.dir = A.dir AND D.datetime_bin::date = A.dt AND D.datetime_bin::time = C.tm
INNER JOIN miovision.bike_screenline_volumes E ON B.intersection_uid = E.intersection_uid AND E.dir = A.dir AND C.tm = E.datetime_bin::time 
WHERE EXTRACT(isodow FROM E.datetime_bin) <= 5 AND E.datetime_bin::date >= (A.dt - INTERVAL '1 day') AND E.datetime_bin::date <= (A.dt + INTERVAL '1 day')
GROUP BY street_cross, street_main, dt, tm, A.dir, D.total_volume
ORDER BY street_cross, street_main, dt, tm, A.dir