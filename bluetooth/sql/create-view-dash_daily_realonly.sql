CREATE OR REPLACE VIEW king_pilot.dash_daily_realonly AS
SELECT Z.street_name AS street, Z.direction, X.dt, X.day_type, X.category, X.period_name AS period, SUM(X.tt)/60.0 as tt
FROM

	(SELECT R.bt_id, S.dt, S.day_type, S.category, T.period_id, T.period_name, AVG(R.tt) AS tt
	FROM king_pilot.real_tt_30min AS R
	INNER JOIN king_pilot.date_lookup S USING (dt)
	INNER JOIN king_pilot.periods T USING (day_type)
	WHERE 	R.time_bin <@ T.period_range 
		AND (
			((upper(T.period_range) - INTERVAL '30 minutes') <= (SELECT MAX(time_bin) FROM king_pilot.real_tt_30min))
			OR
			((SELECT MAX(dt) FROM king_pilot.real_tt_30min) > S.dt)
		)
	GROUP BY R.bt_id, S.dt, S.day_type, S.category, T.period_id, T.period_name
	ORDER BY R.bt_id, S.dt, S.day_type, S.category, T.period_id) X
	
INNER JOIN king_pilot.bt_corridor_segments Y USING (bt_id)
INNER JOIN king_pilot.bt_corridors Z USING (corridor_id)

WHERE Z.corridor_id NOT IN (6,8,9)
GROUP BY Z.corridor_id, Z.street_name, Z.direction, X.dt, X.day_type, X.category, X.period_name, X.period_id, Z.segments
HAVING COUNT(X.*) = Z.segments
ORDER BY Z.corridor_id, Z.direction, X.period_id, X.day_type, X.dt;

ALTER TABLE king_pilot.dash_daily_realonly
  OWNER TO aharpal;
GRANT ALL ON TABLE king_pilot.dash_daily_realonly TO aharpal;
GRANT SELECT ON TABLE king_pilot.dash_daily_realonly TO public;