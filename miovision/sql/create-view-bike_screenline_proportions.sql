DROP VIEW IF EXISTS miovision.bike_screenline_proportions;
CREATE VIEW miovision.bike_screenline_proportions AS 

WITH total_screenlines AS (
	SELECT street_cross, dir, CASE WHEN dt <= '2017-11-11' THEN 'Baseline' ELSE 'Pilot' END AS category, SUM(total_volume) AS screenline_volume
	FROM miovision.bike_screenline_volumes_adj
	GROUP BY street_cross, dir, CASE WHEN dt <= '2017-11-11' THEN 'Baseline' ELSE 'Pilot' END
	ORDER BY street_cross, dir, CASE WHEN dt <= '2017-11-11' THEN 'Baseline' ELSE 'Pilot' END
	),
total_intersections AS (
	SELECT street_cross, street_main, dir, CASE WHEN dt <= '2017-11-11' THEN 'Baseline' ELSE 'Pilot' END AS category, SUM(total_volume) AS street_volume
	FROM miovision.bike_screenline_volumes_adj A
	GROUP BY street_cross, street_main, dir, CASE WHEN dt <= '2017-11-11' THEN 'Baseline' ELSE 'Pilot' END
	ORDER BY street_cross, street_main, dir, CASE WHEN dt <= '2017-11-11' THEN 'Baseline' ELSE 'Pilot' END
)
SELECT street_cross, street_main, dir, category, street_volume/screenline_volume as proportion
FROM total_screenlines
INNER JOIN total_intersections USING (street_cross, dir, category);