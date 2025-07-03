import pandas as pd

# Load column names from sample header (xlsx)
header_sample = pd.read_excel('nctest1.xlsx', nrows=0)
column_names = header_sample.columns.tolist()

# Define columns to keep for PRACTICE address
columns_to_keep = [
    'NPI',
    'Provider Organization Name (Legal Business Name)',
    'Provider Last Name (Legal Name)',
    'Provider First Name',
    'Provider First Line Business Practice Location Address',
    'Provider Business Practice Location Address City Name',
    'Provider Business Practice Location Address State Name',
    'Provider Business Practice Location Address Postal Code',
    'Provider Business Practice Location Address Telephone Number'
] + [f'Healthcare Provider Taxonomy Code_{i}' for i in range(1, 16)]

input_txt = 'npi_nc.txt'
output_csv = 'npi_nc_cleaned_practice.csv'
chunk_size = 100000
header_written = False

for chunk in pd.read_csv(
        input_txt,
        sep='|',
        dtype=str,
        header=None,
        names=column_names,
        chunksize=chunk_size,
        keep_default_na=False,
        encoding='latin-1'
    ):
    # Keep only practice address & wanted columns
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

print("Done! Cleaned practice address file ready:", output_csv)
