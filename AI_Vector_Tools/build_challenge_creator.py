import os
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def ask_questions():
    answers = {}
    questions = [
        "What subject would you like to teach?",
        "What learning outcomes would you like to see?",
        "What age range or grade would you like to teach for?",
        "How long would you like the lesson to be?"
    ]

    for question in questions:
        print(question)
        answers[question] = input()

    return answers, questions  # Return both answers and questions

async def generate_gpt_response(answers, questions):
    # Construct the prompt from the answers
    prompt = (
        "Based on the following requirements:\n"
        f"Subject: {answers[questions[0]]}\n"
        f"Learning Outcomes: {answers[questions[1]]}\n"
        f"Age Range/Grade: {answers[questions[2]]}\n"
        f"Lesson Duration: {answers[questions[3]]}\n"
        "Generate a Minecraft Education build challenge that includes:\n"
        "a) A build challenge prompt for the students.\n"
        "b) An explanation of the build that the teacher can expect to see.\n"
        "c) Some ideas for assessment for that build challenge."
    )

    # Use the async client to create a chat completion
    completion = await client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use the latest available model suitable for your task
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    # Accessing the text of the last completion choice
    return completion.choices[-1].message.content.strip()  # Adjusted for the new response object structure

async def main():
    # Convert ask_questions to be called in an asyncio event loop
    loop = asyncio.get_running_loop()
    answers, questions = await loop.run_in_executor(None, ask_questions)
    
    response = await generate_gpt_response(answers, questions)
    print("\nGenerated Build Challenge and Assessment Ideas:")
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
