from pathlib import Path
import pandas as pd
def clean_data(input_file: str,output: str) -> pd.Dataframe:
  """Load a CSV file, remove duplicates, and save cleaned data."""
  input path = Path(input-file)
  output_path = Path(output_file)
  if not input_path.exists():
    raise File NotFoundError(f"inputfile not found: {input_path}")
    df=pd.read_csv(input_path)
    #remove duplicate rows
    df = df.drop_duplicates()
    #Standardise Column names
    df. columns =(df.columns.str.strip()
    .str.lower()
    .str.replace(" ","_"))
    #remove rows that are completely empty
    df= df.dropna(how="all")
    output_path parent.mkdir(parents=True, exist_ok=True)
    df.to csv(output_path, index=False)
    print(f"Cleaned data saved to:"{output path}")
    print(f"Rows remaining: {len(df)}")

    return df
    if_name_=="-main_":
    print("Instamart data cleaning module is ready.")
    print ("Next, connect it to the assessment's synthetic dataset.")
