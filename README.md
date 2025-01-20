# read-large-file

A Python script for efficiently processing large CSV files with built-in resumability and memory optimization.

## Features

### 1. Memory Efficiency
- Uses pandas' `chunksize` parameter to read the file in smaller chunks (default: 100,000 rows)
- Implements `low_memory=False` for safer data type inference
- Processes data in streams rather than loading the entire file into memory
- Memory usage can be adjusted by modifying the `chunksize` parameter

### 2. Resumability
- Implements a robust checkpoint system using file-based tracking
- Maintains a set of processed dates to avoid reprocessing
- Can safely resume from interruptions without data duplication
- Atomic write operations prevent data corruption

### 3. Data Organization
- Groups data by daily intervals using pandas' `Grouper`
- Creates separate CSV files for each date
- Maintains original data structure within daily files
- Organized output in a dedicated directory structure

### 4. Safety Features
- Atomic file operations to prevent data corruption
- Concurrent processing safety checks
- Creates output directory if it doesn't exist
- Validates file completion before marking as processed

## How to Run

### Production Usage
1. Place your input CSV file (named 'large_file.csv') in the script directory
2. Ensure your CSV has a date column named 'createdDt'
3. Run the script:
```bash
python read_large_csv.py
```

### Testing with Sample Data
The project includes a test script (`main.py`) that helps you verify the functionality:

1. Run the test script:
```bash
python main.py
```

This will:
- Generate a sample CSV file with test data spanning 3 days
- Process the sample file using `read_large_csv.py`
- Display the results showing the number of rows in each daily file

The test script provides:
- Sample data generation with configurable row count
- Automatic testing of the processing pipeline
- Verification of output files and row counts
- Easy way to understand the expected input/output format

## Configuration Options

You can modify these variables in the script:
- `input_file`: Name of your input CSV file (default: 'large_file.csv')
- `output_dir`: Directory for output files (default: 'daily_files')
- `date_column`: Name of the date column (default: 'createdDt')
- `chunksize`: Number of rows to process at once (default: 100000)
- `file_prefix`: Prefix for output files (default: 'daily_')

For testing, you can modify in `main.py`:
- `rows`: Number of sample rows to generate (default: 10 for testing)
- `base_date`: Starting date for sample data (default: 2023-10-01)

## Performance Considerations

### Pros
- Low memory footprint due to chunk-based processing
- Efficient for very large files that don't fit in memory
- Built-in resumability saves time on interruptions
- Safe for concurrent operations
- Organized output structure
- Includes test suite for verification

### Cons
- Slightly slower than full memory processing due to chunk-based approach
- Requires additional disk space for output files
- Date-based grouping might not suit all use cases
- All rows must have valid date values in the date column