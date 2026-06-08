import requests
import json

def emotion_detector(text_to_analyze):
    # Define the URL for the Watson NLP Emotion Detection service
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    
    # Define the headers required for the API request
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    
    # Structure the payload as expected by the Watson NLP service
    payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }
    
    try:
        # Send a POST request to the emotion detection service
        response = requests.post(url, json=payload, headers=headers)
        
        # Error handling for empty or invalid inputs (Status Code 400)
        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
        
        # Convert response text to a Python dictionary
        formatted_response = json.loads(response.text)
        
        # Extract the emotion scores dictionary
        # Based on structure: response_dict['emotionPredictions'][0]['emotion']
        emotions = formatted_response['emotionPredictions'][0]['emotion']
        
        anger_score = emotions['anger']
        disgust_score = emotions['disgust']
        fear_score = emotions['fear']
        joy_score = emotions['joy']
        sadness_score = emotions['sadness']
        
        # Write the code logic to find the dominant emotion with the highest score
        dominant_emotion = max(emotions, key=emotions.get)
        
        # Structure the final output dictionary format exactly as requested
        output = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
        }
        
        return output
        
    except (requests.exceptions.RequestException, KeyError, IndexError, json.JSONDecodeError):
        # Return fallback dictionary with None if any parsing or requests fail
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }