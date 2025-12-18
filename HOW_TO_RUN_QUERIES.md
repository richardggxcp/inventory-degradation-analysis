# How to Run Queries Programmatically

## Prerequisites

1. **Python 3.7+** installed
2. **Required packages:**
   ```bash
   pip install snowflake-connector-python pandas
   ```
3. **Snowflake access** with SSO authentication configured

## Setup

1. **Navigate to the scripts directory:**
   ```bash
   cd inventory-degradation-analysis/scripts
   ```

2. **The `snowflake_connection.py` module handles:**
   - SSO authentication (opens browser for login)
   - Connection caching (reuses connections to avoid repeated authentication)
   - Query execution and result fetching

## Running Queries

### Option 1: Use the Provided Scripts

#### For R7 Rolling 7-Day Queries (Oct-Nov 2024 & 2025):
```bash
cd scripts
python3 run_rolling_7day_queries.py
```

This will:
- Execute all 3 R7 queries (spot allocation, disabled schedules, soft churn)
- Save results to CSV files in the `data/` directory
- Display results in the terminal

#### For Extended Historical Soft Churn (Jan-Sep 2024):
```bash
cd scripts
python3 run_extended_soft_churn_r7.py
```

### Option 2: Run Queries Directly in Python

```python
import sys
import os
sys.path.insert(0, 'scripts')  # Add scripts directory to path

from snowflake_connection import execute_query, close_connection
import pandas as pd

# Read SQL file
with open('sql/06_soft_churn_r7_rolling_7day.sql', 'r') as f:
    query = f.read()

# Execute query
df = execute_query(query, fetch_data=True, reuse_connection=True)

# Process results
df.columns = df.columns.str.lower()  # Normalize column names
print(f"Retrieved {len(df)} rows")
print(df.head())

# Save to CSV
df.to_csv('output.csv', index=False)

# Close connection
close_connection()
```

## How It Works

1. **`snowflake_connection.py`** provides:
   - `execute_query(query, fetch_data=True, reuse_connection=True)` - Executes SQL and returns DataFrame
   - `get_connection(reuse=True)` - Gets or creates Snowflake connection
   - `close_connection()` - Closes the cached connection

2. **SSO Authentication:**
   - First run opens a browser window for authentication
   - Connection is cached and reused for subsequent queries
   - Set `reuse_connection=False` to force new authentication

3. **Connection Configuration:**
   - Account: `MINDBODYORG-MINDBODY`
   - User: `RICHARD.GOH@CLASSPASS.COM`
   - Authenticator: `externalbrowser` (SSO)
   - Role: `SNF-CP-DATASCIENCE`
   - Warehouse: `TEAM_CP_DATASCIENCE`
   - Database: `CP_BI_DERIVED`
   - Schema: `DATAPIPELINE`

## Troubleshooting

### Connection Issues
- Make sure you're authenticated in the browser when prompted
- Check that your Snowflake account has access to the required tables
- Verify warehouse is running: `SHOW WAREHOUSES`

### Query Timeout
- Long-running queries may take 10-30+ minutes
- Check Snowflake query history in the web UI
- Consider breaking large queries into smaller date ranges

### Column Name Issues
- Snowflake returns uppercase column names by default
- Use `df.columns = df.columns.str.lower()` to normalize

## Example: Testing Connection

```bash
cd scripts
python3 test_snowflake_connection.py
```

This runs simple test queries to verify connectivity.
