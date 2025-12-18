-- Chart 6: Soft Churn Rate - R7 Rolling 7-Day (Oct-Nov 2025)
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
r7_window_calc as 
(
    select 
        vac.date,
        vac.venue_id,
        sv.account_classification,
        vac.soft_churn,
        case when (GREATEST_IGNORE_NULLS(vac.acquisition_pin, vac.venue_inactive)) = 1 then 1 else 0 end as is_active
    from cp_bi_derived.datapipeline.venue_adds_and_churns vac 
    left join cp_bi_derived.datapipeline.partner_details pd on vac.venue_id = pd.venue_id
    left join cp_bi_derived.datapipeline.salesforce_venues sv on vac.venue_id = sv.venue_id
    INNER JOIN vids vvm on vac.venue_id = vvm.venue_id
    where vac.date >= '2025-10-01' and vac.date < '2025-12-01'
),
daily_metrics as 
(
    select 
        date,
        -- All Fitness - Daily (matches original query structure)
        sum(soft_churn) as soft_churns,
        count(distinct case when is_active = 1 then venue_id end) as venue_count,
        -- SA Fitness - Daily
        sum(case when account_classification = 'SA' then soft_churn else 0 end) as soft_churns_sa,
        count(distinct case when account_classification = 'SA' 
                and is_active = 1 then venue_id else null end) as venue_count_sa,
        -- Non-SA Fitness - Daily  
        sum(case when account_classification != 'SA' OR account_classification IS NULL then soft_churn else 0 end) as soft_churns_nonsa,
        count(distinct case when (account_classification != 'SA' OR account_classification IS NULL)
                and is_active = 1 then venue_id else null end) as venue_count_nonsa
    from r7_window_calc
    group by 1
),
r7_aggregated as 
(
    select 
        dm1.date,
        -- R7: Sum soft_churn over 7-day window (matches monthly: sum over month)
        (select sum(rwc2.soft_churn)
         from r7_window_calc rwc2
         where rwc2.date <= dm1.date and rwc2.date >= dateadd('day', -6, dm1.date)) as r7_soft_churns,
        -- R7: Count distinct venues over 7-day window (matches monthly: count distinct over month)
        (select count(distinct case when rwc2.is_active = 1 then rwc2.venue_id end)
         from r7_window_calc rwc2
         where rwc2.date <= dm1.date and rwc2.date >= dateadd('day', -6, dm1.date)) as r7_venue_count,
        -- SA Fitness R7
        (select sum(case when rwc2.account_classification = 'SA' then rwc2.soft_churn else 0 end)
         from r7_window_calc rwc2
         where rwc2.date <= dm1.date and rwc2.date >= dateadd('day', -6, dm1.date)) as r7_soft_churns_sa,
        (select count(distinct case when rwc2.account_classification = 'SA' 
                and rwc2.is_active = 1 then rwc2.venue_id else null end)
         from r7_window_calc rwc2
         where rwc2.date <= dm1.date and rwc2.date >= dateadd('day', -6, dm1.date)) as r7_venue_count_sa,
        -- Non-SA Fitness R7
        (select sum(case when rwc2.account_classification != 'SA' OR rwc2.account_classification IS NULL then rwc2.soft_churn else 0 end)
         from r7_window_calc rwc2
         where rwc2.date <= dm1.date and rwc2.date >= dateadd('day', -6, dm1.date)) as r7_soft_churns_nonsa,
        (select count(distinct case when (rwc2.account_classification != 'SA' OR rwc2.account_classification IS NULL)
                and rwc2.is_active = 1 then rwc2.venue_id else null end)
         from r7_window_calc rwc2
         where rwc2.date <= dm1.date and rwc2.date >= dateadd('day', -6, dm1.date)) as r7_venue_count_nonsa
    from daily_metrics dm1
)
select 
    dm.date,
    -- All Fitness - Rolling 7-day (R7) - matches monthly: sum(soft_churn) / count(distinct venue_id)
    r7.r7_soft_churns * 1.0 / nullif(r7.r7_venue_count, 0) * 100 as all_fitness_r7_pct,
    -- SA Fitness - Rolling 7-day (R7)
    r7.r7_soft_churns_sa * 1.0 / nullif(r7.r7_venue_count_sa, 0) * 100 as sa_fitness_r7_pct,
    -- Non-SA Fitness - Rolling 7-day (R7)
    r7.r7_soft_churns_nonsa * 1.0 / nullif(r7.r7_venue_count_nonsa, 0) * 100 as nonsa_fitness_r7_pct
from daily_metrics dm
join r7_aggregated r7 on dm.date = r7.date
order by 1
