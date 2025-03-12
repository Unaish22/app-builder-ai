from transformers import pipeline

# Load a pre-trained NLP model
nlp = pipeline("text-generation", model="gpt-2")  # ✅ Correct

def extract_features(user_input):
    # Extract features from user input
    features = nlp(user_input)
    return features

if __name__ == "__main__":
    user_input = "I want a to-do list app with reminders."
    features = extract_features(user_input)
    print("Extracted Features:", features)