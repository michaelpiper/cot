from typing import Tuple

import torch.nn.functional as F
from ...logger import logger
from ....domain.interfaces.intent_detector import IIntentDetector
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import pickle
# Concrete Implementation of IIntentDetector
class IntentDetector(IIntentDetector):
    def __init__(self, model_path: str, tokenizer_path: str, label_mappings_path: str, threshold: float = 0.7):
        """
        Initialize the IntentDetector with paths to the model, tokenizer, and label mappings.
        :param model_path: Path to the pre-trained model.
        :param tokenizer_path: Path to the tokenizer.
        :param label_mappings_path: Path to the label mappings file.
        :param threshold: Confidence threshold for predictions.
        """
        self.model = BertForSequenceClassification.from_pretrained(model_path)  # Load the model
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_path)  # Load the tokenizer
        self.threshold = threshold
        self.id_to_label = self._load_label_mappings(label_mappings_path)

    def _load_label_mappings(self, label_mappings_path: str):
        """
        Load label mappings from a file.
        :param label_mappings_path: Path to the label mappings file.
        :return: Dictionary mapping IDs to labels.
        """
        try:
            with open(label_mappings_path, "rb") as f:
                label_mappings = pickle.load(f)
            return {int(k): v for k, v in label_mappings["id_to_label"].items()}
        except FileNotFoundError:
            raise FileNotFoundError("Label mappings file not found. Ensure the file exists.")
        except Exception as e:
            raise Exception(f"Error loading label mappings: {e}")

    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict the intent of the input text.
        :param text: Input text to classify.
        :return: A tuple containing the predicted intent and its confidence score.
        """
        # Tokenize input text
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)

        # Move inputs to the same device as the model
        device = self.model.device
        inputs = {key: value.to(device) for key, value in inputs.items()}

        # Predict intent
        with torch.no_grad():
            logits = self.model(**inputs).logits
            probabilities = F.softmax(logits, dim=-1)  # Convert logits to probabilities

        predicted_class_id = logits.argmax().item()
        confidence = probabilities[0, predicted_class_id].item()  # Extract confidence score

        # Debug Logging (optional)
        logger.info(f"Logits: {logits}")
        logger.info(f"Predicted Class ID: {predicted_class_id}, Class Label: {self.id_to_label[predicted_class_id]}, Confidence: {confidence:.4f}")

        # Apply confidence threshold
        if confidence < self.threshold:
            return "unknown", confidence

        return self.id_to_label[predicted_class_id], confidence