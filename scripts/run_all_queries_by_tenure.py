#!/usr/bin/env python3
"""
Run all three queries with tenure segmentation and save results
"""
import sys
import os
from datetime import datetime
import pandas as pd

from snowflake_connection import execute_query, close_connection

QUERIES = {
    'spot_allocation': 'spot_allocation_by_tenure.sql',
    'disabled_schedules': 'disabled_schedules_by_tenure.sql',
    'soft_churn': 'soft_churn_by_tenure.sql'
}

def run_query(query_name, query_file):
    """Run a query and return results"""
    print(f"\n{'='*100}")
    print(f"Running {query_name} query...")
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
    output_file = f'{query_name}_by_tenure_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    df.to_csv(output_file, index=False)
    print(f"💾 Results saved to: {output_file}")
    
    return df, output_file

def format_month_date(date_val):
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
    print(f"{query_name.upper().replace('_', ' ')} RESULTS BY TENURE")
    print(f"{'='*100}\n")
    
    # Get month column
    month_col = [col for col in df.columns if 'month' in col.lower()][0]
    
    if query_name == 'spot_allocation':
        # Show simple averages (not weighted)
        print(f"{'Month':<15} {'All Fitness':<15} {'Long Tenure (>24mo)':<20} {'Short Tenure (<=24mo)':<20}")
        print("-" * 100)
        for _, row in df.iterrows():
            month_str = format_month_date(row[month_col])
            all_fitness = round(float(row.get('avg_spots_per_venue_all_fitness', 0) or 0), 1)
            long_tenure = round(float(row.get('avg_spots_per_venue_long_tenure', 0) or 0), 1)
            short_tenure = round(float(row.get('avg_spots_per_venue_short_tenure', 0) or 0), 1)
            print(f"{month_str:<15} {all_fitness:<15.1f} {long_tenure:<20.1f} {short_tenure:<20.1f}")
    
    elif query_name == 'disabled_schedules':
        print(f"{'Month':<15} {'All Fitness %':<15} {'Long Tenure (>24mo) %':<20} {'Short Tenure (<=24mo) %':<20}")
        print("-" * 100)
        for _, row in df.iterrows():
            month_str = format_month_date(row[month_col])
            all_fitness = round(float(row.get('disabled_rate_all_fitness_pct', 0) or 0), 1)
            long_tenure = round(float(row.get('disabled_rate_long_tenure_pct', 0) or 0), 1)
            short_tenure = round(float(row.get('disabled_rate_short_tenure_pct', 0) or 0), 1)
            print(f"{month_str:<15} {all_fitness:<15.1f} {long_tenure:<20.1f} {short_tenure:<20.1f}")
    
    elif query_name == 'soft_churn':
        print(f"{'Month':<15} {'All Fitness %':<15} {'Long Tenure (>24mo) %':<20} {'Short Tenure (<=24mo) %':<20}")
        print("-" * 100)
        for _, row in df.iterrows():
            month_str = format_month_date(row[month_col])
            all_fitness = round(float(row.get('soft_churn_rate_all_fitness', 0) or 0) * 100, 1)
            long_tenure = round(float(row.get('soft_churn_rate_long_tenure', 0) or 0) * 100, 1)
            short_tenure = round(float(row.get('soft_churn_rate_short_tenure', 0) or 0) * 100, 1)
            print(f"{month_str:<15} {all_fitness:<15.1f} {long_tenure:<20.1f} {short_tenure:<20.1f}")

def main():
    print("="*100)
    print("Running All Queries with Tenure Segmentation")
    print("="*100)
    print("\nQueries to run:")
    print("1. Spot Allocation (avg spots per bookable schedule)")
    print("2. Disabled Schedules (% of total schedules)")
    print("3. Soft Churn Rate")
    print("\nSegments: All Fitness, Long Tenure (>24mo), Short Tenure (<=24mo)")
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
            print(f"  ✓ {query_name.replace('_', ' ').title()}: {len(results[query_name])} months of data")
        
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
