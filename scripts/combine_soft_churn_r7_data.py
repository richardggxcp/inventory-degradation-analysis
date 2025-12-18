#!/usr/bin/env python3
"""
Combine Jan-Sep 2024 R7 soft churn data with existing Oct-Nov 2024 & 2025 data
"""
import sys
import os
import pandas as pd
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')

def main():
    # Find the most recent extended historical file (Jan-Sep 2024)
    import glob
    extended_files = glob.glob(os.path.join(DATA_DIR, 'soft_churn_r7_extended_historical_*.csv'))
    if not extended_files:
        print("❌ No extended historical file found. Please run the query first.")
        return 1
    
    extended_file = max(extended_files, key=os.path.getctime)
    print(f"📖 Reading Jan-Sep 2024 data from: {os.path.basename(extended_file)}")
    
    # Find the existing Oct-Nov 2024 & 2025 file
    oct_nov_files = glob.glob(os.path.join(DATA_DIR, 'soft_churn_rolling_7day_results_*.csv'))
    if not oct_nov_files:
        print("❌ No Oct-Nov 2024 & 2025 file found.")
        return 1
    
    oct_nov_file = max(oct_nov_files, key=os.path.getctime)
    print(f"📖 Reading Oct-Nov 2024 & 2025 data from: {os.path.basename(oct_nov_file)}")
    
    # Read both files
    df_extended = pd.read_csv(extended_file)
    df_oct_nov = pd.read_csv(oct_nov_file)
    
    # Filter extended to Jan-Sep 2024 only (in case it includes buffer days)
    df_extended['date'] = pd.to_datetime(df_extended['date'])
    df_extended = df_extended[(df_extended['date'] >= '2024-01-01') & (df_extended['date'] < '2024-10-01')]
    
    # Ensure Oct-Nov data has date as datetime
    df_oct_nov['date'] = pd.to_datetime(df_oct_nov['date'])
    
    # Combine and sort
    df_combined = pd.concat([df_extended, df_oct_nov], ignore_index=True)
    df_combined = df_combined.sort_values('date').reset_index(drop=True)
    
    # Save combined file
    output_file = os.path.join(DATA_DIR, f'soft_churn_r7_full_2024_2025_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    df_combined.to_csv(output_file, index=False)
    
    print(f"\n✅ Combined data:")
    print(f"   Date range: {df_combined['date'].min().date()} to {df_combined['date'].max().date()}")
    print(f"   Total rows: {len(df_combined)}")
    print(f"   Jan-Sep 2024: {len(df_extended)} rows")
    print(f"   Oct-Nov 2024 & 2025: {len(df_oct_nov)} rows")
    print(f"\n💾 Saved to: {os.path.basename(output_file)}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
