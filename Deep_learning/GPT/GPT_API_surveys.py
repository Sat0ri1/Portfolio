from openai import OpenAI

def generate_survey_openai(user_category, user_subcategories, num_questions_to_generate):
    client = OpenAI()

    # Build the conversation for the chat-based model
    conversation = [
        {"role": "system", "content": "You are a survey generator assistant."},
        {"role": "user", "content": f"Generate a survey with {num_questions_to_generate} questions about {user_category} with subcategories: {', '.join(user_subcategories)}"}
    ]

    # Call the OpenAI API for chat completions
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
    )

    # Extract and print the generated question
    generated_question = completion.choices[0].message.content

    print(f"Generated Question: {generated_question}")

# Example usage:
user_category = input("Enter the category: ")
user_subcategories = input("Enter subcategories separated by commas: ").split(",")
num_questions_to_generate = int(input("Enter the number of questions in the survey:"))

# Generate and print the survey question
generate_survey_openai(user_category, user_subcategories, num_questions_to_generate)
