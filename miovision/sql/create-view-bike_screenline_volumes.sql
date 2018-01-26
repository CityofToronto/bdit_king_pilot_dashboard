CREATE OR REPLACE VIEW miovision.bike_screenline_volumes AS
SELECT	intersection_uid,
	CASE WHEN intersection_uid = 1 AND datetime_bin >= '2017-12-11' AND datetime_bin < '2017-12-14' THEN datetime_bin - INTERVAL '7 days' ELSE datetime_bin END AS datetime_bin,
	dir,
	SUM(volume) AS total_volume
FROM 	miovision.volumes_15min
INNER JOIN miovision.intersections USING (intersection_uid)
WHERE 	classification_uid IN (2,7) 
	AND ((street_cross = 'Spadina' AND leg IN ('E','N','S')) OR (street_cross = 'Jarvis' AND leg IN ('W','N','S')))
	AND dir IN ('EB','WB')
GROUP BY intersection_uid, CASE WHEN intersection_uid = 1 AND datetime_bin >= '2017-12-11' AND datetime_bin < '2017-12-14' THEN datetime_bin - INTERVAL '7 days' ELSE datetime_bin END, dir
ORDER BY intersection_uid, CASE WHEN intersection_uid = 1 AND datetime_bin >= '2017-12-11' AND datetime_bin < '2017-12-14' THEN datetime_bin - INTERVAL '7 days' ELSE datetime_bin END, dir;