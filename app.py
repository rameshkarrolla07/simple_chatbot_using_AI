from flask import Flask, render_template, request, jsonify
import json
from difflib import get_close_matches

app = Flask(__name__)

# Load knowledge base
def load_knowledge_base():
    try:
        with open('knowledge_base.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # Return an empty knowledge base if the file doesn't exist
        return {"questions": []}

# Save knowledge base
def save_knowledge_base(data):
    with open('knowledge_base.json', 'w') as file:
        json.dump(data, file, indent=2)

# Find best match for a question
def find_best_match(user_question, questions):
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Get the answer for the best-matched question
def get_answer_for_question(question, knowledge_base):
    for q in knowledge_base["questions"]:
        if q["question"].lower() == question.lower():
            return q["answer"]
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['message']
    knowledge_base = load_knowledge_base()

    # Get the best match for the user's input
    best_match = find_best_match(user_input.lower(), [q['question'].lower() for q in knowledge_base['questions']])
    
    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        return jsonify({'response': answer})
    else:
        return jsonify({'response': "I don't know the answer. Can you teach me?"})

@app.route('/learn', methods=['POST'])
def learn():
    data = request.json
    user_question = data['question']
    user_answer = data['answer']

    # Load the existing knowledge base and append the new question-answer pair
    knowledge_base = load_knowledge_base()
    knowledge_base['questions'].append({"question": user_question, "answer": user_answer})
    
    # Save the updated knowledge base
    save_knowledge_base(knowledge_base)

    return jsonify({'response': 'Thank you! I learned a new response.'})

if __name__ == '__main__':
    app.run(debug=True)
