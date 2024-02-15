import pandas as pd
import os

# Load the CSV file
file_path = r"C:\Users\juedwards\Downloads\Final_Cleaned_Minecraft_Dataset2.csv"  # Change this to your file's path
data = pd.read_csv(file_path)

# Function to clean column names (optional, for handling leading/trailing spaces)
def clean_column_names(df):
    df.columns = df.columns.str.strip()
    return df

# Clean the column names
data = clean_column_names(data)

# Merge duplicate columns if necessary
# This step depends on your data and how you want to handle duplicates.
# For example, if 'Science' and 'Science ' are duplicates, you might want to merge them:
if 'Science' in data.columns and 'Science ' in data.columns:  # Adjust according to actual column names
    data['Science'] = data[['Science', 'Science ']].max(axis=1)
    data.drop(columns='Science ', inplace=True)  # Drop the duplicate column

# Drop exact duplicate rows
data = data.drop_duplicates()

# Split the directory and the filename
directory, filename = os.path.split(file_path)

# Prefix 'cleaned_' to the filename
cleaned_filename = 'cleaned_' + filename

# Combine the directory with the new filename to get the cleaned file path
cleaned_file_path = os.path.join(directory, cleaned_filename)

# Now save the cleaned data
data.to_csv(cleaned_file_path, index=False)

print(f"Cleaned data saved to {cleaned_file_path}")
