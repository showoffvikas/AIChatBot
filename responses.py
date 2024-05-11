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
    
    processed_question = preprocess_text(nlp, question.lower())
    
    for yaml_file in yaml_files:
        with open(yaml_file, 'r') as file:
            yaml_data = yaml.safe_load(file)
        
        conversations = yaml_data.get("conversations", [])
        for conversation in conversations:
            conversation_question = conversation[0].lower() 
            conversation_answers = conversation[1:]
            processed_conversation_question = preprocess_text(nlp, conversation_question)
            similarity = nlp(processed_question).similarity(nlp(processed_conversation_question))
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
    
  
    if best_question and best_answer:
        print("Best Similar Question:", best_question)
        return best_answer
    
   
    if second_best_question and second_best_answer:
        print("Second Best Similar Question:", second_best_question)
        return second_best_answer
    
    
    if not best_question and not second_best_question:
        print("No similar question found.")
        return "No Related Data"

directory = "C:/Users/acer/Desktop/New folder/data"
yaml_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".yml")]

nlp = spacy.load("en_core_web_lg")

def handle_response(message) -> str:
    return get_most_similar_question(nlp, message)
