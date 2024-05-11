import os
import sys
import spacy
import yaml
import random

def preprocess_text(nlp, text):
    doc = nlp(text)
    processed_text = " ".join([token.lemma_ for token in doc])
    return processed_text

def get_most_similar_question(nlp, question):
    best_similarity = -1.0
    best_question = None
    best_answer = None
    second_best_similarity = -1.0
    second_best_question = None
    second_best_answer = None
    
    # Preprocess the question
    processed_question = preprocess_text(nlp, question.lower())
    
    # Iterate over all YAML files and find the most similar question and its answer
    for yaml_file in yaml_files:
        with open(yaml_file, 'r') as file:
            yaml_data = yaml.safe_load(file)
        
        conversations = yaml_data.get("conversations", [])
        for conversation in conversations:
            conversation_question = conversation[0].lower()  # Convert question to lowercase
            conversation_answers = conversation[1:]
            
            # Preprocess the conversation question
            processed_conversation_question = preprocess_text(nlp, conversation_question)
            
            # Calculate similarity between the processed question and the processed conversation_question
            similarity = nlp(processed_question).similarity(nlp(processed_conversation_question))
            
            # Update the best similarity, question, and answer if the similarity is higher
            if similarity > best_similarity:
                second_best_similarity = best_similarity
                second_best_question = best_question
                second_best_answer = best_answer
                best_similarity = similarity
                best_question = conversation_question
                best_answer = random.choice(conversation_answers)
            elif similarity > second_best_similarity and conversation_question != best_question:
                second_best_similarity = similarity
                second_best_question = conversation_question
                second_best_answer = random.choice(conversation_answers)
    
    # Print the best question and its answer
    if best_question and best_answer:
        print("Best Similar Question:", best_question)
        return best_answer
    
    # Print the second-best question and its answer
    if second_best_question and second_best_answer:
        print("Second Best Similar Question:", second_best_question)
        return second_best_answer
    
    # If no similar question found
    if not best_question and not second_best_question:
        print("No similar question found.")
        return "No Related Data"

# Provide the directory path where your YAML files are located
directory = "C:/Users/acer/Desktop/New folder/data"
yaml_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".yml")]

# Load the larger model with word vectors
nlp = spacy.load("en_core_web_lg")

# Test the model by providing a question



def handle_response(message) -> str:
    return get_most_similar_question(nlp, message)
