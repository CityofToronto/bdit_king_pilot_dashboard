DROP MATERIALIZED VIEW miovision.peds_daily;

CREATE MATERIALIZED VIEW miovision.peds_daily AS
SELECT
intersection_uid,
intersection_name,
dt,
start_bin,
end_bin,
SUM(volume) AS total_volume

FROM
(SELECT days AS dt,
	days + CASE WHEN EXTRACT(isodow FROM days) IN (1,2,3,4,5) THEN INTERVAL '6 hours' ELSE '9 hours' END AS start_bin,
	days + CASE WHEN EXTRACT(isodow FROM days) IN (1,2,3,7) THEN INTERVAL '20 hours' ELSE '28 hours' END AS end_bin
FROM 	generate_series('2017-10-01'::timestamp without time zone, '2017-12-31'::timestamp without time zone, '1 day') AS days
) A
INNER JOIN miovision.volumes_15min B ON B.datetime_bin >= A.start_bin AND B.datetime_bin < A.end_bin
INNER JOIN miovision.intersections USING (intersection_uid)

WHERE 	intersection_uid IN (1,2,3,4,5,6,7,8,9,10,12,15,17,18,20,21,22,23,24,25,26,27,28,29,31) 
	AND classification_uid = 6

GROUP BY intersection_uid, intersection_name, dt, start_bin, end_bin
HAVING 	MIN(datetime_bin) <= (start_bin + INTERVAL '45 minutes')
	AND MAX(datetime_bin) >= (end_bin - INTERVAL '60 minutes')
