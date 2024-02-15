import pandas as pd
import os

# Specify the path to your cleaned CSV file
csv_file_path = r"C:\Users\juedwards\Downloads\cleaned_Final_Cleaned_Minecraft_Dataset2.csv"

# Read the CSV file into a pandas DataFrame
data = pd.read_csv(csv_file_path)

# Convert the DataFrame to JSON format
# orient='records' creates a JSON array of objects, each object representing a row in the DataFrame
json_data = data.to_json(orient='records')

# Specify the path for the output JSON file
# This uses the same directory as the CSV file but changes the extension to .json
json_file_path = os.path.splitext(csv_file_path)[0] + '.json'

# Write the JSON data to a file
with open(json_file_path, 'w') as json_file:
    json_file.write(json_data)

print(f"JSON data saved to {json_file_path}")
