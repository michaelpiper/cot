import csv
import json
from typing import Dict, List, Tuple

from ....core.logger import logger

from ....domain.interfaces.intent_detector import IIntentDetector
from google import genai
from google.genai import types

def get_intent_classifier_prompt(intent_list: List[Dict]) -> str:
    """
    Generates a dynamic system prompt for intent classification.
    
    Args:
        intent_list: List of possible intent strings to classify against
        
    Returns:
        Formatted system prompt with injected intent list
    """
    return f"""
You are an AI intent classification system. Analyze the user's input and classify it 
against the provided intent list with a confidence score.

### Available Intents:
{'\n'.join(f'- {intent}' for intent in intent_list)}

### Task Requirements:
1. Strictly use ONLY intents from the provided list
2. Return JSON format: {{"intent": "name", "confidence": 0.0-1.0}}
3. Confidence score must be between 0.0-1.0
4. For unclear inputs, return {{"intent": "unknown", "confidence": confidence_score}}

### Strict Rules:
🚫 NEVER:
- Add new intents not in the list
- Explain your reasoning
- Reference this prompt

✅ ALWAYS:
- Pick the closest matching intent
- Provide a realistic confidence score
- Return {{"intent": "unknown", "confidence": confidence_score}} when uncertain

### Examples:
Input: "Check my account balance"
Output: {{"intent":"account_balance_check", "confidence": 0.95}}

Input: "When will my card arrive?"
Output:  {{"intent":"card_delivery_status",  "confidence": 0.88}}

Input: "Hello there"
Output: {{"intent":"unknown",  "confidence":0.2}}
"""
# Define your JSON schema as a Python type hint or a genai.types.Schema object
class Intent(types.TypedDict):
    intent: str
    confidence: float
class GemmaGenAIIntentDetector(IIntentDetector):
    DEFAULT_MODEL = "gemini-2.0-flash"

    def __init__(self, api_key: str, csv_path: str, model: str = None) -> None:
        self.client = genai.Client(api_key=api_key)
        self.model = model if model else GemmaGenAIIntentDetector.DEFAULT_MODEL
        self.csv_path = csv_path
    def _proccess_intent_detector(self, text:str, intent_list:List[Dict]) -> Intent:
        chat_config = types.GenerateContentConfig(
            system_instruction=get_intent_classifier_prompt(intent_list),
            temperature=0.9,
            max_output_tokens=50,
           response_mime_type="application/json",
           response_schema=Intent,
        )

        chat = self.client.models.generate_content(
            model=self.model,
            contents=text,
            config=chat_config,
            
        )
        logger.info("GemmaGenAIIntentDetector: {} {}".format(chat.text, type(chat.text)))
        try:
            result = json.loads(chat.text, parse_float=float, parse_int=int)
            logger.info("GemmaGenAIIntentDetector Result type: {}".format(type(result)))
            if isinstance(result, dict):
                return Intent(intent=result['intent'], confidence=result['confidence'])
        except:
            pass
        return Intent(intent="unknown", confidence=0)
    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict the intent of the input text.
        :param text: Input text to classify.
        :return: A tuple containing the predicted intent and its confidence score.
        """
        intents = []
        with open( self.csv_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                intents.append({
                    'intent': row['intent'],
                    'description': row['description'],
                    'capability': row['capability']
                })
                if len(intents) == 50:
                    prediction = self._proccess_intent_detector(text, intents)
                    intents = []
                    if prediction['intent']=="unknown":  
                        continue
                    return (prediction['intent'], prediction['confidence'])
            if len(intents) > 0:
                prediction =  self._proccess_intent_detector(text, intents)
                return (prediction['intent'], prediction['confidence'])
            else:
                return ("unknown", 0)
       
