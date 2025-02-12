from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
#generate the new Openai for DALL-E
from openai import OpenAI

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

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
                messages=[{"role": "developer", "content": "You are a Jungian psychoanalyst, an expert in dream interpretation, using Carl Jung's psychological theories that uses concept like archetypes, the collective unconscious, and the process of individuation. Analyse the dreamer's dream and focus on symbolic elements such as figures, actions, and settings. Your responses are detailed and comprehensive(200 words) that is easy to understand and relate to the dreamer's dream."}, 
                          {"role": "user", "content": prompt}],
                          temperature=1.2,
                          max_completion_tokens=250
            )
            result = response.choices[0].message.content
            #generate the image url from the DALL-E API
            response = openai.images.generate(
                model="dall-e-3",
                prompt="In a dreamlike style, create a visual representations of the interpreted dreams.:"+prompt,
                n=1,
                size="1024x1024",
                quality="standard"
            )
            image_url = response.data[0].url
            
        except Exception as e:
            result = f"Error: {str(e)}"
    return render_template("index.html", result=result, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing