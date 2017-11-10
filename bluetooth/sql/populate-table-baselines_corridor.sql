SELECT Z.corridor_name, X.day_type, X.period_name, SUM(X.tt) AS tt
FROM
( 	SELECT A.bt_id, A.day_type, B.period_name, AVG(A.tt) AS tt
	FROM king_pilot.baselines A
	INNER JOIN king_pilot.periods B USING (day_type)
	INNER JOIN king_pilot.bt_segments C USING (bt_id)
	WHERE A.time_bin <@ B.period_range
	GROUP BY A.bt_id, A.day_type, B.period_name
	) AS X
INNER JOIN king_pilot.bt_corridor_segments Y USING (bt_id)
INNER JOIN king_pilot.bt_corridors Z USING (corridor_id)
GROUP BY Z.corridor_id, Z.corridor_name, X.day_type, X.period_name
ORDER BY Z.corridor_id