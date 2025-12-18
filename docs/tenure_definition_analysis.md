# Partner Tenure Definition Analysis

## Team's Standard Definition

Based on the codebase review, here's how partner tenure is defined in your team's repo:

### Primary Definition (venue_value_model.sql, partner_optimization.sql)

```sql
-- Standard calculation:
CURRENT_DATE - pd.estimated_launch_date AS days_tenure

-- Special case for reactivated venues:
CASE
    WHEN pd.venue_status = 'reactivated' THEN CURRENT_DATE - pd.status_date
    ELSE CURRENT_DATE - pd.estimated_launch_date
END AS days_tenure
```

### Key Differences from My Initial Implementation

| Aspect | Team's Definition | My Initial Implementation |
|--------|------------------|---------------------------|
| **Unit** | **DAYS** | Months |
| **Reference Date** | **CURRENT_DATE** (snapshot as of today) | Analysis date (date from each record) |
| **Calculation** | `CURRENT_DATE - estimated_launch_date` | `DATEDIFF('month', estimated_launch_date, [analysis_date])` |

### Alternative Approach Found

In `venue_excelerate_scoring.sql`, there's a different approach that counts months of activity:
```sql
CASE 
    WHEN count(month) >= 24 THEN '>2yr'
    WHEN count(month) >= 12 THEN '1-2yr'
    WHEN count(month) >= 6 THEN '6-12mo'
    ELSE '<6mo' 
END AS tenure_cat
```
This counts months of actual activity, not time since launch.

## Implications for Your Queries

### Option 1: Match Team's Standard (DAYS, CURRENT_DATE)
- **Pros**: Consistent with existing codebase
- **Cons**: Tenure is static (doesn't change over time in historical analysis)
- **Use case**: Snapshot analysis as of today

### Option 2: Dynamic Tenure (DAYS, Analysis Date)
- **Pros**: Tenure changes over time (partners age during analysis period)
- **Cons**: Different from team's standard
- **Use case**: Historical trend analysis

### Option 3: Months-Based (as I initially implemented)
- **Pros**: Easier to interpret (24 months vs 730 days)
- **Cons**: Different from team's standard (which uses days)
- **Use case**: If you prefer month-based segmentation

## Recommendation

For **historical trend analysis** (which your queries are doing), I recommend **Option 2** (dynamic tenure using days):
- Calculate tenure relative to each analysis date
- Use days to match team's standard
- Convert to months for the >24 months threshold: `(analysis_date - estimated_launch_date) > 730` (24 months = 730 days)

This gives you:
- Consistency with team's unit (days)
- Dynamic tenure that changes over time
- Accurate historical analysis
