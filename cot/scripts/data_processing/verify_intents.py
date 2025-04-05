from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
import pickle
input_path = "../../data/models/intent_model"
input_file = f"{input_path}/label_mappings.pkl"
# Load the fine-tuned model and tokenizer
model = DistilBertForSequenceClassification.from_pretrained(input_path)
tokenizer = DistilBertTokenizer.from_pretrained(input_path)

# Load label mappings
with open(input_file, "rb") as f:
    label_mappings = pickle.load(f)
id_to_label = label_mappings["id_to_label"]

# Function to predict intent
def predict_intent(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    return id_to_label[predicted_class_id]

# Test the model
test_inputs = ["hi", "check my balance", "12345", "help"]
for text in test_inputs:
    intent = predict_intent(text)
    print(f"Input: {text} -> Predicted Intent: {intent}")