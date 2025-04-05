import os
import requests
from dotenv import load_dotenv
import json
import random

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

CATEGORIES = ["Verbal", "Logical", "Mathematics"]

def generate_questions(category=None, difficulty="Easy", num_questions=10):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    if not category:
        selected_categories = random.choices(CATEGORIES, k=num_questions)
    else:
        selected_categories = [category] * num_questions

    prompt = f"""Generate {num_questions} multiple choice aptitude questions randomly mixed from these categories: Verbal, Logical, Mathematics with {difficulty} difficulty.
Each question must be a JSON object with keys: 'question', 'options' (list of 4), 'answer', and 'category'. Return a JSON array of all questions."""

    body = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that generates aptitude questions."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
        if response.status_code != 200:
            print("❌ API Error:", response.status_code, response.text)
            raise Exception("API returned error")

        data = response.json()

        if "choices" not in data:
            print("❌ Unexpected response format:", data)
            raise Exception("'choices' key missing")

        content = data["choices"][0]["message"]["content"]

        # Remove markdown code block if present
        if content.strip().startswith("```json"):
            content = content.strip().split("```json")[-1].strip("` \n")
        elif content.strip().startswith("```"):
            content = content.strip().split("```")[-1].strip("` \n")

        questions = json.loads(content)

        # Ensure each question has 'category', 'options', and 'answer'
        cleaned_questions = []
        for i, q in enumerate(questions):
            q.setdefault("category", selected_categories[i % len(selected_categories)])
            q.setdefault("options", ["A", "B", "C", "D"])
            q.setdefault("answer", q["options"][0])
            cleaned_questions.append(q)

        return cleaned_questions

    except Exception as e:
        print("❌ Error generating/parsing questions:", e)
        return [{
            "question": f"API failed to load. Using fallback. What is 2 + 2?",
            "options": ["3", "4", "5", "6"],
            "answer": "4",
            "category": "Mathematics"
        }] * num_questions
