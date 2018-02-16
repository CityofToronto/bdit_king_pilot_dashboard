CREATE OR REPLACE VIEW king_pilot.tt_30min_cars_only AS 
	SELECT 	A.bt_id, 
		B.datetime_bin::date AS dt,
		(TIMESTAMP WITHOUT TIME ZONE 'epoch' +
			INTERVAL '1 second' * (floor((extract('epoch' from B.datetime_bin)) / 1800) * 1800))::time AS time_bin,
		SUM(B.tt*B.obs)/SUM(b.obs) AS tt,
		SUM(B.obs) AS obs
	FROM king_pilot.bt_segments A
	INNER JOIN bluetooth.aggr_5min_cars_only B USING (analysis_id)
	WHERE NOT (A.bt_id = 33 AND B.datetime_bin::date = '2017-09-19' AND B.datetime_bin::time >= '19:00')
	GROUP BY A.bt_id, dt, time_bin;
GRANT SELECT ON TABLE king_pilot.tt_30min_cars_only TO bdit_humans;

CREATE OR REPLACE VIEW king_pilot.dash_daily_cars_only AS 
 SELECT f.street,
    f.direction,
    f.dt,
    f.day_type,
    f.category,
    f.period,
    f.tt
   FROM ( SELECT z.street_name AS street,
            z.direction,
            x.dt,
            x.day_type,
            x.category,
            x.period_name AS period,
            sum(x.tt) / 60.0 AS tt
           FROM ( SELECT a.bt_id,
                    b.dt,
                    b.day_type,
                    b.category,
                    c.period_id,
                    c.period_name,
                    avg(a.tt) AS tt
                   FROM king_pilot.tt_30min_cars_only a
                     JOIN king_pilot.date_lookup b USING (dt)
                     JOIN king_pilot.periods c USING (day_type)
                  WHERE a.time_bin <@ c.period_range
                  GROUP BY a.bt_id, b.dt, b.day_type, b.category, c.period_id, c.period_name
                  ORDER BY a.bt_id, b.dt, b.day_type, b.category, c.period_id) x
             JOIN king_pilot.bt_corridor_segments y USING (bt_id)
             JOIN king_pilot.bt_corridors z USING (corridor_id)
          WHERE z.corridor_id <> ALL (ARRAY[6, 8, 9])
          GROUP BY z.corridor_id, z.street_name, z.direction, x.dt, x.day_type, x.category, x.period_name, x.period_id, z.segments
         HAVING count(x.*) = z.segments
          ORDER BY z.corridor_id, z.direction, x.period_id, x.day_type, x.dt) f;
GRANT SELECT ON TABLE king_pilot.dash_daily_cars_only TO bdit_humans;

CREATE OR REPLACE VIEW king_pilot.baselines_cars_only AS

SELECT 	A.bt_id, 
	B.day_type,
	A.time_bin,
	AVG(A.tt) AS tt,
	SUM(A.obs) AS obs

FROM king_pilot.tt_30min A
INNER JOIN king_pilot.date_baseline B USING (bt_id,dt)
GROUP BY A.bt_id, B.day_type, A.time_bin;
GRANT SELECT ON TABLE king_pilot.baselines_cars_only TO bdit_humans;

CREATE OR REPLACE VIEW king_pilot.dash_baseline_cars_only AS 
 SELECT z.street_name AS street,
    z.direction,
    z.from_intersection,
    z.to_intersection,
    x.day_type,
    x.period_name AS period,
    ((('('::text || to_char(lower(x.period_range)::interval, 'HH24:MM'::text)) || '-'::text) || to_char(upper(x.period_range)::interval, 'HH24:MM'::text)) || ')'::text AS period_range,
    sum(x.tt) / 60.0 AS tt
   FROM ( SELECT a.bt_id,
            a.day_type,
            b.period_name,
            b.period_range,
            avg(a.tt) AS tt
           FROM king_pilot.baselines_cars_only a
             JOIN king_pilot.periods b USING (day_type)
             JOIN king_pilot.bt_segments c USING (bt_id)
          WHERE a.time_bin <@ b.period_range
          GROUP BY a.bt_id, a.day_type, b.period_name, b.period_range) x
     JOIN king_pilot.bt_corridor_segments y USING (bt_id)
     JOIN king_pilot.bt_corridors z USING (corridor_id)
  WHERE z.corridor_id <> ALL (ARRAY[6, 8, 9])
  GROUP BY z.corridor_id, z.corridor_name, x.day_type, x.period_name, x.period_range, z.segments, z.street_name, z.direction, z.from_intersection, z.to_intersection
 HAVING count(x.*) = z.segments
  ORDER BY z.corridor_id, x.day_type, x.period_range;

ALTER TABLE king_pilot.dash_baseline_cars_only
  OWNER TO rdumas;
GRANT ALL ON TABLE king_pilot.dash_baseline_cars_only TO rds_superuser WITH GRANT OPTION;
GRANT ALL ON TABLE king_pilot.dash_baseline_cars_only TO aharpal;
GRANT SELECT, UPDATE, INSERT, REFERENCES, TRIGGER ON TABLE king_pilot.dash_baseline_cars_only TO bdit_humans WITH GRANT OPTION;
GRANT ALL ON TABLE king_pilot.dash_baseline_cars_only TO aharpal;
GRANT SELECT ON TABLE king_pilot.dash_baseline_cars_only TO public;
GRANT SELECT ON TABLE king_pilot.dash_baseline_cars_only TO public;


-- WITH prev_aggr AS( SELECT street, direction, day_type, period, avg(tt) as prev_mean
-- FROM king_pilot.dash_daily_dev
-- where category = 'Pilot'
-- GROUP BY street, direction, day_type, period)
-- , cars_only_aggr AS(SELECT street, direction, day_type, period, avg(tt) as new_mean
-- FROM king_pilot.dash_daily_nov_cars_only
-- where category = 'Pilot'
-- GROUP BY street, direction, day_type, period
-- )
-- SELECT street, direction, day_type, period, prev_mean - new_mean as "Travel Time Difference"
-- 
-- from cars_only_aggr
-- NATURAL JOIN prev_aggr
