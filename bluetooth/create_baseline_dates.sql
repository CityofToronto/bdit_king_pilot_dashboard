create temporary table cuts(
	report_name varchar, cut_date date 
);

-- INSERT INTO cuts
-- 	VALUES
-- 	('DT-0037. Eastern_Richmond-WB_Broadview-to-Parliament', '2017-10-05'),
-- 	('DT-0037. Eastern_Richmond-WB_Broadview-to-Parliament', '2017-10-10'),
-- 	('DT-0037. Eastern_Richmond-WB_Broadview-to-Parliament', '2017-10-02'),
-- 	('DT-0033. Queen-WB_Spadina-to-Bathurst', '2017-10-02');
DROP TABLE baseline_dates;
create table baseline_dates as (
	SELECT DISTINCT aa.analysis_id, CASE WHEN EXTRACT(ISODOW FROM bt.datetime_bin) < 6 THEN 'weekday' ELSE 'weekend' END as daytype, bt.datetime_bin::date as date
	FROM dt_30min_agg bt
		INNER JOIN bluetooth.all_analyses aa USING (analysis_id)
		LEFT OUTER JOIN cuts ON (cuts.report_name = aa.report_name AND cuts.cut_date = bt.datetime_bin::date)
		LEFT OUTER JOIN ref.holiday hol ON (bt.datetime_bin::DATE = hol.dt)
	WHERE cuts.cut_date IS NULL AND
		bt.datetime_bin::date NOT BETWEEN '2017-10-15' AND '2017-10-29'
		AND hol.dt IS NULL);
		
		--use analysis_id
		--move to bt_analysis
SELECT * FROM baseline_dates
