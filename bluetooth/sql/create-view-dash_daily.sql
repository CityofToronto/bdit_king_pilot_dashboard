DROP VIEW IF EXISTS king_pilot.dash_daily;

CREATE VIEW king_pilot.dash_daily AS
SELECT Z.street_name AS street, Z.direction, X.dt, X.day_type, X.period_name AS period, SUM(X.tt)/60.0 as tt
FROM
(SELECT A.bt_id, B.dt, B.day_type, C.period_id, C.period_name, AVG(A.tt) AS tt
FROM king_pilot.tt_30min A
INNER JOIN king_pilot.date_lookup B USING (dt)
INNER JOIN king_pilot.periods C USING (day_type)
WHERE A.time_bin <@ C.period_range
GROUP BY A.bt_id, B.dt, B.day_type, C.period_id, C.period_name
ORDER BY A.bt_id, B.dt, B.day_type, C.period_id) X

INNER JOIN king_pilot.bt_corridor_segments Y USING (bt_id)
INNER JOIN king_pilot.bt_corridors Z USING (corridor_id)
WHERE Z.corridor_id NOT IN (6)
GROUP BY Z.corridor_id, Z.street_name, Z.direction, X.dt, X.day_type, X.period_name, X.period_id, Z.segments
HAVING COUNT(X.*) = Z.segments
ORDER BY Z.corridor_id, Z.direction, X.period_id, X.day_type, X.dt;