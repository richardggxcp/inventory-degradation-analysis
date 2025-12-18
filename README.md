# Inventory Degradation Analysis

A comprehensive analysis of ClassPass schedules and partner soft churn over time, examining inventory degradation metrics across different partner segments and time horizons.

## 📊 Overview

This project analyzes three key metrics that indicate inventory degradation:

1. **Average Spot Allocation per Bookable Schedule** - Measures how many spots partners allocate to ClassPass
2. **Disabled Schedules as % of Total Schedules** - Tracks schedule availability issues
3. **Soft Churn Rate** - Measures partner engagement decline

The analysis is performed across multiple dimensions:
- **Segmentation**: All Fitness, SA Fitness, Non-SA Fitness, and by Partner Tenure (>24mo vs ≤24mo)
- **Time Periods**: Monthly trends (Dec 2024 - Nov 2025) and Rolling 7-day (R7) trends (Oct-Nov 2024 & 2025 for year-over-year comparison)

## 📁 Project Structure

```
inventory-degradation-analysis/
├── README.md                    # This file
├── sql/                         # SQL queries for chart-ready data
│   ├── 01_spot_allocation_monthly_by_tenure.sql
│   ├── 02_disabled_schedules_monthly_by_tenure.sql
│   ├── 03_soft_churn_monthly_by_tenure.sql
│   ├── 04_spot_allocation_r7_rolling_7day.sql
│   ├── 05_disabled_schedules_r7_rolling_7day.sql
│   └── 06_soft_churn_r7_rolling_7day.sql
├── scripts/                     # Python execution scripts
│   ├── snowflake_connection.py
│   ├── run_all_queries_by_tenure.py
│   └── run_rolling_7day_queries.py
├── docs/                        # Documentation and analysis summaries
│   ├── tenure_queries_verification.md
│   ├── tenure_segmentation_results_summary.md
│   ├── rolling_7day_oct_nov_summary.md
│   └── tenure_definition_analysis.md
└── data/                        # Output CSV files (gitignored)
```

## 🎯 Key Metrics

### 1. Average Spot Allocation per Bookable Schedule
- **Definition**: Average number of ClassPass spots allocated per bookable schedule
- **Calculation Method**: Simple average per venue (groups by venue_id first, then averages venue-level ratios)
- **Segments**: All Fitness, SA Fitness, Non-SA Fitness, Long Tenure (>24mo), Short Tenure (≤24mo)
- **Expected Range**: 5.7-6.9 (monthly), ~2.0-2.7 (daily R7)

### 2. Disabled Schedules as % of Total Schedules
- **Definition**: Percentage of schedules disabled due to partner actions
- **Calculation**: `count(distinct disabled_schedules) / count(distinct total_schedules) * 100`
- **Segments**: Same as above
- **Expected Range**: 8-13% (monthly), ~6-13% (daily R7)

### 3. Soft Churn Rate
- **Definition**: Rate of partner soft churn (venue-level churn indicator)
- **Calculation**: `sum(soft_churn) / count(distinct active_venue_id) * 100`
- **Active Venue Filter**: `(GREATEST_IGNORE_NULLS(acquisition_pin, venue_inactive)) = 1`
- **Segments**: Same as above
- **Expected Range**: 0.5-1.3% (monthly), ~0.01-0.06% (daily R7)

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Snowflake access with SSO authentication
- Required Python packages:
  ```bash
  pip install snowflake-connector-python pandas
  ```

### Running Queries

#### Monthly Queries by Tenure
```bash
cd scripts
python run_all_queries_by_tenure.py
```

#### Rolling 7-Day Queries (Oct-Nov 2025)
```bash
cd scripts
python run_rolling_7day_queries.py
```

### Direct SQL Execution

All SQL files in the `sql/` directory output chart-ready data directly. You can run them directly in Snowflake:

```sql
-- Example: Monthly spot allocation by tenure
-- File: sql/01_spot_allocation_monthly_by_tenure.sql
-- Output columns: month_date, all_fitness, long_tenure_gt24mo, short_tenure_le24mo
```

## 📈 Key Findings

### Monthly Trends (Dec 2024 - Nov 2025)

#### Spot Allocation
- ✅ **Upward trend** across all segments
- **All Fitness**: 6.1 → 6.8 (+0.7)
- **Long Tenure (>24mo)**: 7.0 → 7.2 (+0.2) - Higher absolute values, slower growth
- **Short Tenure (≤24mo)**: 5.1 → 6.2 (+1.1) - Stronger growth, catching up

#### Disabled Schedules
- ✅ **Downward trend** (improvement) across all segments
- **All Fitness**: 12.2% → 9.4% (-2.8%)
- **Long Tenure**: 13.7% → 10.8% (-2.9%)
- **Short Tenure**: 11.5% → 8.5% (-3.0%) - Better performance and stronger improvement

#### Soft Churn Rate
- ✅ **Long tenure performs better** (lower churn)
- **All Fitness**: 1.0% → 0.9% (-0.1%)
- **Long Tenure**: 0.7% → 0.5% (-0.2%)
- **Short Tenure**: 1.2% → 1.2% (stable, higher than long tenure)

### Rolling 7-Day Trends (Oct-Nov 2024 & 2025 - Year-over-Year Comparison)

#### Spot Allocation
- **Thanksgiving impact**: Sharp drop in daily values around Nov 27-30
- **Overall R7 trend**: Slight decline from Oct to Nov
- **SA consistently higher** than Non-SA throughout

#### Disabled Schedules
- **Thanksgiving spike**: Significant increase Nov 26-27 (12.45% daily on Nov 27)
- **End-of-period increase**: R7 averages trending up in late November
- **SA performs better** (lower disabled rates) than Non-SA

#### Soft Churn
- **Very stable** throughout the period (~0.03-0.04%)
- **SA consistently lower** than Non-SA
- **No sharp trends** visible in this short period

## 🔍 Technical Details

### Calculation Methods

#### Spot Allocation
- **Method**: Simple average per venue
- **Process**: 
  1. Group by `venue_id`, `date/month`, calculate `cp_alloc_adjusted / bookable_schedules` per venue
  2. Average these venue-level ratios
- **Rationale**: Matches original validated query structure (produces 5.7-6.9 range)

#### Disabled Schedules
- **Method**: Direct count ratio
- **Process**: `count(distinct disabled_schedules) / count(distinct total_schedules)`
- **Filters**: Includes schedules with `unbookable_reason` containing "schedule disable" or "zero spots"

#### Soft Churn Rate
- **Method**: Sum over count distinct
- **Process**: `sum(soft_churn) / count(distinct active_venue_id)`
- **Active Filter**: `(GREATEST_IGNORE_NULLS(acquisition_pin, venue_inactive)) = 1`
- **R7 Calculation**: Uses 7-day rolling window with `dateadd('day', -6, date)` to match monthly logic

### Tenure Definition
- **Long Tenure**: Partners launched >24 months ago (`days_tenure > 730`)
- **Short Tenure**: Partners launched ≤24 months ago (`days_tenure <= 730`)
- **Tenure Calculation**: `(schedule_date - estimated_launch_date)` or `(churn_date - estimated_launch_date)`

### Rolling 7-Day (R7) Calculation
- **Window**: `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`
- **For Soft Churn**: Uses subqueries with `dateadd('day', -6, date)` to properly aggregate `sum()` and `count(distinct)` over the 7-day window
- **Rationale**: Matches team's standard R7/R28 rolling average pattern

## 📊 Data Sources

### Snowflake Tables
- `cp_bi_derived.datapipeline.partner_details` - Partner and venue metadata
- `cp_bi_derived.datapipeline.salesforce_venues` - Account classification (SA vs Non-SA)
- `cp_bi_derived.datapipeline.sched_schedules` - Schedule-level data
- `cp_bi_derived.datapipeline.venue_adds_and_churns` - Soft churn data
- `cp_bi_derived.datapipeline.ineligible_classes` - Classes to exclude

### Filters Applied
- **Venue Type**: `venue_type = 'Fitness'`
- **Launch Date**: `estimated_launch_date IS NOT NULL`
- **VVM Filter**: None (analyzing "All Fitness", not just VVM 85+)
- **Ineligible Classes**: Excludes classes in `ineligible_classes` table
- **Active Venues**: For soft churn, only counts venues where `(GREATEST_IGNORE_NULLS(acquisition_pin, venue_inactive)) = 1`

## 🔧 Query Validation

All queries have been validated against expected results:

1. **Spot Allocation**: Validated against monthly values (5.7-6.9 range) ✅
2. **Disabled Schedules**: Validated against monthly percentages ✅
3. **Soft Churn Rate**: Validated against monthly rates (1.0% Oct, 0.9% Nov) ✅

Tenure-segmented queries follow the exact same structure as validated queries, only adding tenure filters.

See `docs/tenure_queries_verification.md` for detailed verification notes.

## 📝 Files Description

### SQL Queries (`sql/`)

#### Original Validated Queries (Baseline)
- `00_spot_allocation_monthly_original.sql` - Original validated spot allocation (All Fitness, SA Fitness, Non-SA Fitness)
- `00_disabled_schedules_monthly_original.sql` - Original validated disabled schedules % (All Fitness, SA Fitness, Non-SA Fitness)
- `00_soft_churn_monthly_original.sql` - Original validated soft churn rate (All Fitness, SA Fitness, Non-SA Fitness)

#### Monthly by Tenure (Charts 1-3)
- `01_spot_allocation_monthly_by_tenure.sql` - Monthly spot allocation segmented by tenure
- `02_disabled_schedules_monthly_by_tenure.sql` - Monthly disabled schedules % by tenure
- `03_soft_churn_monthly_by_tenure.sql` - Monthly soft churn rate by tenure

#### Rolling 7-Day (Charts 4-6) - Year-over-Year Comparison
- `04_spot_allocation_r7_rolling_7day.sql` - R7 spot allocation (Oct-Nov 2024 & 2025)
- `05_disabled_schedules_r7_rolling_7day.sql` - R7 disabled schedules % (Oct-Nov 2024 & 2025)
- `06_soft_churn_r7_rolling_7day.sql` - R7 soft churn rate (Oct-Nov 2024 & 2025)

### Python Scripts (`scripts/`)

- `snowflake_connection.py` - Snowflake connection utility with SSO authentication and connection caching
- `run_all_queries_by_tenure.py` - Executes monthly tenure-segmented queries and saves results
- `run_rolling_7day_queries.py` - Executes R7 queries for Oct-Nov 2025 and saves results

### Documentation (`docs/`)

- `tenure_queries_verification.md` - Verification that tenure queries match original validated structure
- `tenure_segmentation_results_summary.md` - Summary of monthly tenure-segmented results
- `rolling_7day_oct_nov_summary.md` - Summary of R7 trend analysis findings
- `tenure_definition_analysis.md` - Analysis of partner tenure definition

## 🐛 Known Issues & Solutions

### Issue: R7 Soft Churn Values Much Lower Than Monthly
- **Root Cause**: Initial calculation averaged daily rates instead of aggregating over 7-day window
- **Solution**: Updated to use subqueries with `dateadd('day', -6, date)` to properly `sum(soft_churn)` and `count(distinct venue_id)` over the 7-day window
- **Result**: R7 values now proportional to monthly (~0.23% for 7 days vs 1.0% for 30 days)

### Issue: Spot Allocation R7 Values Lower Than Monthly
- **Root Cause**: Initial calculation used weighted average instead of simple average
- **Solution**: Updated to use simple average per venue (group by venue_id first, then average ratios)
- **Result**: R7 values now match expected range (~2.0-2.7)

### Issue: Missing Active Venue Filter in Soft Churn
- **Root Cause**: Initial query didn't include `(GREATEST_IGNORE_NULLS(acquisition_pin, venue_inactive)) = 1` filter
- **Solution**: Added active venue filter to denominator calculation
- **Result**: Soft churn rates now match expected values (1.0% Oct, 0.9% Nov)

## 📅 Change Log

### 2025-12-18
- Created final 6 SQL queries (3 monthly by tenure, 3 R7 rolling 7-day)
- All queries output chart-ready data directly from SQL
- Organized project structure and documentation

### 2025-12-17
- Fixed R7 soft churn calculation to properly aggregate over 7-day window
- Updated R7 spot allocation to use simple average per venue
- Created R7-only CSV files for plotting

### 2025-12-16
- Created tenure-segmented queries (All Fitness, >24mo, ≤24mo)
- Validated tenure queries match original query structure
- Created rolling 7-day queries for Oct-Nov 2025

### 2025-12-15
- Validated all three original queries against expected results
- Fixed soft churn query to include active venue filter
- Confirmed spot allocation uses simple average per venue

## 🤝 Contributing

When making changes:
1. Update the relevant SQL query in `sql/`
2. Test against expected results
3. Update documentation in `docs/` if calculation methods change
4. Update this README if findings or structure change

## 📄 License

Internal ClassPass project - Confidential

## 👤 Author

Richard Goh - ClassPass Data Science Team
