import os
import asyncio
import pandas as pd
from openai import AsyncOpenAI
import os

client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

async def generate_gpt_response(subject, learning_outcomes, age_range, lesson_duration):
    prompt = (
        "Based on the following requirements:\n"
        f"Subject: {subject}\n"
        f"Learning Outcomes: {learning_outcomes}\n"
        f"Age Range/Grade: {age_range}\n"
        f"Lesson Duration: {lesson_duration}\n"
        "Generate a Minecraft Education build challenge that includes:\n"
        "a) A build challenge prompt for the students.\n"
        "b) An explanation of the build that the teacher can expect to see.\n"
        "c) Some ideas for assessment for that build challenge."
    )

    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[-1].message.content.strip()

def safe_filename(filename):
    """Generate a safe filename by removing or replacing invalid characters."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '-')
    return filename[:200]  # Limit the filename length to 200 characters for compatibility

async def process_and_save_response(row, base_dir):
    response = await generate_gpt_response(row['Subject'], row['LearningOutcomes'], row['AgeRange'], row['LessonLength'])
    
    # Format the Markdown content
    markdown_content = f"# Minecraft Mini Build Challenge\n\n" \
                       f"**Subject:** {row['Subject']}\n\n" \
                       f"**Learning Outcomes:** {row['LearningOutcomes']}\n\n" \
                       f"**Age Range:** {row['AgeRange']}\n\n" \
                       f"**Lesson Duration:** {row['LessonLength']}\n\n" \
                       "---\n\n" \
                       f"{response}"
    
    # Use the subject as the filename (or modify as needed to ensure uniqueness)
    filename = safe_filename(row['Subject']) + ".md"
    filepath = os.path.join(base_dir, filename)
    
    # Save the formatted content to a Markdown file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(markdown_content)

    print(f"Saved response to {filepath}")

async def main():
    csv_file_path = os.path.expanduser("~/Downloads/101ways.csv")
    df = pd.read_csv(csv_file_path)

    # Determine the base directory from the CSV file path
    base_dir = os.path.dirname(csv_file_path)

    # Process and save responses for each row
    tasks = [process_and_save_response(row, base_dir) for _, row in df.iterrows()]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
