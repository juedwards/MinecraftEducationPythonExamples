import pandas as pd
import re

# Load the merged dataset
file_path = 'C:/Users/juedwards/Downloads/EG_Minecraft/Merged_Processed_Minecraft_Dataset.csv'
df = pd.read_csv(file_path)

# Task 1: Convert "World Name" to Capital Case and remove non-alphanumeric characters
df['World_Name'] = df['World_Name'].apply(lambda x: ' '.join(re.sub(r'[^A-Za-z0-9 ]', '', word).capitalize() for word in str(x).split()))

# Task 2: Separate "Grades" into individual columns with True/False indicators
grades = df['Grades'].str.get_dummies(sep=',')
grades = grades.rename(lambda x: x.strip(), axis='columns')  # Remove any leading/trailing spaces from column names
grades = grades.astype(bool)  # Convert to boolean values

# Task 3: Remove "Name", "Description", and "Subjects" columns
df = df.drop(['Name', 'Description', 'Subjects'], axis=1)

# Merge the processed "Grades" columns back into the dataframe
df_cleaned = pd.concat([df, grades], axis=1)

# Save the cleaned dataset to a new CSV file
output_path = 'C:/Users/juedwards/Downloads/EG_Minecraft/Cleaned_Merged_Minecraft_Dataset.csv'
df_cleaned.to_csv(output_path, index=False)

print(f'Cleaned dataset saved to {output_path}')
