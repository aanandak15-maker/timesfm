#!/usr/bin/env python3
"""
Universal CSV Data Preparation Script for TimesFM
Converts any CSV with date and value columns to TimesFM format
"""

import pandas as pd
import numpy as np
import argparse
import sys
from datetime import datetime

def detect_date_column(df):
    """Detect the date column in the DataFrame"""
    date_columns = []
    
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in ['date', 'time', 'timestamp', 'day', 'month', 'year']):
            date_columns.append(col)
    
    return date_columns

def detect_value_column(df):
    """Detect the value column in the DataFrame"""
    value_columns = []
    
    for col in df.columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in ['value', 'price', 'yield', 'amount', 'quantity', 'rate', 'level', 'temp', 'moisture']):
            value_columns.append(col)
    
    return value_columns

def convert_date_format(date_series):
    """Convert various date formats to YYYY-MM-DD"""
    try:
        # Try to parse as datetime
        parsed_dates = pd.to_datetime(date_series, errors='coerce')
        
        # Check if any dates failed to parse
        if parsed_dates.isna().any():
            print("⚠️  Warning: Some dates could not be parsed. They will be removed.")
        
        # Convert to YYYY-MM-DD format
        formatted_dates = parsed_dates.dt.strftime('%Y-%m-%d')
        
        return formatted_dates
    except Exception as e:
        print(f"❌ Error converting dates: {e}")
        return None

def prepare_csv_for_timesfm(input_file, output_file=None, date_col=None, value_col=None):
    """
    Prepare any CSV file for TimesFM
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file (optional)
        date_col: Name of date column (optional, will auto-detect)
        value_col: Name of value column (optional, will auto-detect)
    """
    
    print(f"📊 Preparing {input_file} for TimesFM...")
    print("=" * 50)
    
    try:
        # Read the CSV file
        df = pd.read_csv(input_file)
        print(f"✅ Loaded CSV with {len(df)} rows and {len(df.columns)} columns")
        print(f"📋 Columns: {list(df.columns)}")
        
        # Auto-detect columns if not specified
        if date_col is None:
            date_candidates = detect_date_column(df)
            if date_candidates:
                date_col = date_candidates[0]
                print(f"🔍 Auto-detected date column: '{date_col}'")
            else:
                print("❌ Could not auto-detect date column. Please specify with --date-col")
                return False
        
        if value_col is None:
            value_candidates = detect_value_column(df)
            if value_candidates:
                value_col = value_candidates[0]
                print(f"🔍 Auto-detected value column: '{value_col}'")
            else:
                print("❌ Could not auto-detect value column. Please specify with --value-col")
                return False
        
        # Check if columns exist
        if date_col not in df.columns:
            print(f"❌ Date column '{date_col}' not found in CSV")
            return False
        
        if value_col not in df.columns:
            print(f"❌ Value column '{value_col}' not found in CSV")
            return False
        
        # Create new DataFrame with required columns
        prepared_df = pd.DataFrame()
        
        # Convert date column
        print(f"📅 Converting date column '{date_col}'...")
        prepared_df['date'] = convert_date_format(df[date_col])
        
        if prepared_df['date'] is None:
            print("❌ Failed to convert dates")
            return False
        
        # Convert value column to numeric
        print(f"📈 Converting value column '{value_col}'...")
        prepared_df['value'] = pd.to_numeric(df[value_col], errors='coerce')
        
        # Remove rows with missing values
        original_length = len(prepared_df)
        prepared_df = prepared_df.dropna()
        removed_count = original_length - len(prepared_df)
        
        if removed_count > 0:
            print(f"⚠️  Removed {removed_count} rows with missing values")
        
        # Sort by date
        prepared_df = prepared_df.sort_values('date')
        
        # Reset index
        prepared_df = prepared_df.reset_index(drop=True)
        
        # Generate output filename if not provided
        if output_file is None:
            base_name = input_file.replace('.csv', '')
            output_file = f"{base_name}_timesfm_ready.csv"
        
        # Save prepared data
        prepared_df.to_csv(output_file, index=False)
        
        # Print summary
        print(f"\n✅ Data preparation completed!")
        print(f"📁 Output file: {output_file}")
        print(f"📊 Records: {len(prepared_df)}")
        print(f"📅 Date range: {prepared_df['date'].min()} to {prepared_df['date'].max()}")
        print(f"📈 Value range: {prepared_df['value'].min():.2f} to {prepared_df['value'].max():.2f}")
        
        # Show sample data
        print(f"\n📋 Sample data:")
        print(prepared_df.head())
        
        print(f"\n🚀 Ready to upload to TimesFM frontend!")
        print(f"   Upload {output_file} to http://localhost:8501")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return False

def main():
    """Main function with command line interface"""
    
    parser = argparse.ArgumentParser(description='Prepare CSV data for TimesFM')
    parser.add_argument('input_file', help='Input CSV file path')
    parser.add_argument('-o', '--output', help='Output CSV file path (optional)')
    parser.add_argument('-d', '--date-col', help='Name of date column (optional, auto-detect if not specified)')
    parser.add_argument('-v', '--value-col', help='Name of value column (optional, auto-detect if not specified)')
    
    args = parser.parse_args()
    
    # Check if input file exists
    import os
    if not os.path.exists(args.input_file):
        print(f"❌ Input file '{args.input_file}' not found")
        sys.exit(1)
    
    # Prepare the data
    success = prepare_csv_for_timesfm(
        input_file=args.input_file,
        output_file=args.output,
        date_col=args.date_col,
        value_col=args.value_col
    )
    
    if success:
        print("\n🎉 Success! Your data is ready for TimesFM.")
    else:
        print("\n❌ Failed to prepare data. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

