import pandas as pd
import os
from datetime import datetime

def process_large_file():
    # Configuration
    input_file = 'large_file.csv'
    output_dir = 'daily_files'
    date_column = 'createdDt'
    chunksize = 100000  # Adjust based on your system's memory
    file_prefix = 'daily_'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Track COMPLETELY processed dates (initial existing + newly completed)
    processed_dates = set()
    
    # 1. Check existing COMPLETED dates (only trust fully written files)
    for filename in os.listdir(output_dir):
        if filename.startswith(file_prefix) and filename.endswith('.csv'):
            date_str = filename[len(file_prefix):-4]
            processed_dates.add(date_str)
    
    # 2. Process file in chunks
    for chunk in pd.read_csv(
        input_file,
        chunksize=chunksize,
        parse_dates=[date_column],
        infer_datetime_format=True,
        low_memory=False
    ):
        # 3. Filter out already processed dates BEFORE grouping
        chunk = chunk[~chunk[date_column].dt.strftime('%Y-%m-%d').isin(processed_dates)]
        
        if chunk.empty:
            continue
            
        # 4. Group remaining dates
        grouped = chunk.groupby(pd.Grouper(key=date_column, freq='D'))
        
        # 5. Process new dates
        for date, group in grouped:
            if group.empty:
                continue
                
            date_str = date.strftime('%Y-%m-%d')
            output_path = os.path.join(output_dir, f'{file_prefix}{date_str}.csv')
            
            # 6. Check for concurrent completion
            if date_str in processed_dates:
                continue  # Skip if another chunk already processed this date
                
            # 7. Write with atomic completion check
            if not os.path.exists(output_path):
                # First write: create file with header
                group.to_csv(output_path, index=False)
                processed_dates.add(date_str)  # Mark as completed
            else:
                # Safety check: if file exists but not tracked, skip to prevent corruption
                continue

if __name__ == '__main__':
    process_large_file()