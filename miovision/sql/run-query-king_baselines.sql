DROP TABLE IF EXISTS aharpal.king_baselines;

CREATE TABLE aharpal.king_baselines AS 
WITH lng AS (
SELECT intersection_name, dir, dow, time_bin, average_volume
FROM miovision.volumes_by_dow
INNER JOIN miovision.intersections USING (intersection_uid)
WHERE class_group = 'Vehicles' AND intersection_uid IN (10,17,20) AND dow <= 5 AND ((dir = 'EB' AND leg = 'W') OR (dir = 'WB' AND leg = 'E')) AND count_type = 'Baseline'
ORDER BY intersection_uid, dir, dow, time_bin)

/*
SELECT 	intersection_name, 
	dir, 
	time_bin, 
	SUM(CASE WHEN dow = 1 THEN average_volume ELSE 0 END) AS monday,
	SUM(CASE WHEN dow = 2 THEN average_volume ELSE 0 END) AS tuesday,
	SUM(CASE WHEN dow = 3 THEN average_volume ELSE 0 END) AS wednesday,
	SUM(CASE WHEN dow = 4 THEN average_volume ELSE 0 END) AS thursday,
	SUM(CASE WHEN dow = 5 THEN average_volume ELSE 0 END) AS friday
FROM	lng
GROUP BY intersection_name, dir, time_bin
ORDER BY intersection_name, dir, time_bin

*/

/*
SELECT 	intersection_name, 
	dow,
	time_bin, 
	SUM(CASE WHEN dir = 'EB' THEN average_volume ELSE 0 END) AS eastbound,
	SUM(CASE WHEN dir = 'WB' THEN average_volume ELSE 0 END) AS westbound
FROM	lng
GROUP BY intersection_name, dow, time_bin
ORDER BY intersection_name, dow, time_bin
*/

SELECT 	intersection_name,
	dir,
	time_bin, 
	AVG(average_volume) AS weekday_average
FROM	lng
GROUP BY intersection_name, dir, time_bin
ORDER BY intersection_name, dir, time_bin