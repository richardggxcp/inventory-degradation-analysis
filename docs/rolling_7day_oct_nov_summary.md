# Rolling 7-Day Analysis (Oct-Nov 2025) - Summary

## Overview
Daily data with rolling 7-day (R7) averages for Oct 1 - Nov 30, 2025
Segments: All Fitness, SA Fitness, Non-SA Fitness

## Results Files
- `spot_allocation_rolling_7day_results_[timestamp].csv`
- `disabled_schedules_rolling_7day_results_[timestamp].csv`
- `soft_churn_rolling_7day_results_[timestamp].csv`

---

## 1. Average Spot Allocation per Bookable Schedule

### Key Observations
- **Daily values show volatility** (ranging from ~1.8 to ~2.4)
- **R7 averages smooth out daily fluctuations** and show trends
- **All segments show similar patterns** with some divergence

### Trend Analysis (R7 values)
- **All Fitness R7**: Starts ~2.16-2.17, ends ~2.04 (slight decline)
- **SA Fitness R7**: Starts ~2.70-2.76, ends ~2.44 (decline)
- **Non-SA Fitness R7**: Starts ~2.00-2.06, ends ~1.93-1.94 (decline)

### Notable Patterns
- **Thanksgiving week (Nov 27-30)**: Sharp drop in daily values, R7 averages show decline
- **SA consistently higher** than Non-SA throughout the period
- **Daily volatility** is higher than monthly averages suggest

---

## 2. Disabled Schedules as % of Total Schedules

### Key Observations
- **Daily values show significant variation** (ranging from ~6% to ~13%)
- **R7 averages provide smoother trend view**
- **Clear downward trend** in R7 averages for all segments

### Trend Analysis (R7 values)
- **All Fitness R7**: Starts ~9.5%, ends ~10.17% (slight increase)
- **SA Fitness R7**: Starts ~6.4-6.7%, ends ~8.09% (increase)
- **Non-SA Fitness R7**: Starts ~9.7-9.8%, ends ~10.74% (increase)

### Notable Patterns
- **Thanksgiving week spike**: Nov 26-27 show sharp increases (10.25%, 12.45% daily)
- **SA performs better** (lower disabled rates) than Non-SA
- **End of period shows increase** in disabled rates across all segments

---

## 3. Soft Churn Rate

### Key Observations
- **Daily values are very low** (mostly 0.01-0.06%)
- **R7 averages are stable** around 0.03-0.04%
- **SA shows lower rates** than Non-SA

### Trend Analysis (R7 values)
- **All Fitness R7**: Stable around 0.03-0.04%
- **SA Fitness R7**: Very low, mostly 0.01-0.02%
- **Non-SA Fitness R7**: Slightly higher, around 0.03-0.04%

### Notable Patterns
- **Very stable** with minimal variation
- **SA consistently lower** than Non-SA
- **No sharp trends** visible in this short period

---

## Sharp Trend Detection

### Spot Allocation
- **Thanksgiving impact**: Sharp drop in daily values around Nov 27-30
- **Overall R7 trend**: Slight decline from Oct to Nov

### Disabled Schedules
- **Thanksgiving spike**: Significant increase Nov 26-27 (12.45% daily on Nov 27)
- **End-of-period increase**: R7 averages trending up in late November

### Soft Churn
- **No sharp trends**: Very stable throughout the period

---

## Files Created

1. **Query Files:**
   - `spot_allocation_rolling_7day.sql`
   - `disabled_schedules_rolling_7day.sql`
   - `soft_churn_rolling_7day.sql`

2. **Results CSV Files:**
   - All include daily values and R7 rolling averages
   - 61 days of data (Oct 1 - Nov 30, 2025)

3. **Execution Script:**
   - `run_rolling_7day_queries.py` - Runs all three queries programmatically

---

## Next Steps

The data is ready for visualization. You can:
1. Create line charts showing daily vs R7 trends
2. Identify specific date ranges with sharp changes
3. Compare All Fitness, SA, and Non-SA trends side-by-side
4. Focus on Thanksgiving week (Nov 26-30) for detailed analysis
