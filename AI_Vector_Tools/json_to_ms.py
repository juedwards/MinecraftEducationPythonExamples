import json
import os

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def create_md_content(entry):
    md_content = f"# {entry['UUID']}\n## {entry['World_Name']}\n\n"
    for key, value in entry.items():
        md_content += f"### {key}\n{value}\n\n"
    return md_content

def save_md_files(data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for entry in data:
        md_content = create_md_content(entry)
        safe_world_name = entry['World_Name'].replace(' ', '_').translate({ord(c): '' for c in '/\\:*?"<>|'})
        file_name = f"{safe_world_name}.md"
        with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as md_file:
            md_file.write(md_content)

def main():
    input_file = r"C:\Users\juedwards\Downloads\cleaned_Final_Cleaned_Minecraft_Dataset2.json"  # Update this to your JSON file path
    output_dir = os.path.dirname(input_file) + '/MD_files'  # Save MD files in the same directory as the JSON file
    data = load_json(input_file)
    save_md_files(data, output_dir)

if __name__ == "__main__":
    main()
