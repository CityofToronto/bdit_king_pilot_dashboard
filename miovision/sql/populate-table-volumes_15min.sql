TRUNCATE miovision.volumes_15min;

INSERT INTO miovision.volumes_15min(intersection_uid, datetime_bin, classification_uid, leg, dir, volume)
SELECT 	A.intersection_uid,
	A.datetime_bin,
	A.classification_uid,
	B.leg_new as leg,
	B.dir,
	SUM(A.volume) AS volume

FROM miovision.volumes_15min_tmc A
INNER JOIN miovision.movement_map B ON B.leg_old = A.leg AND B.movement_uid = A.movement_uid

GROUP BY A.intersection_uid, A.datetime_bin, A.classification_uid, B.leg_new, B.dir
ORDER BY A.datetime_bin, A.intersection_uid, A.classification_uid, B.leg_new, B.dir