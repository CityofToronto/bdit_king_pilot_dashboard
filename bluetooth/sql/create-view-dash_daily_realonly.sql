CREATE OR REPLACE VIEW king_pilot.dash_daily_realonly AS
SELECT Z.street_name AS street, Z.direction, X.dt, X.day_type, X.category, X.period_name AS period, SUM(X.tt)/60.0 as tt
FROM

	(SELECT R.bt_id, S.dt, S.day_type, S.category, T.period_id, T.period_name, AVG(R.tt) AS tt
	FROM	(SELECT A.bt_id, 
			B.datetime_bin::date AS dt,
			(TIMESTAMP WITHOUT TIME ZONE 'epoch' +
				INTERVAL '1 second' * (floor((extract('epoch' from B.datetime_bin)) / 1800) * 1800))::time AS time_bin,
			SUM(B.tt*B.obs)/SUM(b.obs) AS tt,
			SUM(B.obs) AS obs

		FROM	
		(	SELECT
			OBS.analysis_id,
			TIMESTAMP WITHOUT TIME ZONE 'epoch' +
				INTERVAL '1 second' * (floor((extract('epoch' from OBS.measured_timestamp)-1) / 300) * 300) as datetime_bin,
			median(OBS.measured_time) AS tt,
			COUNT(OBS.user_id) AS obs


			FROM king_pilot.daily_raw_bt AS OBS
			WHERE OBS.outlier_level = 0 AND device_class = 1 AND OBS.measured_timestamp::date > (SELECT MAX(dt) FROM king_pilot.tt_30min)
			GROUP BY OBS.analysis_id, (floor((extract('epoch' from OBS.measured_timestamp)-1) / 300) * 300)
			ORDER BY OBS.analysis_id, (floor((extract('epoch' from OBS.measured_timestamp)-1) / 300) * 300) 
			) AS B

		INNER JOIN king_pilot.bt_segments_fake A USING (analysis_id)

		GROUP BY A.bt_id, B.datetime_bin::date, (TIMESTAMP WITHOUT TIME ZONE 'epoch' + INTERVAL '1 second' * (floor((extract('epoch' from B.datetime_bin)) / 1800) * 1800))::time
		ORDER BY A.bt_id, B.datetime_bin::date,  (TIMESTAMP WITHOUT TIME ZONE 'epoch' + INTERVAL '1 second' * (floor((extract('epoch' from B.datetime_bin)) / 1800) * 1800))::time) AS R
	INNER JOIN king_pilot.date_lookup S USING (dt)
	INNER JOIN king_pilot.periods T USING (day_type)
	WHERE R.time_bin <@ T.period_range
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