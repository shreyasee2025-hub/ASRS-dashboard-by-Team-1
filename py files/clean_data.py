import os, glob
import pandas as pd

# script lives in a subfolder (e.g. "py files/")
# project root is always one level up from the script
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Exact values from ASRS Coding Taxonomy PDF (page 4)
CLEAN_PHASES = [
    'Parked',
    'Taxi',
    'Takeoff',           # taxonomy: "Takeoff" (not "Takeoff / Launch")
    'Initial Climb',
    'Climb',
    'Cruise',
    'Descent',
    'Initial Approach',
    'Final Approach',
    'Landing',
]

# ── Load data ─────────────────────────────────────────────────────────────
print("Loading ASRS data...")

df = None

# Updated path to your raw data folder
raw_data_path = os.path.join(PROJECT_ROOT, "data", "raw")

if os.path.exists(raw_data_path):
    print(f"  Reading from raw folder: {raw_data_path}")
    
    # Check if it's a single parquet file
    parquet_files = glob.glob(os.path.join(raw_data_path, "*.parquet"))
    
    if len(parquet_files) == 1:
        # Single parquet file
        print(f"  Reading single parquet file: {parquet_files[0]}")
        df = pd.read_parquet(parquet_files[0])
    elif len(parquet_files) > 1:
        # Multiple parquet files - concatenate them
        print(f"  Found {len(parquet_files)} parquet files, concatenating...")
        chunks = []
        for file in parquet_files:
            try:
                chunk = pd.read_parquet(file)
                chunks.append(chunk)
                print(f"  Loaded {len(chunk)} rows from {os.path.basename(file)}")
            except Exception as e:
                print(f"  Error reading {file}: {e}")
        if chunks:
            df = pd.concat(chunks, ignore_index=True)
    else:
        # Check for subdirectories with parquet files
        subdirs = [d for d in os.listdir(raw_data_path) if os.path.isdir(os.path.join(raw_data_path, d))]
        if subdirs:
            print(f"  Found subdirectories: {subdirs}")
            # Try to read from first subdirectory
            subdir_path = os.path.join(raw_data_path, subdirs[0])
            parquet_files = glob.glob(os.path.join(subdir_path, "*.parquet"))
            if parquet_files:
                chunks = []
                for file in parquet_files:
                    try:
                        chunk = pd.read_parquet(file)
                        chunks.append(chunk)
                        print(f"  Loaded {len(chunk)} rows from {os.path.basename(file)}")
                    except Exception as e:
                        print(f"  Error reading {file}: {e}")
                if chunks:
                    df = pd.concat(chunks, ignore_index=True)
else:
    print("ERROR: Raw data folder not found at:", raw_data_path)
    exit(1)

print(f"  Loaded {len(df):,} rows, {len(df.columns)} columns")

# ── Rename using exact column names from README ───────────────
col_map = {
    '__ACN':                                            'ACN',
    'Time__Date':                                       'Date',
    'Time__Local_Time_Of_Day':                          'Time_Of_Day',
    'Place__State_Reference':                           'State',
    'Place__Locale_Reference':                          'Airport',
    'Environment__Flight_Conditions':                   'Flight_Conditions',
    'Environment__Light':                               'Light',
    'Aircraft_1__Flight_Phase':                         'Flight_Phase',
    'Aircraft_1__Aircraft_Operator':                    'Operator',
    'Aircraft_1__Make_Model_Name':                      'Aircraft_Model',
    'Person_1__Human_Factors':                          'Human_Factors',
    'Person_1__Communication_Breakdown':                'Communication_Breakdown_Raw',
    'Events__Anomaly':                                  'Anomaly',
    'Assessments__Primary_Problem':                     'Primary_Problem',
    'Assessments__Contributing_Factors_And_Situations': 'Contributing_Factors',
    'Report_1__Narrative':                              'Narrative',
    'Report_1__Synopsis':                               'Synopsis',
}

df = df.rename(columns=col_map)
keep = [c for c in col_map.values() if c in df.columns]
missing = [c for c in col_map.values() if c not in df.columns]
if missing:
    print(f"  Warning: these expected columns were not found: {missing}")

df = df[keep]

# ── Year and Month from Date field (YYYYMM string e.g. "200001") ────
df['Date']  = df['Date'].astype(str).str.strip()
df['Year']  = pd.to_numeric(df['Date'].str[:4], errors='coerce').astype('Int64')
df['Month'] = pd.to_numeric(df['Date'].str[4:6], errors='coerce').astype('Int64')

# Filter for years 2000-2018 (2019 data is incomplete - only January captured)
df = df[df['Year'].between(2000, 2018)]
print(f"After year filter (2000-2018): {len(df):,} rows")

# ── Time of day ──────────────────────────
time_map = {
    '0001-0600': 'Late Night',
    '0601-1200': 'Morning',
    '1201-1800': 'Afternoon',
    '1801-2400': 'Evening'
}
df['Time_Of_Day'] = df['Time_Of_Day'].map(time_map).fillna('Unknown')

# ── Flight phase — keep only clean single-phase values ────
df = df[df['Flight_Phase'].isin(CLEAN_PHASES)]
df = df.dropna(subset=['Primary_Problem', 'Flight_Phase'])
print(f"After phase/problem filter: {len(df):,} rows")

# ── Human factor binary flags ─────────────────────────
for hf in ['Fatigue', 'Distraction', 'Workload', 'Situational Awareness', 'Communication Breakdown']:
    col = 'HF_' + hf.replace(' ', '_')
    df[col] = df['Human_Factors'].str.contains(hf, case=False, na=False).astype(int)

# ── Deduplicate ──────────────────────────
before = len(df)
df = df.drop_duplicates(subset=['ACN'])
removed = before - len(df)
if removed:
    print(f"Removed {removed:,} duplicate ACNs")

# ── Save ──────────────────────────────────
os.makedirs(os.path.join(PROJECT_ROOT, 'data', 'processed'), exist_ok=True)
out_path = os.path.join(PROJECT_ROOT, 'data', 'processed', 'asrs_clean.parquet')
df.to_parquet(out_path, index=False)
print(f"\nSaved {len(df):,} rows → {out_path}")
print("Done. Run:  streamlit run app.py")
