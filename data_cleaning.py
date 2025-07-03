import pandas as pd

# === SETTINGS ===
input_csv = 'npidata_pfile_20050523-20250608.csv'
nucc_csv = 'nucc_taxonomy_250.csv'

output1 = 'npidata_cleaned.csv'
output2 = 'nucc_taxonomy_processed.csv'
output3 = 'npi_taxonomy_codes.csv'

# --- Step 1: Read and clean master data ---
chunk_size = 100000
columns_to_keep = [
    'NPI',
    'Provider Organization Name (Legal Business Name)',
    'Provider Last Name (Legal Name)',
    'Provider First Name',
    'Provider First Line Business Practice Location Address',
    'Provider Second Line Business Practice Location Address',
    'Provider Business Practice Location Address City Name',
    'Provider Business Practice Location Address State Name',
    'Provider Business Practice Location Address Postal Code',
    'Provider Business Practice Location Address Telephone Number'
] + [f'Healthcare Provider Taxonomy Code_{i}' for i in range(1, 16)]

chunks = []
for chunk in pd.read_csv(input_csv, dtype=str, chunksize=chunk_size, keep_default_na=False, encoding='latin-1'):
    chunk = chunk[[c for c in columns_to_keep if c in chunk.columns]]
    chunk = chunk.applymap(lambda x: 'no data' if (pd.isna(x) or str(x).strip() == '') else str(x).strip())
    chunks.append(chunk)
df_master = pd.concat(chunks, ignore_index=True)
df_master = df_master.drop_duplicates(subset=['NPI']).reset_index(drop=True)
print(f"Loaded {len(df_master)} distinct NPI numbers from main file.")

# --- Step 2: File 1 (npidata_cleaned.csv) ---
df_file1 = df_master.copy()
df_file1.to_csv(output1, index=False)

# --- Step 3: File 3 (npi_taxonomy_codes.csv, LONG format) ---
taxonomy_cols = [f'Healthcare Provider Taxonomy Code_{i}' for i in range(1, 16)]

# Melt taxonomy columns into rows
npi_taxonomy_pairs = (
    df_master.melt(id_vars=['NPI'], value_vars=taxonomy_cols, var_name='taxonomy_col', value_name='taxonomy_code')
    .dropna(subset=['taxonomy_code'])
)
# Remove blanks or 'no data'
npi_taxonomy_pairs = npi_taxonomy_pairs[npi_taxonomy_pairs['taxonomy_code'].str.lower() != 'no data']
npi_taxonomy_pairs = npi_taxonomy_pairs[npi_taxonomy_pairs['taxonomy_code'].str.strip() != '']
npi_taxonomy_pairs = npi_taxonomy_pairs[['NPI', 'taxonomy_code']].drop_duplicates()
npi_taxonomy_pairs.to_csv(output3, index=False)
print("File 3 ready (NPI-taxonomy long format):", output3)

# --- Step 4: File 2 (nucc_taxonomy_processed.csv, Code + Specialization only) ---
nucc = pd.read_csv(nucc_csv, dtype=str, keep_default_na=False, encoding='latin-1')
# Find the actual column names in NUCC file (case-insensitive)
code_col = [col for col in nucc.columns if col.strip().lower() == 'code'][0]
spec_col = [col for col in nucc.columns if 'specialization' in col.lower()][0]
columns_nucc_keep = [code_col, spec_col]
df_file2 = nucc[columns_nucc_keep].copy()
df_file2 = df_file2.applymap(lambda x: 'no data' if (pd.isna(x) or str(x).strip() == '') else str(x).strip())
df_file2.to_csv(output2, index=False)
print("File 2 ready (Code + Specialization):", output2)

# --- Step 5: Show max length for each column and append as last row ---

def append_max_length_row(filename):
    df = pd.read_csv(filename, dtype=str, keep_default_na=False, encoding='latin-1')
    maxlen = {col: df[col].astype(str).map(len).max() for col in df.columns}
    print(f"\nMax length in '{filename}':")
    for col, l in maxlen.items():
        print(f"  {col}: {l}")
    # Add summary row at end
    summary_row = [str(maxlen[col]) for col in df.columns]
    df.loc[len(df)] = summary_row
    df.to_csv(filename, index=False)

append_max_length_row(output1)
append_max_length_row(output2)
append_max_length_row(output3)
