CREATE MATERIALIZED VIEW miovision.peds_15min AS
SELECT
intersection_uid,
intersection_name,
dt,
datetime_bin,
SUM(volume) AS total_volume

FROM
(SELECT days AS dt,
	days + CASE WHEN EXTRACT(isodow FROM days) IN (1,2,3,4,5) THEN INTERVAL '6 hours' ELSE '9 hours' END AS start_bin,
	days + CASE WHEN EXTRACT(isodow FROM days) IN (1,2,3,7) THEN INTERVAL '20 hours' ELSE '28 hours' END AS end_bin
FROM 	generate_series('2017-10-01'::timestamp without time zone, '2017-12-31'::timestamp without time zone, '1 day') AS days
) A
INNER JOIN miovision.volumes_15min B ON B.datetime_bin >= A.start_bin AND B.datetime_bin < A.end_bin
INNER JOIN miovision.peds_daily C USING (dt, intersection_uid)
INNER JOIN miovision.intersections USING (intersection_uid, intersection_name)

WHERE 	classification_uid = 6

GROUP BY intersection_uid, intersection_name, dt, datetime_bin