import csv
from datetime import datetime, timedelta
import os

def create_sample_csv(filename='sample_large_file.csv', rows=100):
    # Create sample data with 3 columns (including createdDt)
    header = ['id', 'createdDt', 'value']
    
    # Generate dates spanning 3 days
    base_date = datetime(2023, 10, 1)
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        
        for i in range(rows):
            # Alternate dates between 3 different days
            date_offset = i % 3
            dt = base_date + timedelta(days=date_offset)
            
            # Create row data
            row = [
                i + 1,  # ID
                dt.strftime('%Y-%m-%d %H:%M:%S'),  # createdDt
                f"Value_{i}"  # Random value
            ]
            writer.writerow(row)
    
    print(f"Created sample file '{filename}' with {rows} rows")

def test_processing():
    # Create sample data (10 rows for quick testing)
    create_sample_csv('large_file.csv', rows=10)

    import sys
    sys.path.append('.')
    # print("Testing processing... sys.path:", sys.path)
    
    # Run the processing script
    from read_large_csv import process_large_file
    process_large_file()
    
    # Verify output
    output_dir = 'daily_files'
    print("\nGenerated files:")
    for fname in os.listdir(output_dir):
        if fname.startswith('daily_'):
            with open(os.path.join(output_dir, fname)) as f:
                line_count = sum(1 for line in f) - 1  # Subtract header
            print(f"{fname}: {line_count} rows")

if __name__ == '__main__':
    # Create sample file and test processing
    test_processing()
    print("\nTest complete. Check the 'daily_files' directory for results.")