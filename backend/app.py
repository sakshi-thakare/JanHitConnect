from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# custom functions
from complaintClassify import ClassifyComplaint
from water_prediction import predictWater
from electricty_prediction import predictPower


app = Flask(__name__) 
CORS(app)
genai_api_key = "AIzaSyC897bCsmDp-Yc9fCrZtuj_0Pux_YMop6o"

@app.route('/test', methods=['GET'])
def test():
    return "Hello, World!"

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data['complaint']
    print(text)
    genai.configure(api_key=genai_api_key)

    # Set up the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,  
        "top_k": 5,     
        "max_output_tokens": 50,  
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)
    
    convo = model.start_chat(history=[
    ])

    prompt = "Sumarize the following complaint in very short just give me sumary only in plain text for the title of complaint: " + text

    convo.send_message(prompt)
    summary = convo.last.text
    return jsonify({"summary": summary})

@app.route('/classify', methods=['POST'])
def classify():
    try:
        data = request.get_json()
        title = data['title']
        description = data['description']
        print(title)
        print(description)
        classification_result = ClassifyComplaint(title1=title, description1=description)
        print(classification_result['ministry'].content)
        # if classification_result and hasattr(classification_result, 'ministry'):
        #     predicted_ministry = classification_result.ministry.content
        # else:
        #     predicted_ministry = "None"

        return jsonify({"ministry": classification_result['ministry'].content})
    
    except Exception as e:
        print(e)
        return jsonify({"ministry": "None"})
    
        # ClassifyComplaint(title1=title,description1=description)

@app.route('/predict-water', methods=['POST'])
def predict_water():
    try:
        data = request.get_json()
        total_people = data['total_people']
        season = data['season']
        isConstruction = data['isConstruction']

        print(total_people) # 856
        print(season) # Summer
        print(isConstruction)  # True/False

        predicted_water = predictWater(people_in_ward=total_people, season=season, construction=isConstruction)

        predicted_water = round(predicted_water, 2)
        return jsonify({"predicted_water": predicted_water})
    
    except Exception as e:
        print(e)
        return jsonify({"predicted_water": "None"})
    
@app.route('/predict-power', methods=['POST'])
def predict_power():
    try:
        data = request.get_json()
        total_people = data['total_people']
        season = data['festive_season']
        isConstruction = data['isConstruction']

        print(total_people) # 856
        print(season) # Summer
        print(isConstruction)  # True/False

        predicted_power = predictPower(people_in_ward=total_people, season=season, construction=isConstruction)

        return jsonify({"predicted_power": predicted_power})
    
    except Exception as e:
        print(e)
        return jsonify({"predicted_power": "None"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)