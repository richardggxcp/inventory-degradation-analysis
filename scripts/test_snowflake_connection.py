#!/usr/bin/env python3
"""Test Snowflake connection with simple queries"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from snowflake_connection import execute_query, close_connection

print('='*80)
print('Testing Snowflake Connection')
print('='*80)

# Test 1: Basic connection
print('\n1. Testing basic connection...')
try:
    df = execute_query("SELECT CURRENT_TIMESTAMP() as test_time", fetch_data=True, reuse_connection=False)
    df.columns = df.columns.str.lower()
    print(f'✅ Connection works! Time: {df.iloc[0]["test_time"]}')
except Exception as e:
    print(f'❌ Connection failed: {e}')
    close_connection()
    sys.exit(1)

# Test 2: Simple query - 1 row
print('\n2. Testing simple query (1 row from venue_adds_and_churns)...')
try:
    df = execute_query("""
        SELECT date, venue_id, soft_churn
        FROM cp_bi_derived.datapipeline.venue_adds_and_churns
        WHERE date = '2024-01-01'
        LIMIT 1
    """, fetch_data=True, reuse_connection=True)
    print(f'✅ Query works! Retrieved {len(df)} row(s)')
    print(df)
except Exception as e:
    print(f'❌ Query failed: {e}')
    import traceback
    traceback.print_exc()

# Test 3: Count rows
print('\n3. Testing count query for Jan-Sep 2024...')
try:
    df = execute_query("""
        SELECT COUNT(*) as row_count
        FROM cp_bi_derived.datapipeline.venue_adds_and_churns
        WHERE date >= '2024-01-01' AND date < '2024-10-01'
    """, fetch_data=True, reuse_connection=True)
    df.columns = df.columns.str.lower()
    print(f'✅ Count query works!')
    print(f'   Total rows: {df.iloc[0]["row_count"]:,}')
except Exception as e:
    print(f'❌ Count query failed: {e}')
    import traceback
    traceback.print_exc()

print('\n' + '='*80)
print('Test complete!')
print('='*80)

close_connection()
