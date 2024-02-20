import pandas as pd
import requests

# Load the dataset
file_path = 'C:/Users/juedwards/Downloads/EG_Minecraft/Final_Cleaned_Minecraft_Dataset.csv'
df = pd.read_csv(file_path)

# Function to check if the Minecraft world exists
def check_minecraft_world(uuid):
    url = f"https://education.minecraft.net/world/{uuid}"
    response = requests.get(url)
    final_url = response.url
    return final_url.endswith("?loaded=yes"), final_url if final_url.endswith("?loaded=yes") else ""

# Check each UUID and update the DataFrame
df['Minecraft World Exists'] = False
df['Minecraft World URL'] = ""

for index, row in df.iterrows():
    print(f"Checking UUID: {row['UUID']}")  # Print the UUID being checked
    exists, world_url = check_minecraft_world(row['UUID'])
    df.at[index, 'Minecraft World Exists'] = exists
    if exists:
        df.at[index, 'Minecraft World URL'] = world_url
        print(f"Minecraft world exists for UUID {row['UUID']}. URL: {world_url}")
    else:
        print(f"No Minecraft world found for UUID {row['UUID']}.")

# Save the updated dataset
output_path = 'C:/Users/juedwards/Downloads/EG_Minecraft/Updated_Minecraft_Dataset.csv'
df.to_csv(output_path, index=False)

print(f'Updated dataset saved to {output_path}')
