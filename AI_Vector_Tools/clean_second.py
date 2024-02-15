import pandas as pd

# Load the cleaned dataset
file_path = 'C:/Users/juedwards/Downloads/EG_Minecraft/Cleaned_Merged_Minecraft_Dataset.csv'
df = pd.read_csv(file_path)

# Remove "ID" and "Resource_Type" columns
df = df.drop(['ID', 'Resource_Type'], axis=1)

# Reorder columns to place "World Name" as the second column and "URL" as the third
cols = ['UUID', 'World_Name', 'URL'] + [col for col in df.columns if col not in ['UUID', 'World_Name', 'URL']]
df = df[cols]

# Save the updated dataset to a new CSV file
output_path = 'C:/Users/juedwards/Downloads/EG_Minecraft/Final_Cleaned_Minecraft_Dataset.csv'
df.to_csv(output_path, index=False)

print(f'Final cleaned dataset saved to {output_path}')
