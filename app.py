from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import os
from together import Together

app = Flask(__name__)

# Configure Together.AI API (Replace with your credentials)
os.environ["TOGETHER_API_KEY"] = ""
api_client = Together()

# Global variable to store scraped data
scraped_data = ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scrape", methods=["POST"])
def scrape():
    global scraped_data
    url = request.form.get("url")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        scraped_data = soup.get_text(separator=" ", strip=True)
        return render_template("query.html")
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/answer", methods=["POST"])
def answer():
    global scraped_data
    user_query = request.form.get("query")
    try:
        # Sending the scraped data and user query to Together.AI
        response = api_client.chat.completions.create(
            model="meta-llama/Llama-Vision-Free",
            messages=[{"role": "user", "content": f"Data: {scraped_data}\nQuery: {user_query}"}]
        )
        return render_template("answer.html", answer=response.choices[0].message.content.strip())
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
