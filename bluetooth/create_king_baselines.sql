DROP TABLE cuts;
create temporary table cuts(
	report_name varchar, cut_date date 
);

-- INSERT INTO cuts
-- 	VALUES
-- 	('DT-0037. Eastern_Richmond-WB_Broadview-to-Parliament', '2017-10-05'),
-- 	('DT-0037. Eastern_Richmond-WB_Broadview-to-Parliament', '2017-10-10'),
-- 	('DT-0037. Eastern_Richmond-WB_Broadview-to-Parliament', '2017-10-02'),
-- 	('DT-0033. Queen-WB_Spadina-to-Bathurst', '2017-10-02');
--DROP TABLE baseline_dates;
DROP TABLE king_pilot_baselines;
CREATE TABLE king_pilot_baselines as (
	WITH baseline_dates as (

		WITH dt_30min_agg as (
			SELECT 
				bt.analysis_id,
				TIMESTAMP WITHOUT TIME ZONE 'epoch' +
					INTERVAL '1 second' * (floor((extract('epoch' from bt.datetime_bin)-1) / 1800) * 1800) as datetime_bin,
				sum(bt.tt*bt.obs)/sum(bt.obs) AS travel_time,
				sum(bt.obs) AS obs
			FROM bluetooth.all_analyses aa
				INNER JOIN bluetooth.aggr_5min bt USING (analysis_id)
			WHERE left(aa.report_name, 4) = 'DT-0'
				AND datetime_bin < '2017-11-12 00:00:00'
			GROUP BY bt.analysis_id, (floor((extract('epoch' from bt.datetime_bin)-1) / 1800) * 1800)
			ORDER BY bt.analysis_id, (floor((extract('epoch' from bt.datetime_bin)-1) / 1800) * 1800)
			)
		SELECT DISTINCT aa.analysis_id, CASE WHEN EXTRACT(ISODOW FROM bt.datetime_bin) < 6 THEN 'weekday' ELSE 'weekend' END as daytype, bt.datetime_bin::date as date
		FROM dt_30min_agg bt
			INNER JOIN bluetooth.all_analyses aa USING (analysis_id)
			LEFT OUTER JOIN cuts ON (cuts.report_name = aa.report_name AND cuts.cut_date = bt.datetime_bin::date)
			LEFT OUTER JOIN ref.holiday hol ON (bt.datetime_bin::DATE = hol.dt)
		WHERE cuts.cut_date IS NULL AND
			bt.datetime_bin::date NOT BETWEEN '2017-10-15' AND '2017-10-29'
			AND hol.dt IS NULL
	)
	SELECT datetime_bin::time as time, 
	    avg(bt.travel_time) as avg_tt,
	    bt.analysis_id as analysis_id,
	    dates.daytype as daytype

	FROM dt_30min_agg bt
	    INNER JOIN baseline_dates dates ON (dates.analysis_id = bt.analysis_id AND dates.date = bt.datetime_bin::date) 

	GROUP BY bt.analysis_id, 
	    datetime_bin::time, 
	    dates.daytype
)
