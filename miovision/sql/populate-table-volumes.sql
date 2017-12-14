TRUNCATE miovision.volumes;

INSERT INTO miovision.volumes (intersection_uid, datetime_bin, classification_uid, leg, movement_uid, volume)
SELECT B.intersection_uid, A.datetime_bin, C.classification_uid, A.entry_name as leg, D.movement_uid, A.volume
FROM miovision.raw_data A
INNER JOIN miovision.intersections B ON TRIM(substring(replace(A.study_name,'Adelaide/','Adelaide /') FROM '(?:(?!Oct|Nov).)*')) = B.intersection_name
INNER JOIN miovision.movements D USING (movement)
INNER JOIN miovision.classifications C USING (classification, location_only)
WHERE A.lat = B.lat AND A.lng = B.lng
ORDER BY A.datetime_bin, B.intersection_uid, C.classification_uid, A.entry_name, D.movement_uid;