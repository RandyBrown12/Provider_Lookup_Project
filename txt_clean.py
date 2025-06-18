import pandas as pd

# Step 1: Extract header from sample
header_sample = pd.read_excel('nctest1.xlsx', nrows=0)
column_names = header_sample.columns.tolist()

# Step 2: Define your columns to keep
columns_to_keep = [
    'NPI',
    'Provider Organization Name (Legal Business Name)',
    'Provider Last Name (Legal Name)',
    'Provider First Name',
    'Provider First Line Business Mailing Address',
    'Provider Business Mailing Address City Name',
    'Provider Business Mailing Address State Name',
    'Provider Business Mailing Address Postal Code',
    'Provider Business Mailing Address Telephone Number'
] + [f'Healthcare Provider Taxonomy Code_{i}' for i in range(1, 16)]

input_txt = 'npi_nc.txt'
output_csv = 'npi_nc_cleaned.csv'
chunk_size = 100000
header_written = False

# Step 3: Read and process without header in the txt, set column names manually
for chunk in pd.read_csv(
        input_txt,
        sep='|',
        dtype=str,
        header=None,                # no header in txt
        names=column_names,         # assign column names from sample
        chunksize=chunk_size,
        keep_default_na=False,
        encoding='latin-1'
    ):
    # Only keep the columns we want
    chunk = chunk[[c for c in columns_to_keep if c in chunk.columns]]
    # Fill blanks with 'no data'
    chunk = chunk.applymap(lambda x: 'no data' if (pd.isna(x) or str(x).strip() == '') else str(x).strip())
    # Write header only for first chunk
    if not header_written:
        chunk.to_csv(output_csv, index=False, mode='w')
        header_written = True
    else:
        chunk.to_csv(output_csv, index=False, mode='a', header=False)
    print("Processed chunk")

print("Done! Cleaned file ready:", output_csv)

