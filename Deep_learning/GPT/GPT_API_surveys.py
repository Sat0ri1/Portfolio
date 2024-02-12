import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
import numpy as np
import random

# Define categories and subcategories
categories = ["Mental Health", "Physical Health", "Social Life", "Wealthness"]

subcategories = {
    "Mental Health": ["Emotional Well-being", "Self-Esteem", "Mental Resilience"],
    "Physical Health": ["Quality of Sleep", "Genetic Diseases", "Other Serious Diseases", "Resistance to Regular Diseases", "Sports"],
    "Wealthness": ["Actual Earnings", "Possessions"],
    "Social Life": ["Social Status", "Meetings", "Meaningful Relations"],
}

# Define questions for each subcategory
questions = {
    "Emotional Well-being": [
        "How does practicing gratitude contribute to emotional well-being?",
        "Discuss the impact of positive affirmations on one's mood.",
        "What role does self-expression play in emotional health?",
    ],
    "Self-Esteem": [
        "How can setting and achieving personal goals boost self-esteem?",
        "Discuss the relationship between self-compassion and self-esteem.",
        "What are effective strategies for overcoming self-doubt?",
    ],
    "Mental Resilience": [
        "How can individuals develop resilience in the face of adversity?",
        "Discuss the importance of problem-solving skills for mental resilience.",
        "What role does social support play in building mental toughness?",
    ],
    "Quality of Sleep": [
        "How can a consistent sleep schedule improve overall health?",
        "Discuss the impact of technology on sleep quality.",
        "What are effective bedtime routines for better sleep?",
    ],
    "Genetic Diseases": [
        "Explain the role of genetics in the risk of certain diseases.",
        "What preventive measures can individuals take for genetic health?",
        "Discuss the importance of genetic counseling.",
    ],
    "Other Serious Diseases": [
        "How can a healthy lifestyle reduce the risk of serious diseases?",
        "Discuss the importance of regular health check-ups.",
        "What role does stress management play in preventing diseases?",
    ],
    "Resistance to Regular Diseases": [
        "How can a strong immune system prevent common illnesses?",
        "Discuss the impact of nutrition on immune health.",
        "What are effective habits for maintaining overall well-being?",
    ],
    "Sports": [
        "What are the physical and mental benefits of regular exercise?",
        "Discuss the importance of proper warm-up and cool-down in sports.",
        "Can you recommend sports activities for different fitness levels?",
    ],
    "Actual Earnings": [
        "How can individuals increase their income through career development?",
        "Discuss the importance of financial planning for wealth accumulation.",
        "What are effective investment strategies for building wealth?",
    ],
    "Possessions": [
        "How does decluttering contribute to a sense of wealth?",
        "Discuss the role of mindful spending in managing possessions.",
        "What are effective ways to prioritize spending on experiences over material goods?",
    ],
    "Social Status": [
        "How can individuals navigate social hierarchies in a positive way?",
        "Discuss the impact of social media on perceived social status.",
        "What are effective communication skills for enhancing social standing?",
    ],
    "Meetings": [
        "How can productive meetings contribute to a fulfilling social life?",
        "Discuss the importance of active listening in social interactions.",
        "What are effective strategies for networking in professional meetings?",
    ],
    "Meaningful Relations": [
        "How can individuals cultivate meaningful relationships with others?",
        "Discuss the role of empathy in building meaningful connections.",
        "What are effective conflict resolution strategies in relationships?",
    ],
}

# Flatten the list of questions to a single list
all_questions = [question for sublist in questions.values() for question in sublist]

tokenizer_questions = Tokenizer()
tokenizer_questions.fit_on_texts(all_questions)
sequences_questions = tokenizer_questions.texts_to_sequences(all_questions)
word_index_questions = tokenizer_questions.word_index

embedding_dim = 50  # Choose an appropriate embedding dimension
max_length = 20  # Choose an appropriate maximum length for questions

# Create a dictionary to map subcategories to labels
subcategory_labels = {subcategory: idx + 1 for idx, subcategory in enumerate(all_questions)}

# Create training data and labels
X_train = pad_sequences(sequences_questions, maxlen=max_length)
y_train = np.array([subcategory_labels[subcategory] for subcategory_list in questions.values() for subcategory in subcategory_list])

model = Sequential()
model.add(Embedding(len(word_index_questions) + 1, embedding_dim, input_length=max_length))
model.add(LSTM(100))
model.add(Dense(len(all_questions) + 1, activation='softmax'))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(X_train, y_train, epochs=10)

# Function to generate a random question from a given subcategory
def generate_random_question(subcategory):
    if subcategory in questions:
        subcategory_questions = questions[subcategory]
        return random.choice(subcategory_questions)
    else:
        return "Invalid subcategory."

# Function to generate questions based on user input
def generate_questions(user_category, user_subcategories, num_questions_per_subcategory, model, tokenizer, max_length):
    generated_questions = []

    for subcategory in user_subcategories:
        for _ in range(num_questions_per_subcategory):
            question = generate_random_question(subcategory)
            generated_questions.append((subcategory, question))

    return generated_questions

# Example usage:
user_category = input("Enter the category: ")
user_subcategories = input("Enter subcategories separated by commas: ").split(",")
num_questions_per_subcategory = int(input("Enter the number of questions per subcategory: "))

generated_questions = generate_questions(user_category, user_subcategories, num_questions_per_subcategory, model, tokenizer_questions, max_length)

for subcategory, question in generated_questions:
    print(f"Generated Question for {subcategory}: {question}")
