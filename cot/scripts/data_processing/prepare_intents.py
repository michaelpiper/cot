
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import csv
import pickle
import os
from sklearn.model_selection import train_test_split
input_file = os.path.join(os.path.dirname(__file__),"../../../data/training/intent_dataset.csv")
output_path = os.path.normpath(os.path.join(os.path.dirname(__file__),"../../../data/models/intent_model"))
output_file = f"{output_path}/label_mappings.pkl"
texts = []
intents = []
# Load dataset
with open(input_file, mode="r",  newline='', encoding='utf-8') as f:
    data = csv.DictReader(f)
    # Convert dataset to Hugging Face Dataset format
    for x in data: 
        texts.append(x["text"] )
        intents.append(x["intent"])

# Create a mapping from intent labels to integers
intent_labels = list(set(intents))
label_to_id = {label: idx for idx, label in enumerate(intent_labels)}
id_to_label = {idx: label for label, idx in label_to_id.items()}

# Convert labels to integers
labels = [label_to_id[label] for label in intents]

# Split dataset into training and evaluation sets
train_texts, eval_texts, train_labels, eval_labels = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Create Hugging Face Dataset objects
train_dataset = Dataset.from_dict({"text": train_texts, "label": train_labels})
eval_dataset = Dataset.from_dict({"text": eval_texts, "label": eval_labels})

# Tokenize data
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

train_tokenized_dataset = train_dataset.map(tokenize_function, batched=True)
eval_tokenized_dataset = eval_dataset.map(tokenize_function, batched=True)

# Load model
model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=len(intent_labels)
)

# Define training arguments
training_args = TrainingArguments(
    output_dir=output_path,
    eval_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=0.98,  # Increase epochs for better fine-tuning
    weight_decay=0.01,
    save_strategy="epoch",
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=10,
)

# Define Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_tokenized_dataset,
    eval_dataset=eval_tokenized_dataset,
)
# Before training, explicitly put the model in training mode:
model.train()

# Train the model
trainer.train()

# Save the model and tokenizer
model.save_pretrained(output_path)
tokenizer.save_pretrained(output_path)

# Save label mappings as JSON
with open(output_file, "wb") as f:
    pickle.dump({"label_to_id": label_to_id, "id_to_label": id_to_label}, f)

print(f"Model fine-tuning complete and saved to {output_path}")