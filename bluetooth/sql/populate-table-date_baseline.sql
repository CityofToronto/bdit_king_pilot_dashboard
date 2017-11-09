INSERT INTO king_pilot.date_baseline
SELECT B.bt_id, A.daytype as day_type, A.date as dt
FROM rrodger.baseline_dates A
INNER JOIN king_pilot.bt_segments B USING (analysis_id)
ORDER BY B.bt_id, A.date;

UPDATE king_pilot.date_baseline
SET day_type = 'Weekday'
WHERE day_type = 'weekday';

UPDATE king_pilot.date_baseline
SET day_type = 'Weekend'
WHERE day_type = 'weekend';