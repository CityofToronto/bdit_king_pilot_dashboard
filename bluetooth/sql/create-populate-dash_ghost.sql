CREATE OR REPLACE VIEW king_pilot.dash_ghost AS 
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
                   FROM king_pilot.tt_30min a
                     JOIN king_pilot.date_lookup_ghost b USING (dt)
                     JOIN king_pilot.periods c USING (day_type)
                  WHERE a.time_bin <@ c.period_range
                  GROUP BY a.bt_id, b.dt, b.day_type, b.category, c.period_id, c.period_name
                  ORDER BY a.bt_id, b.dt, b.day_type, b.category, c.period_id) x
             JOIN king_pilot.bt_corridor_segments y USING (bt_id)
             JOIN king_pilot.bt_corridors z USING (corridor_id)
          WHERE (z.corridor_id <> ALL (ARRAY[6, 8, 9])) AND x.dt >= ('now'::text::date - '14 days'::interval)::date --limits to two weeks, excludes unnused segments
          GROUP BY z.corridor_id, z.street_name, z.direction, x.dt, x.day_type, x.category, x.period_name, x.period_id, z.segments
         HAVING count(x.*) = z.segments
          ORDER BY z.corridor_id, z.direction, x.period_id, x.day_type, x.dt) f
-- UNION ALL
--  SELECT dash_daily_real_ghost.street,
--     dash_daily_real_ghost.direction,
 --    dash_daily_real_ghost.dt,
--     dash_daily_real_ghost.day_type,
--     dash_daily_real_ghost.category,
--     dash_daily_real_ghost.period,
--     dash_daily_real_ghost.tt
--    FROM king_pilot.dash_daily_realonly
