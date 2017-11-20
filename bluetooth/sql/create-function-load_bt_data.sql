CREATE OR REPLACE FUNCTION king_pilot.load_bt_data() RETURNS integer AS $$

BEGIN
	-- TRUNCATE king_pilot.tt_30min
	TRUNCATE king_pilot.tt_30min;

	-- LOAD king_pilot.30min
	INSERT INTO king_pilot.tt_30min (bt_id, dt, time_bin, tt, obs)
	SELECT 	A.bt_id, 
		B.datetime_bin::date AS dt,
		(TIMESTAMP WITHOUT TIME ZONE 'epoch' +
			INTERVAL '1 second' * (floor((extract('epoch' from B.datetime_bin)) / 1800) * 1800))::time AS time_bin,
		SUM(B.tt*B.obs)/SUM(b.obs) AS tt,
		SUM(B.obs) AS obs
	FROM king_pilot.bt_segments A
	INNER JOIN bluetooth.aggr_5min B USING (analysis_id)
	WHERE NOT (A.bt_id = 33 AND B.datetime_bin::date = '2017-09-19' AND B.datetime_bin::time >= '19:00')
	GROUP BY A.bt_id, dt, time_bin;

	RETURN 1;
END
$$ LANGUAGE plpgsql;
GRANT EXECUTE ON FUNCTION king_pilot.load_bt_data() TO bt_insert_bot;
GRANT EXECUTE ON FUNCTION king_pilot.load_bt_data() TO rdumas;
 ALTER FUNCTION king_pilot.load_bt_data()
   OWNER TO bt_admins;