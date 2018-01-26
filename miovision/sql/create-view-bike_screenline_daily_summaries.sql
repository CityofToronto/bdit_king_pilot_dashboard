DROP VIEW IF EXISTS miovision.bike_screenline_daily_summaries;
CREATE VIEW miovision.bike_screenline_daily_summaries AS
SELECT street_cross, dir, dt, SUM(total_volume) AS daily_volume
FROM miovision.bike_screenline_volumes_adj
GROUP BY street_cross, dir, dt
ORDER BY street_cross, dir, dt;