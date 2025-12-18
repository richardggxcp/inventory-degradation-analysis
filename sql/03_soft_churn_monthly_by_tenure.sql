-- Chart 3: Soft Churn Rate - Monthly by Tenure (All Fitness, >24mo, <=24mo)
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
    date_trunc('month', date) as month,
    -- All Fitness (with active venue filter)
    sum(vac.soft_churn) * 1.0 / nullif(count(distinct case when (GREATEST_IGNORE_NULLS(vac.acquisition_pin, vac.venue_inactive)) = 1 then vac.venue_id end), 0) * 100 as all_fitness_pct,
    -- Long Tenure (>24mo = >730 days) - with active venue filter
    sum(case when (vac.date - pd.estimated_launch_date) > 730 then vac.soft_churn else 0 end) * 1.0 /
        nullif(count(distinct case when (vac.date - pd.estimated_launch_date) > 730 
                and (GREATEST_IGNORE_NULLS(vac.acquisition_pin, vac.venue_inactive)) = 1 then vac.venue_id else null end), 0) * 100 as long_tenure_gt24mo_pct,
    -- Short Tenure (<=24mo = <=730 days) - with active venue filter
    sum(case when (vac.date - pd.estimated_launch_date) <= 730 then vac.soft_churn else 0 end) * 1.0 /
        nullif(count(distinct case when (vac.date - pd.estimated_launch_date) <= 730 
                and (GREATEST_IGNORE_NULLS(vac.acquisition_pin, vac.venue_inactive)) = 1 then vac.venue_id else null end), 0) * 100 as short_tenure_le24mo_pct
from cp_bi_derived.datapipeline.venue_adds_and_churns vac 
left join cp_bi_derived.datapipeline.partner_details pd on vac.venue_id = pd.venue_id
left join cp_bi_derived.datapipeline.salesforce_venues sv on vac.venue_id = sv.venue_id
INNER JOIN vids vvm on vac.venue_id = vvm.venue_id
where date between '2024-11-01' and '2025-11-30'
group by 1
order by 1
