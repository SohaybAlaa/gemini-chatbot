import os
from flask import Flask, request, render_template, session, redirect, url_for, jsonify
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

app = Flask(__name__)
app.secret_key = 'supersecretkey'  

@app.route('/')
def index():
    chat_history = session.get('chat_history', [])
    return render_template('index.html', chat_history=chat_history)

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form.get('question', '').strip()

    if not question:
        return redirect(url_for('index'))

    try:
        response = model.generate_content(question)
        answer = response.text
    except Exception as e:
        answer = f"❌ Error: {str(e)}"

    chat_history = session.get('chat_history', [])
    chat_history.append({"question": question, "answer": answer})
    session['chat_history'] = chat_history

    return redirect(url_for('index'))

@app.route('/chat', methods=['POST'])
def chat_api():
    user_question = request.json.get('question', '').strip()

    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    try:
        response = model.generate_content(user_question)
        return jsonify({
            "question": user_question,
            "answer": response.text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reset')
def reset():
    session.pop('chat_history', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
