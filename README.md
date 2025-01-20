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

---
### How much time should a 60 GB file need to be processed?

The time to process a 60 GB file depends heavily on **your hardware** and **data characteristics**, but here’s a structured way to estimate it:


### **Key Factors Affecting Runtime**
1. **Hardware**:
   - **Disk Speed** (SSD vs HDD):  
     - NVMe SSD: 3–5 GB/s read  
     - SATA SSD: 500 MB/s read  
     - HDD: 100–200 MB/s read  
   - **CPU**: Multi-core performance for parsing/grouping  
   - **RAM**: Sufficient memory to hold chunks (e.g., 100k rows)  

2. **Data Complexity**:
   - Number of unique dates (more dates = more file writes)  
   - Column types (string-heavy data is slower to process)  

3. **Code Workflow**:
   - `chunksize` value (larger = fewer I/O ops but more RAM usage)  
   - Grouping/writing efficiency  

---

### **Rough Performance Benchmarks**
| Hardware Profile                | Estimated Time | Notes                                  |
|----------------------------------|----------------|----------------------------------------|
| **High-End Server** (NVMe SSD, 32-core CPU, 64GB RAM) | 10–30 mins | Parallel I/O, fast CPU optimizes grouping |
| **Consumer SSD Laptop** (4-core CPU, 16GB RAM)        | 1–3 hours   | Limited by single-threaded writes       |
| **HDD Machine** (8-core CPU, 32GB RAM)                | 4–8 hours   | Bottlenecked by disk I/O                |

---

### **Breakdown of Operations**
1. **Reading the File** (60 GB):  
   - SSD: ~2–5 minutes (sequential read)  
   - HDD: ~30–60 minutes  

2. **Processing Chunks** (50M rows):  
   - Parsing + Grouping: 0.1–0.5 seconds per 100k-row chunk  
   - Total for 500 chunks: ~5–40 minutes  

3. **Writing Daily Files**:  
   - SSD: ~1–10 minutes (depends on number of daily files)  
   - HDD: ~30–60 minutes  

---

### **Optimization Levers**
1. **Increase `chunksize`**:  
   - Example: `chunksize=500_000` reduces chunk count from 500 to 100.  
   - Tradeoff: Higher RAM usage (~2–4 GB per chunk).  

2. **Use `dtype` Parameter**:  
   - Explicitly define column types to skip Pandas inference:  
     ```python
     dtype={'id': 'int32', 'value': 'category', ...}
     ```

3. **Disable Indexing**:  
   - Add `index=False` in `to_csv` to skip writing row indices.  

4. **Use Faster Storage**:  
   - Process files on an NVMe SSD or RAM disk.  

---

### **Sample Calculation for a Mid-Range SSD Machine**
Assume:
- **Read speed**: 500 MB/s → 60 GB = ~2 minutes  
- **Processing**: 0.2 seconds per 100k-row chunk (500 chunks → 100 seconds ≈ 1.7 mins)  
- **Write speed**: 200 MB/s for daily files → ~3 mins  
- **Total**: ~7 minutes (ideal) + 2x overhead ≈ **15–20 mins**.

---

### **Real-World Expectations**
- For most users with SSDs: **30–60 minutes**.  
- For HDD users: **4–10 hours**.  

---

### **Actionable Steps**
1. **Run a Test** with a 1 GB subset of your data.  
   - Multiply the runtime by 60 for a rough estimate.  
   - Example: 1 GB takes 3 mins → 60 GB ≈ 3 hours.  

2. **Monitor Resources**:  
   ```bash
   # Linux
   htop  # Watch CPU/RAM usage
   iotop # Monitor disk I/O
   ```

3. **Parallelize** (Advanced):  
   Use `concurrent.futures` to process multiple chunks in parallel if your workflow allows it.  

---

### **Final Answer**
On a modern SSD machine with 16+ GB RAM, expect **30–90 minutes**. On HDD, plan for **4–10 hours**. Always test with a small sample first!
