DROP VIEW king_pilot.dash_baseline;

CREATE OR REPLACE VIEW king_pilot.dash_baseline AS 
 SELECT z.street_name AS street,
    z.direction,
    z.from_intersection,
    z.to_intersection,
    x.day_type,
    x.period_name AS period,
    '(' || to_char(lower(period_range), 'HH24:MM') || '-' || to_char(upper(period_range), 'HH24:MM') ||')' AS period_range,
    sum(x.tt) / 60.0 AS tt
   FROM ( SELECT a.bt_id,
            a.day_type,
            b.period_name,
            b.period_range,
            avg(a.tt) AS tt
           FROM king_pilot.baselines a
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

ALTER TABLE king_pilot.dash_baseline
  OWNER TO aharpal;
GRANT ALL ON TABLE king_pilot.dash_baseline TO aharpal;
GRANT SELECT ON TABLE king_pilot.dash_baseline TO public;
