# Tenure Queries Verification

## Confirmation: All tenure queries follow the validated original query structure exactly

---

## 1. Spot Allocation

### Original Validated Query (`spot_allocation_no_vvm_filter.sql`)
- **Structure**: Groups by `venue_id`, `account_classification`, `month_date`
- **Calculation**: `avg(cp_alloc_adjusted * 1.0 / bookable_scheds_per_venue_per_month)` - **SIMPLE AVERAGE**
- **Validated**: Matches expected values (5.7-6.9 range)

### Tenure Query (`spot_allocation_by_tenure.sql`)
- **Structure**: Groups by `venue_id`, `account_classification`, `month_date`, `days_tenure`
- **Calculation**: `avg(cp_alloc_adjusted * 1.0 / bookable_scheds_per_venue_per_month)` - **SAME SIMPLE AVERAGE**
- **Difference**: Adds `days_tenure` calculation and filters in CASE statements
- **All Fitness segment**: Uses same calculation as original (no tenure filter)

**✓ VERIFIED**: Same calculation method, only adds tenure segmentation

---

## 2. Disabled Schedules

### Original Validated Query (`disabled_schedules_query.sql`)
- **Structure**: Groups by `month_date`, counts schedules directly
- **Calculation**: `count(distinct disabled_scheds) / count(distinct total_scheds) * 100`
- **Filters**: Same filters for unbookable_reason and ineligible_classes

### Tenure Query (`disabled_schedules_by_tenure.sql`)
- **Structure**: Groups by `month_date`, counts schedules directly
- **Calculation**: `count(distinct disabled_scheds) / count(distinct total_scheds) * 100` - **SAME**
- **Difference**: Adds tenure filter `(s.start_date - v.estimated_launch_date) > 730` in CASE statements
- **All Fitness segment**: Uses same calculation as original (no tenure filter)

**✓ VERIFIED**: Same structure and calculation, only adds tenure segmentation

---

## 3. Soft Churn

### Original Validated Query (`soft_churn_query_with_active_filter.sql`)
- **Structure**: Groups by `month`, aggregates `soft_churn` and `venue_id`
- **Calculation**: `sum(soft_churn) / count(distinct venue_id)` with active filter
- **Active Filter**: `(GREATEST_IGNORE_NULLS(vac.acquisition_pin, vac.venue_inactive)) = 1`
- **Validated**: Matches expected values (1.0% for Oct, 0.9% for Nov)

### Tenure Query (`soft_churn_by_tenure.sql`)
- **Structure**: Groups by `month`, aggregates `soft_churn` and `venue_id`
- **Calculation**: `sum(soft_churn) / count(distinct venue_id)` with active filter - **SAME**
- **Active Filter**: `(GREATEST_IGNORE_NULLS(vac.acquisition_pin, vac.venue_inactive)) = 1` - **SAME**
- **Difference**: Adds tenure filter `(vac.date - pd.estimated_launch_date) > 730` in CASE statements
- **All Fitness segment**: Uses same calculation as original (no tenure filter)

**✓ VERIFIED**: Same calculation method and active filter, only adds tenure segmentation

---

## Summary

All three tenure queries:
1. ✅ Use the **same CTE structure** as original queries
2. ✅ Use the **same calculation methods** (simple average, direct counts, sum/count distinct)
3. ✅ Use the **same filters** (active venue filter, ineligible classes, etc.)
4. ✅ Only difference: Adds tenure segmentation using `days_tenure > 730` vs `<= 730`
5. ✅ The "All Fitness" segment in tenure queries produces the same values as original queries

**Conclusion**: The tenure queries are correct - they follow the validated original query structure exactly, just with tenure segmentation added.
