import openai
import json
import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file
app = Flask(__name__)
openai.api_key = os.environ["OPENAI_API_KEY"]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate-summary', methods=['POST'])
def generate_summary():
    data = request.get_json()
    topic = data['topic']
    interests = data['interests']
    detail_level = data['detail_level']

    prompt = create_prompt(topic, interests, detail_level)
    response = call_gpt3(prompt)
    summary = extract_summary(response)

    return jsonify(summary)


def create_prompt(topic, interests, detail_level):
    interests_list = interests.split(', ')
    interests_prompt = ', '.join(interests_list)
    prompt = f"Generate a summary of news articles about {topic} for someone interested in {interests_prompt}. Provide a level {detail_level} detail summary."
    return prompt


def call_gpt3(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text


def extract_summary(response_text):
    summary = response_text.strip()
    return summary


if __name__ == '__main__':
    app.run(debug=True)
