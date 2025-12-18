-- Chart 4: Spot Allocation - R7 Rolling 7-Day (Oct-Nov 2024 & 2025)
-- Segments: All Fitness, SA Fitness, Non-SA Fitness
-- Outputs final chart-ready R7 values directly from SQL
-- Includes both 2024 and 2025 for year-over-year comparison

with all_fitness_vids as 
(
    select 
        sv.account_classification, 
        pd.*
    from cp_bi_derived.datapipeline.partner_details pd
    left join cp_bi_derived.datapipeline.salesforce_venues sv on pd.venue_id = sv.venue_id
    where pd.venue_type = 'Fitness'
    and estimated_launch_date is not null
),
avg_spot_alloc_per_venue_per_day as 
(
    select 
        s.venue_id, 
        account_classification,
        s.start_date::date as date,
        count(distinct s.schedule_id) as bookable_scheds_per_venue_per_day,
        sum(case when is_bookable = 'false' then 0
               when is_bookable = 'true' and classpass_spots < 
                (max_capacity - total_booked + classpass_spots_taken) THEN classpass_spots
               else (max_capacity - total_booked + classpass_spots_taken)
               end) as cp_alloc_adjusted
    from all_fitness_vids v
    join cp_bi_derived.datapipeline.sched_schedules s on s.venue_id = v.venue_id
    and s.start_date >= '2024-10-01' and s.start_date < '2025-12-01'
    and unbookable_reason is null
    and s.class_id not in (select distinct class_id from cp_bi_derived.datapipeline.ineligible_classes)
    group by 1, 2, 3
),
daily_metrics as 
(
    select 
        date,
        -- All Fitness - Daily (SIMPLE AVERAGE: avg of venue-level ratios, matches original monthly view)
        avg(cp_alloc_adjusted * 1.0 / nullif(bookable_scheds_per_venue_per_day, 0)) as avg_spots_all_fitness_daily,
        -- SA Fitness - Daily (SIMPLE AVERAGE)
        avg(case when account_classification = 'SA' then cp_alloc_adjusted * 1.0 / nullif(bookable_scheds_per_venue_per_day, 0) end) as avg_spots_SA_fitness_daily,
        -- Non-SA Fitness - Daily (SIMPLE AVERAGE)
        avg(case when account_classification != 'SA' OR account_classification IS NULL then cp_alloc_adjusted * 1.0 / nullif(bookable_scheds_per_venue_per_day, 0) end) as avg_spots_nonSA_fitness_daily
    from avg_spot_alloc_per_venue_per_day
    group by 1
)
select 
    date,
    -- All Fitness - Rolling 7-day (R7) - matches team's pattern
    avg(avg_spots_all_fitness_daily) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as all_fitness_r7,
    -- SA Fitness - Rolling 7-day (R7)
    avg(avg_spots_SA_fitness_daily) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as sa_fitness_r7,
    -- Non-SA Fitness - Rolling 7-day (R7)
    avg(avg_spots_nonSA_fitness_daily) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as nonsa_fitness_r7
from daily_metrics
order by 1
