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
    
    # Get existing processed dates
    existing_dates = set()
    for filename in os.listdir(output_dir):
        if filename.startswith(file_prefix) and filename.endswith('.csv'):
            date_str = filename[len(file_prefix):-4]
            existing_dates.add(date_str)
    
    # Process file in chunks
    for chunk_idx, chunk in enumerate(pd.read_csv(
        input_file,
        chunksize=chunksize,
        parse_dates=[date_column],
        infer_datetime_format=True,
        low_memory=False
    )):
        print(f"Processing chunk {chunk_idx + 1}")
        
        # Group by date
        grouped = chunk.groupby(pd.Grouper(key=date_column, freq='D'))
        
        # Process each daily group
        for date, group in grouped:
            if group.empty:
                continue
                
            date_str = date.strftime('%Y-%m-%d')
            output_path = os.path.join(output_dir, f'{file_prefix}{date_str}.csv')
            
            # Determine write mode and header
            if date_str in existing_dates:
                mode = 'a'
                header = False
            else:
                mode = 'a' if os.path.exists(output_path) else 'w'
                header = not os.path.exists(output_path)
                existing_dates.add(date_str)
            
            # Write to file
            group.to_csv(
                output_path,
                mode=mode,
                header=header,
                index=False,
                date_format='%Y-%m-%d %H:%M:%S'  # Keep original datetime format
            )

if __name__ == '__main__':
    process_large_file()