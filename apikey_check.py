import os
import openai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = openai.OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

def generate_mcqs():
    prompt = """
    Generate 5 multiple-choice aptitude questions on mathematics (easy level).
    Each question should have 4 options (A, B, C, D) and provide the correct answer.
    Format:
    Q1: <question>
    A. <option>
    B. <option>
    C. <option>
    D. <option>
    Answer: <correct option letter>
    """

    response = client.chat.completions.create(
        model="mistralai/mixtral-8x7b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    print("=== Response ===")
    print(response.choices[0].message.content)

generate_mcqs()
