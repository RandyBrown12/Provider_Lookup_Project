import pandas as pd
import os
import glob

def clean_csv_file(input_path, output_path, chunk_size=100000):
    # Read and process in chunks for large files
    reader = pd.read_csv(input_path, chunksize=chunk_size, dtype=str, keep_default_na=False)
    with open(output_path, 'w', encoding='utf-8', newline='') as f_out:
        first_chunk = True
        for chunk in reader:
            # Replace blanks, NaN, or only whitespace with 'no data'
            chunk = chunk.applymap(lambda x: 'no data' if (pd.isna(x) or str(x).strip() == '') else str(x).strip())
            # Write header only for the first chunk
            chunk.to_csv(f_out, index=False, header=first_chunk)
            first_chunk = False

def clean_all_csvs(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    csv_files = glob.glob(os.path.join(input_folder, '*.csv'))
    print(f"Found {len(csv_files)} CSV files to process.")
    for file in csv_files:
        filename = os.path.basename(file)
        output_path = os.path.join(output_folder, filename)
        print(f"Cleaning {filename} ...")
        clean_csv_file(file, output_path)
        print(f"Saved cleaned file to {output_path}")

if __name__ == "__main__":
    # Set your input and output folders here
    input_folder = './Original_data'     # Folder where your CSVs are stored
    output_folder = './Clean_data'  # Folder to save cleaned CSVs

    clean_all_csvs(input_folder, output_folder)
    print("All files cleaned!")
