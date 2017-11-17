CREATE VIEW king_pilot.real_tt_30min AS
SELECT A.bt_id, 
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
ORDER BY A.bt_id, B.datetime_bin::date,  (TIMESTAMP WITHOUT TIME ZONE 'epoch' + INTERVAL '1 second' * (floor((extract('epoch' from B.datetime_bin)) / 1800) * 1800))::time;

ALTER TABLE king_pilot.real_tt_30min
  OWNER TO aharpal;
GRANT ALL ON TABLE king_pilot.real_tt_30min TO aharpal;
GRANT SELECT ON TABLE king_pilot.real_tt_30min TO public;
