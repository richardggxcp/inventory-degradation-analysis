-- Chart 5: Disabled Schedules - R7 Rolling 7-Day (Oct-Nov 2025)
-- Segments: All Fitness, SA Fitness, Non-SA Fitness
-- Outputs final chart-ready R7 percentage values directly from SQL

with vids as 
(
    select sv.account_classification, pd.*
    from cp_bi_derived.datapipeline.partner_details pd
    left join cp_bi_derived.datapipeline.salesforce_venues sv on pd.venue_id = sv.venue_id
    where pd.venue_type = 'Fitness'
    and estimated_launch_date is not null
    -- NO VVM filter - this is for "All Fitness"
),
daily_metrics as 
(
    select 
        s.start_date::date as date,
        -- All Fitness - Daily (matches original query structure)
        count(distinct schedule_id) as total_scheds,
        count(distinct case when unbookable_reason ilike '%schedule disable%' then schedule_id end) as disabled_scheds,
        -- SA Fitness - Daily
        count(distinct case when account_classification = 'SA' then schedule_id end) as SA_total_scheds,
        count(distinct case when account_classification = 'SA' 
                and unbookable_reason ilike '%schedule disable%' then schedule_id end) as SA_disabled_scheds,
        -- Non-SA Fitness - Daily
        count(distinct case when account_classification != 'SA' OR account_classification IS NULL then schedule_id end) as nonSA_total_scheds,
        count(distinct case when (account_classification != 'SA' OR account_classification IS NULL)
                and unbookable_reason ilike '%schedule disable%' then schedule_id end) as nonSA_disabled_scheds
    from vids v
    join cp_bi_derived.datapipeline.sched_schedules s on s.venue_id = v.venue_id
    and s.start_date >= '2025-10-01' and s.start_date < '2025-12-01'
    and (unbookable_reason is null or (unbookable_reason ilike '%schedule%' or unbookable_reason ilike '%zero spots%'))
    and s.class_id not in (select distinct class_id from cp_bi_derived.datapipeline.ineligible_classes)
    group by 1
)
select 
    date,
    -- All Fitness - Rolling 7-day (R7) - matches team's pattern
    avg(disabled_scheds * 1.0 / nullif(total_scheds, 0) * 100) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as all_fitness_r7_pct,
    -- SA Fitness - Rolling 7-day (R7)
    avg(SA_disabled_scheds * 1.0 / nullif(SA_total_scheds, 0) * 100) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as sa_fitness_r7_pct,
    -- Non-SA Fitness - Rolling 7-day (R7)
    avg(nonSA_disabled_scheds * 1.0 / nullif(nonSA_total_scheds, 0) * 100) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as nonsa_fitness_r7_pct
from daily_metrics
order by 1
