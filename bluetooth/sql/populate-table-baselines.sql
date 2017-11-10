TRUNCATE king_pilot.baselines;

INSERT INTO king_pilot.baselines

SELECT 	A.bt_id, 
	B.day_type,
	A.time_bin,
	AVG(A.tt) AS tt,
	SUM(A.obs) AS obs

FROM king_pilot.tt_30min A
INNER JOIN king_pilot.date_baseline B USING (bt_id,dt)

GROUP BY A.bt_id, B.day_type, A.time_bin
ORDER BY A.bt_id, B.day_type, A.time_bin