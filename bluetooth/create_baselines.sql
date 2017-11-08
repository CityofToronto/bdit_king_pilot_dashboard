DROP TABLE baselines;
create table baselines as (
SELECT datetime_bin::time as time, 
    avg(bt.travel_time) as avg_tt,
    bt.analysis_id,
    dates.daytype

FROM dt_30min_agg bt
    INNER JOIN baseline_dates dates ON (dates.analysis_id = bt.analysis_id AND dates.date = bt.datetime_bin::date) 

GROUP BY bt.analysis_id, 
    datetime_bin::time, 
    dates.daytype);
    
 SELECT * FROM baselines