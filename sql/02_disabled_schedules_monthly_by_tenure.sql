-- Chart 2: Disabled Schedules - Monthly by Tenure (All Fitness, >24mo, <=24mo)
-- Outputs final chart-ready percentage values directly from SQL

with vids as 
(
    select sv.account_classification, pd.*
    from cp_bi_derived.datapipeline.partner_details pd
    left join cp_bi_derived.datapipeline.salesforce_venues sv on pd.venue_id = sv.venue_id
    where pd.venue_type = 'Fitness'
    and estimated_launch_date is not null
    -- NO VVM filter - this is for "All Fitness"
)
select 
    date_trunc('month', s.start_date) as month_date,
    -- All Fitness
    count(distinct case when unbookable_reason ilike '%schedule disable%' then schedule_id end) * 1.0 / 
        nullif(count(distinct schedule_id), 0) * 100 as all_fitness_pct,
    -- Long Tenure (>24mo = >730 days)
    count(distinct case when (s.start_date - v.estimated_launch_date) > 730 
            and unbookable_reason ilike '%schedule disable%' then schedule_id end) * 1.0 /
        nullif(count(distinct case when (s.start_date - v.estimated_launch_date) > 730 then schedule_id end), 0) * 100 as long_tenure_gt24mo_pct,
    -- Short Tenure (<=24mo = <=730 days)
    count(distinct case when (s.start_date - v.estimated_launch_date) <= 730 
            and unbookable_reason ilike '%schedule disable%' then schedule_id end) * 1.0 /
        nullif(count(distinct case when (s.start_date - v.estimated_launch_date) <= 730 then schedule_id end), 0) * 100 as short_tenure_le24mo_pct
from vids v
join cp_bi_derived.datapipeline.sched_schedules s on s.venue_id = v.venue_id
and s.start_date >= '2024-12-01' and s.start_date < '2025-12-01'
and (unbookable_reason is null or (unbookable_reason ilike '%schedule%' or unbookable_reason ilike '%zero spots%'))
and s.class_id not in (select distinct class_id from cp_bi_derived.datapipeline.ineligible_classes)
group by 1
order by 1
