#!/usr/bin/env python3
"""
Run all three queries with rolling 7-day aggregation for Oct-Nov 2024 & 2025
Daily data with R7 rolling averages - includes year-over-year comparison
"""
import sys
import os
from datetime import datetime
import pandas as pd

from snowflake_connection import execute_query, close_connection

# Get the project root directory (parent of scripts directory)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
SQL_DIR = os.path.join(PROJECT_ROOT, 'sql')

QUERIES = {
    'spot_allocation': os.path.join(SQL_DIR, '04_spot_allocation_r7_rolling_7day.sql'),
    'disabled_schedules': os.path.join(SQL_DIR, '05_disabled_schedules_r7_rolling_7day.sql'),
    'soft_churn': os.path.join(SQL_DIR, '06_soft_churn_r7_rolling_7day.sql')
}

def run_query(query_name, query_file):
    """Run a query and return results"""
    print(f"\n{'='*100}")
    print(f"Running {query_name} query (Rolling 7-day, Oct-Nov 2025)...")
    print(f"{'='*100}")
    
    if not os.path.exists(query_file):
        print(f"❌ Query file not found: {query_file}")
        return None
    
    with open(query_file, 'r') as f:
        query = f.read()
    
    print(f"📖 Query file: {query_file}")
    print("⏳ Executing query...")
    
    df = execute_query(query, fetch_data=True, reuse_connection=True)
    
    if df is None or len(df) == 0:
        print(f"❌ Query returned no results")
        return None
    
    print(f"✅ Retrieved {len(df)} rows")
    
    # Normalize column names
    df.columns = df.columns.str.lower()
    
    # Save results
    output_file = f'{query_name}_rolling_7day_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    df.to_csv(output_file, index=False)
    print(f"💾 Results saved to: {output_file}")
    
    return df, output_file

def format_date(date_val):
    """Format date to YYYY-MM-DD string"""
    if isinstance(date_val, datetime):
        return date_val.strftime('%Y-%m-%d')
    elif isinstance(date_val, str):
        try:
            dt = datetime.strptime(date_val[:10], '%Y-%m-%d')
            return dt.strftime('%Y-%m-%d')
        except:
            return str(date_val)
    return str(date_val)

def display_results(query_name, df):
    """Display query results in a readable format"""
    print(f"\n{'='*100}")
    print(f"{query_name.upper().replace('_', ' ')} - ROLLING 7-DAY (Oct-Nov 2024 & 2025)")
    print(f"{'='*100}\n")
    
    # Get date column
    date_col = [col for col in df.columns if 'date' in col.lower()][0]
    
    if query_name == 'spot_allocation':
        print(f"{'Date':<12} {'All Fitness (R7)':<20} {'SA Fitness (R7)':<20} {'Non-SA (R7)':<20}")
        print("-" * 80)
        for _, row in df.iterrows():
            date_str = format_date(row[date_col])
            all_r7 = round(float(row.get('all_fitness_r7', 0) or 0), 2)
            sa_r7 = round(float(row.get('sa_fitness_r7', 0) or 0), 2)
            nonsa_r7 = round(float(row.get('nonsa_fitness_r7', 0) or 0), 2)
            print(f"{date_str:<12} {all_r7:<20.2f} {sa_r7:<20.2f} {nonsa_r7:<20.2f}")
    
    elif query_name == 'disabled_schedules':
        print(f"{'Date':<12} {'All Fitness (R7 %)':<22} {'SA Fitness (R7 %)':<22} {'Non-SA (R7 %)':<22}")
        print("-" * 80)
        for _, row in df.iterrows():
            date_str = format_date(row[date_col])
            all_r7 = round(float(row.get('all_fitness_r7_pct', 0) or 0), 2)
            sa_r7 = round(float(row.get('sa_fitness_r7_pct', 0) or 0), 2)
            nonsa_r7 = round(float(row.get('nonsa_fitness_r7_pct', 0) or 0), 2)
            print(f"{date_str:<12} {all_r7:<22.2f} {sa_r7:<22.2f} {nonsa_r7:<22.2f}")
    
    elif query_name == 'soft_churn':
        print(f"{'Date':<12} {'All Fitness (R7 %)':<22} {'SA Fitness (R7 %)':<22} {'Non-SA (R7 %)':<22}")
        print("-" * 80)
        for _, row in df.iterrows():
            date_str = format_date(row[date_col])
            all_r7 = round(float(row.get('all_fitness_r7_pct', 0) or 0), 2)
            sa_r7 = round(float(row.get('sa_fitness_r7_pct', 0) or 0), 2)
            nonsa_r7 = round(float(row.get('nonsa_fitness_r7_pct', 0) or 0), 2)
            print(f"{date_str:<12} {all_r7:<22.2f} {sa_r7:<22.2f} {nonsa_r7:<22.2f}")

def main():
    print("="*100)
    print("Running Queries with Rolling 7-Day Aggregation (Oct-Nov 2025)")
    print("="*100)
    print("\nQueries to run:")
    print("1. Spot Allocation (avg spots per bookable schedule)")
    print("2. Disabled Schedules (% of total schedules)")
    print("3. Soft Churn Rate")
    print("\nSegments: All Fitness, SA Fitness, Non-SA Fitness")
    print("Time Period: Oct 1 - Nov 30, 2024 & 2025 (year-over-year comparison)")
    print("Aggregation: Daily + Rolling 7-day (R7) averages")
    print("="*100)
    
    results = {}
    
    try:
        for query_name, query_file in QUERIES.items():
            result = run_query(query_name, query_file)
            if result:
                df, output_file = result
                results[query_name] = df
                display_results(query_name, df)
        
        print(f"\n{'='*100}")
        print("✅ All queries completed successfully!")
        print(f"{'='*100}")
        print("\nSummary:")
        for query_name in results.keys():
            print(f"  ✓ {query_name.replace('_', ' ').title()}: {len(results[query_name])} days of data")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        close_connection()

if __name__ == '__main__':
    sys.exit(main())
