# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-12-18

### Added
- Initial project structure with 6 SQL queries (3 monthly by tenure, 3 R7 rolling 7-day)
- Python scripts for executing queries programmatically
- Comprehensive documentation and analysis summaries
- README with project overview, findings, and technical details

### SQL Queries
- `01_spot_allocation_monthly_by_tenure.sql` - Monthly spot allocation by tenure
- `02_disabled_schedules_monthly_by_tenure.sql` - Monthly disabled schedules % by tenure
- `03_soft_churn_monthly_by_tenure.sql` - Monthly soft churn rate by tenure
- `04_spot_allocation_r7_rolling_7day.sql` - R7 spot allocation (Oct-Nov 2025)
- `05_disabled_schedules_r7_rolling_7day.sql` - R7 disabled schedules % (Oct-Nov 2025)
- `06_soft_churn_r7_rolling_7day.sql` - R7 soft churn rate (Oct-Nov 2025)

### Python Scripts
- `snowflake_connection.py` - Snowflake connection utility with SSO
- `run_all_queries_by_tenure.py` - Execute monthly tenure queries
- `run_rolling_7day_queries.py` - Execute R7 queries

### Documentation
- `tenure_queries_verification.md` - Query validation documentation
- `tenure_segmentation_results_summary.md` - Monthly results summary
- `rolling_7day_oct_nov_summary.md` - R7 analysis summary
- `tenure_definition_analysis.md` - Tenure definition analysis

### Fixed
- R7 soft churn calculation to properly aggregate over 7-day window
- R7 spot allocation to use simple average per venue (matching monthly)
- Soft churn query to include active venue filter

### Technical Details
- All queries output chart-ready data directly from SQL
- Calculation methods validated against expected results
- Tenure segmentation verified to match original query structure
