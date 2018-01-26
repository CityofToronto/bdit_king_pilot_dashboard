DROP TABLE IF EXISTS veh_vol;
DROP TABLE IF EXISTS tod_vol;
DROP TABLE IF EXISTS aharpal.wellington_vol;

CREATE TEMPORARY TABLE veh_vol (
	intersection_uid integer,
	datetime_bin timestamp without time zone,
	dir text,
	leg text,
	total_volume numeric
	);

CREATE TEMPORARY TABLE tod_vol (
	intersection_uid integer,
	dow integer,
	time_bin time,
	count_type text,
	dir text,
	leg text,
	average_volume numeric,
	obs integer);

CREATE TABLE aharpal.wellington_vol (
	intersection_uid integer,
	dir text,
	leg text,
	time_bin time without time zone,
	baseline_vol numeric,
	pilot_vol numeric);
	
INSERT INTO veh_vol
SELECT	intersection_uid,
	datetime_bin,
	dir,
	leg,
	SUM(volume) AS total_volume
FROM 	miovision.volumes_15min
WHERE 	intersection_uid IN (8,31) AND classification_uid IN (1,4,5) AND dir = 'WB'
GROUP BY intersection_uid, datetime_bin, dir, leg
ORDER BY intersection_uid, datetime_bin, dir, leg;

INSERT INTO tod_vol
SELECT 	intersection_uid, 
	EXTRACT(isodow FROM datetime_bin) AS dow,
	datetime_bin::time AS time_bin,
	CASE WHEN datetime_bin <= '2017-11-11' THEN 'Baseline' ELSE 'Pilot' END AS count_type,
	dir, 
	leg,
	AVG(total_volume) AS average_volume,
	COUNT(*) AS obs
FROM 	veh_vol
GROUP BY intersection_uid, EXTRACT(isodow FROM datetime_bin), datetime_bin::time, CASE WHEN datetime_bin <= '2017-11-11' THEN 'Baseline' ELSE 'Pilot' END, dir, leg 
ORDER BY intersection_uid, CASE WHEN datetime_bin <= '2017-11-11' THEN 'Baseline' ELSE 'Pilot' END, EXTRACT(isodow FROM datetime_bin), datetime_bin::time, dir, leg;

INSERT INTO aharpal.wellington_vol
SELECT intersection_uid, dir, leg, time_bin, AVG(B.average_volume) AS baseline_vol, AVG(P.average_volume) AS pilot_vol
FROM 	(SELECT * FROM tod_vol WHERE count_type = 'Baseline') B
INNER JOIN (SELECT * FROM tod_vol WHERE count_type = 'Pilot') P USING (intersection_uid, dow, time_bin, dir, leg)
WHERE dow <= 5 AND time_bin >= '6:00' AND time_bin < '22:00'
GROUP BY intersection_uid, dir, leg, time_bin;

