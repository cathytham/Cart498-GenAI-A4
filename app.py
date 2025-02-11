from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
#generate the new Openai for DALL-E
from openai import OpenAI

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

# Initialize the OpenAI client with the API key from environment variables
#client = OpenAI(os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    #get the image url from the DALL-E API to use as image background in index.html
    image_url = None

    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",  
                messages=[{"role": "developer", "content": "You are a psychedelic AI that speaks in Oulipian constraints. Your responses are short, surreal, and witty. Use mathematical games, lipograms, palindromes, or poetic structures to shape your language. Avoid predictable phrasing. Let logic slip through the cracks like liquid geometry."}, 
                          {"role": "user", "content": prompt}],
                          temperature=1.2,
                          max_completion_tokens=50
            )
            result = response.choices[0].message.content

            #generate the image url from the DALL-E API
            response = openai.images.generate(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response.data[0].url
            print(image_url)
            
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing