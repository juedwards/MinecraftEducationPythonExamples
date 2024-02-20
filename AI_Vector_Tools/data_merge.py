import pandas as pd

# Define file paths
metadata_path = 'C:/Users/juedwards/Downloads/EG_Minecraft/EG_MetaData_Minecraft.txt'
learning_object_path = 'C:/Users/juedwards/Downloads/EG_Minecraft/EG_Learning-Object_Minecraft.txt'

# Load the metadata dataset
metadata_df = pd.read_csv(metadata_path, delimiter='\t', header=None, names=['UUID', 'Resource_Type', 'Name', 'Description', 'Subjects'])

# Identify unique categories from the 'Name' column
unique_categories = set()
metadata_df['Name'].dropna().str.split(',').apply(lambda x: unique_categories.update(x))

# Function to process the 'Name' column and create new columns for each category
def process_name_column(row):
    for category in unique_categories:
        row[category] = category in row['Name']
    return row

# Process each row to create new columns for categories
metadata_df = metadata_df.apply(process_name_column, axis=1)

# Drop the original 'Name' column if no longer needed
# metadata_df.drop(columns=['Name'], inplace=True)

# Load the learning-object dataset
learning_object_df = pd.read_csv(learning_object_path, delimiter='\t', header=None, names=['UUID', 'Code', 'World_Name', 'URL', 'Learning_Description', 'Grades', 'ID'])

# Merging the datasets on 'UUID'
merged_df = pd.merge(metadata_df, learning_object_df, on='UUID', how='inner')

# Saving the merged dataset to a new CSV file
output_path = 'C:/Users/juedwards/Downloads/EG_Minecraft/Merged_Processed_Minecraft_Dataset.csv'
merged_df.to_csv(output_path, index=False)

print(f'Merged and processed dataset saved to {output_path}')
