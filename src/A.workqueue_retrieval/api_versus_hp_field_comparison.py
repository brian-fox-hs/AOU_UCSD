import pandas as pd
import numpy as np

def infer_format(series):
    """Infer the format of a given column based on the data types."""
    if pd.api.types.is_integer_dtype(series):
        return "Integer"
    elif pd.api.types.is_float_dtype(series):
        return "Float"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "Datetime"
    elif pd.api.types.is_object_dtype(series):
        return "Text/String"
    else:
        return "Unknown"

def compare_csv_files(file1, file2):
    """Compare field names and formats of two CSV files."""
    df1 = pd.read_csv(file1, dtype=str, on_bad_lines='skip')
    df2 = pd.read_csv(file2, dtype=str, on_bad_lines='skip')

    fields1 = set(df1.columns)
    fields2 = set(df2.columns)

    common_fields = fields1 & fields2
    only_in_file1 = fields1 - fields2
    only_in_file2 = fields2 - fields1

    print("Field Comparison Report")
    print("="*50)

    print("\nFields only in File 1:")
    for field in only_in_file1:
        print(f"  - {field}")

    print("\nFields only in File 2:")
    for field in only_in_file2:
        print(f"  - {field}")

    print("\nComparing Common Fields:")
    for field in common_fields:
        print(f"\nField: {field}")

        try:
            df1_sample = pd.to_numeric(df1[field], errors='coerce')
            df2_sample = pd.to_numeric(df2[field], errors='coerce')

            format1 = infer_format(df1_sample) if not df1_sample.isna().all() else "Text/String"
            format2 = infer_format(df2_sample) if not df2_sample.isna().all() else "Text/String"

            if format1 != format2:
                print(f"  - Format Mismatch: {file1}: {format1}, {file2}: {format2}")
            else:
                print(f"  - Format Match: {format1}")

        except Exception as e:
            print(f"  - Could not determine format: {e}")

        # Show examples if format is unclear
        print(f"  - Sample values from {file1}: {df1[field].dropna().unique()[:3]}")
        print(f"  - Sample values from {file2}: {df2[field].dropna().unique()[:3]}")

if __name__ == "__main__":
    file1 = "hp_example2.csv"
    file2 = "api_example2.csv"
    compare_csv_files(file1, file2)
