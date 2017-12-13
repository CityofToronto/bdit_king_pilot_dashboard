-- EB segments
select bt_id, period_name, round(avg(bl)/60,2) bl_min, round(avg(bl),1) bl_sec
from 
(
	-- avg tt per time_bin for corridor
	select bt_id, period_name, sum(sum(avgtt)) over (partition by bt_id, time_bin) as bl
	from
	(
		-- avg tt per time_bin per bt_id
		select bt_id, period_name, time_bin, avg(tt) as avgtt
		from king_pilot.ttc_tt_30min t
		inner join king_pilot.periods on (time_bin::time <@ period_range
							and day_type = (case 
								when extract(dow from dt) = 0 then 'Weekend'
								when extract(dow from dt) = 1 then 'Weekday'
								when extract(dow from dt) = 2 then 'Weekday'
								when extract(dow from dt) = 3 then 'Weekday'
								when extract(dow from dt) = 4 then 'Weekday'
								when extract(dow from dt) = 5 then 'Weekday'
								when extract(dow from dt) = 6 then 'Weekend' end))
		where bt_id >= 52 and bt_id <= 55 -- EB KING Bathurst to Jarvis
		and dt >= '2017-09-24' and dt <= '2017-10-14'
		and period_id in (1, 3) -- weekday AM Peak and PM Peak
		group by bt_id, period_name, time_bin
		order by bt_id, time_bin
	)
	as bt_avgtt
	group by period_name, bt_id, time_bin
	order by bt_id, time_bin
)
as corridor_avgtt
group by bt_id, period_name
order by period_name, bt_id






-- WB segments
select bt_id, period_name, round(avg(bl)/60,2) bl_min, round(avg(bl),1) bl_sec
from 
(
	-- avg tt per time_bin for corridor
	select bt_id, period_name, sum(sum(avgtt)) over (partition by bt_id, time_bin) as bl
	from
	(
		-- avg tt per time_bin per bt_id
		select bt_id, period_name, time_bin, avg(tt) as avgtt
		from king_pilot.ttc_tt_30min t
		inner join king_pilot.periods on (time_bin::time <@ period_range
							and day_type = (case 
								when extract(dow from dt) = 0 then 'Weekend'
								when extract(dow from dt) = 1 then 'Weekday'
								when extract(dow from dt) = 2 then 'Weekday'
								when extract(dow from dt) = 3 then 'Weekday'
								when extract(dow from dt) = 4 then 'Weekday'
								when extract(dow from dt) = 5 then 'Weekday'
								when extract(dow from dt) = 6 then 'Weekend' end))
		where bt_id >= 60 and bt_id <= 63 -- WB KING Jarvis to Bathurst
		and dt >= '2017-09-24' and dt <= '2017-10-14'
		and period_id in (1, 3) -- weekday AM Peak and PM Peak
		group by bt_id, period_name, time_bin
		order by bt_id, time_bin
	)
	as bt_avgtt
	group by period_name, bt_id, time_bin
	order by bt_id, time_bin
)
as corridor_avgtt
group by bt_id, period_name
order by period_name, bt_id
