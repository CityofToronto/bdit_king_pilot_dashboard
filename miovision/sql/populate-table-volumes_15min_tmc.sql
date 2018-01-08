TRUNCATE miovision.volumes_15min_tmc;

INSERT INTO miovision.volumes_15min_tmc(intersection_uid, datetime_bin, classification_uid, leg, movement_uid, volume)
SELECT 	A.intersection_uid,
	TIMESTAMP WITHOUT TIME ZONE 'epoch' + INTERVAL '1 second' * (floor((extract('epoch' from A.datetime_bin)) / 900) * 900) AS datetime_bin,
	A.classification_uid,
	A.leg,
	A.movement_uid,
	SUM(A.volume) AS volume

FROM miovision.volumes A

GROUP BY A.intersection_uid, TIMESTAMP WITHOUT TIME ZONE 'epoch' + INTERVAL '1 second' * (floor((extract('epoch' from A.datetime_bin)) / 900) * 900), A.classification_uid, A.leg, A.movement_uid;