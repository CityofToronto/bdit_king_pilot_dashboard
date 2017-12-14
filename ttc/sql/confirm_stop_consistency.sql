SELECT count(*)
FROM ttc.trip_stops
WHERE stop_uid IN (7,76,8,77)
GROUP BY trip_uid;
--HAVING count(*) <> 2;
--every trip is logged at two stops
SELECT stop_uid
FROM (SELECT pattern_name
	FROM (SELECT trip_uid
		FROM ttc.trip_stops
			LEFT OUTER JOIN ttc.trips trips USING (trip_uid)
		WHERE line_number IN (504, 514)
		GROUP BY trip_uid
		HAVING count(trip_uid) FILTER (WHERE stop_uid IN (7,8,76,77)) < 2) as not_stopped_trip -- There are 1379 out of 15060 trips that don't touch the Bathurst and jarvis stops
		INNER JOIN ttc.trips USING (trip_uid) 
	GROUP BY line_number, line_name, pattern_name, direction) as not_stopped_pattern -- These have pattern_names BRBS, RQDW, BSBR, and DWRQ
	LEFT OUTER JOIN ttc.trips USING (pattern_name)
	LEFT OUTER JOIN ttc.trip_stops USING (trip_uid)
--WHERE stop_uid IN (7,8,76,77) -- The patterns that the trips that didn't visit Bathurst and Jarvis belonged to, never have trips that visit Bathurst and Jarvis.
GROUP BY stop_uid -- From this we can conclude that all streetcars visiting both Bathurst and Jarvis are accounted for
--The only routes that don't 