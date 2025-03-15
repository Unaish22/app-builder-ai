from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import os
import logging
from huggingface_hub import login
import warnings

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Suppress specific warnings
warnings.filterwarnings("ignore", message="The attention mask and the pad token id were not set.")

def setup_huggingface_auth():
    """Set up Hugging Face authentication using token from environment variable or user input"""
    token = os.environ.get("HUGGINGFACE_TOKEN")
    
    if not token:
        logger.info("No Hugging Face token found in environment variables.")
        logger.info("You can get a token from https://huggingface.co/settings/tokens")
        token = input("Enter your Hugging Face token (or press Enter to try without token): ")
    
    if token:
        try:
            login(token=token)
            logger.info("Successfully logged in to Hugging Face")
            return True
        except Exception as e:
            logger.warning(f"Failed to log in with token: {e}")
    
    logger.info("Proceeding without authentication (may limit access to some models)")
    return False

def load_model(model_name="distilgpt2", use_auth=True):
    """Load a text generation model with error handling and fallbacks"""
    if use_auth:
        setup_huggingface_auth()
    
    models_to_try = [
        model_name,  # First try the requested model
        "distilgpt2",  # Fallback to smaller models if the first fails
        "gpt2-medium",
        "EleutherAI/gpt-neo-125M"
    ]
    
    for model in models_to_try:
        try:
            logger.info(f"Attempting to load model: {model}")
            
            # Try to load the model and tokenizer
            tokenizer = AutoTokenizer.from_pretrained(model)
            model = AutoModelForCausalLM.from_pretrained(model)
            
            # Create the pipeline
            nlp = pipeline("text-generation", model=model, tokenizer=tokenizer)
            logger.info(f"Successfully loaded model: {model}")
            return nlp
        
        except Exception as e:
            logger.warning(f"Failed to load model {model}: {e}")
    
    # If all models fail, raise an exception
    raise RuntimeError("Failed to load any text generation model. Please check your internet connection and Hugging Face authentication.")

def extract_features(user_input, max_length=50, num_return_sequences=1):
    """Extract features from user input using the text generation model"""
    try:
        # Load the model (only done once)
        if not hasattr(extract_features, "nlp"):
            extract_features.nlp = load_model()
        
        # Generate text based on the input
        generated_texts = extract_features.nlp(
            user_input, 
            max_length=max_length, 
            num_return_sequences=num_return_sequences,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            no_repeat_ngram_size=2
        )
        
        # Process the generated text to extract features
        features = []
        for item in generated_texts:
            # Extract the generated text
            text = item['generated_text']
            
            # Simple feature extraction: identify key phrases
            features.append({
                'original_input': user_input,
                'generated_text': text,
                'length': len(text.split()),
                'contains_app': 'app' in text.lower(),
                'contains_reminder': 'reminder' in text.lower(),
                'contains_todo': any(word in text.lower() for word in ['todo', 'to-do', 'task']),
            })
        
        return features
    
    except Exception as e:
        logger.error(f"Error in feature extraction: {e}")
        return [{'error': str(e), 'original_input': user_input}]

def offline_mode():
    """Fallback function when no models can be loaded"""
    logger.info("Running in offline mode with rule-based processing")
    
    def offline_extract_features(user_input):
        # Simple rule-based feature extraction
        features = {
            'original_input': user_input,
            'contains_app': 'app' in user_input.lower(),
            'contains_reminder': 'reminder' in user_input.lower(),
            'contains_todo': any(word in user_input.lower() for word in ['todo', 'to-do', 'task']),
        }
        return [features]
    
    return offline_extract_features

if __name__ == "__main__":
    try:
        user_input = "I want a to-do list app with reminders."
        logger.info(f"Processing input: {user_input}")
        
        features = extract_features(user_input)
        print("\nExtracted Features:")
        for i, feature in enumerate(features):
            print(f"\nFeature set {i+1}:")
            for key, value in feature.items():
                print(f"  {key}: {value}")
    
    except Exception as e:
        logger.error(f"Failed to run with online models: {e}")
        logger.info("Falling back to offline mode")
        
        # Fall back to offline mode
        offline_extract = offline_mode()
        features = offline_extract("I want a to-do list app with reminders.")
        
        print("\nExtracted Features (Offline Mode):")
        for i, feature in enumerate(features):
            print(f"\nFeature set {i+1}:")
            for key, value in feature.items():
                print(f"  {key}: {value}")
                
                