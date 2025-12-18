-- Chart 1: Spot Allocation - Monthly by Tenure (All Fitness, >24mo, <=24mo)
-- Outputs final chart-ready values directly from SQL

with vids as 
(
    select sv.account_classification, pd.*
    from cp_bi_derived.datapipeline.partner_details pd
    left join cp_bi_derived.datapipeline.salesforce_venues sv on pd.venue_id = sv.venue_id
    where pd.venue_type = 'Fitness'
    and estimated_launch_date is not null
    -- NO VVM filter - this is for "All Fitness"
),
avg_spot_alloc_per_venue_per_month as 
(
    select s.venue_id, account_classification,
            date_trunc('month', s.start_date) as month_date,
            (s.start_date - v.estimated_launch_date) as days_tenure,
            count(distinct s.schedule_id) as bookable_scheds_per_venue_per_month,
            sum(case when is_bookable = 'false' then 0
                   when is_bookable = 'true' and classpass_spots < 
                    (max_capacity - total_booked + classpass_spots_taken) THEN classpass_spots
                   else (max_capacity - total_booked + classpass_spots_taken)
                   end) as cp_alloc_adjusted
    from vids v
    join cp_bi_derived.datapipeline.sched_schedules s on s.venue_id = v.venue_id
    and s.start_date >= '2024-12-01' and s.start_date < '2025-12-01'
    and unbookable_reason is null
    and s.class_id not in (select distinct class_id from cp_bi_derived.datapipeline.ineligible_classes)
    group by 1, 2, 3, 4
)
select 
    month_date,
    -- All Fitness (simple average - matches validated query)
    avg(cp_alloc_adjusted * 1.0 / bookable_scheds_per_venue_per_month) as all_fitness,
    -- Long Tenure (>24mo = >730 days) - simple average
    avg(case when days_tenure > 730 then cp_alloc_adjusted * 1.0 / bookable_scheds_per_venue_per_month end) as long_tenure_gt24mo,
    -- Short Tenure (<=24mo = <=730 days) - simple average
    avg(case when days_tenure <= 730 then cp_alloc_adjusted * 1.0 / bookable_scheds_per_venue_per_month end) as short_tenure_le24mo
from avg_spot_alloc_per_venue_per_month
group by 1
order by 1
