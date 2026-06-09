import requests
import json

def emotion_detector(text_to_analyze):
    """
    Runs emotion detection on the provided text using the Watson NLP library,
    extracts the individual emotion scores, determines the dominant emotion,
    and returns a structured dictionary.
    
    Parameters:
    text_to_analyze (str): The text content that needs to be analyzed for emotions.
    
    Returns:
    dict: A dictionary containing the scores for anger, disgust, fear, joy, 
          sadness, and the name of the dominant emotion.
    """
    # Define the API endpoint URL for the Watson NLP Emotion Predict service
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    
    # Define the headers required by the gRPC-to-JSON gateway
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    
    # Create the payload dictionary representing the input JSON structure
    payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }
    
    try:
        # Perform the POST request to the Watson NLP service
        response = requests.post(url, json=payload, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response text into a dictionary
            formatted_response = json.loads(response.text)
            
            # Extract the emotions sub-dictionary
            emotions = formatted_response['emotionPredictions'][0]['emotion']
            
            # Extract individual scores
            anger_score = emotions['anger']
            disgust_score = emotions['disgust']
            fear_score = emotions['fear']
            joy_score = emotions['joy']
            sadness_score = emotions['sadness']
            
            # Find the dominant emotion (key with the maximum score value)
            dominant_emotion = max(emotions, key=emotions.get)
            
            # Construct and return the output dictionary
            return {
                'anger': anger_score,
                'disgust': disgust_score,
                'fear': fear_score,
                'joy': joy_score,
                'sadness': sadness_score,
                'dominant_emotion': dominant_emotion
            }
        else:
            # Handle non-200 responses gracefully
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
            
    except (requests.exceptions.RequestException, KeyError, ValueError, IndexError):
        # Handle connection errors, empty inputs, or parsing failures
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }