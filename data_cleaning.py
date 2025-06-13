import pandas as pd

input_csv = 'npidata_pfile_20050523-20250608.csv'    # Original file
output_csv = 'npidata_cleaned.csv'                   # Cleaned file
chunk_size = 100000

# List of columns you want to keep (edit as needed)
columns_to_keep = [
    'NPI',
    'Provider First Name',
    'Provider Last Name (Legal Name)',
    'Provider Credential Text',
    'Provider Business Mailing Address Telephone Number',
    'Provider First Line Business Mailing Address',
    'Provider Second Line Business Mailing Address',
    'Provider Business Mailing Address City Name',
    'Provider Business Mailing Address State Name',
    'Provider Business Mailing Address Postal Code'
]

header_written = False

for chunk in pd.read_csv(input_csv, dtype=str, chunksize=chunk_size, keep_default_na=False, encoding='latin-1'):
    # Only keep the columns we care about (drop everything else)
    chunk = chunk[[c for c in columns_to_keep if c in chunk.columns]]
    # Fill blanks with 'no data'
    chunk = chunk.applymap(lambda x: 'no data' if (pd.isna(x) or str(x).strip() == '') else str(x).strip())
    # Write header only for the first chunk
    if not header_written:
        chunk.to_csv(output_csv, index=False, mode='w')
        header_written = True
    else:
        chunk.to_csv(output_csv, index=False, mode='a', header=False)
    print("Processed chunk")

print("Done! Cleaned file ready:", output_csv)

