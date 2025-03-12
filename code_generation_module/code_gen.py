from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the CodeGen model and tokenizer
model_name = "Salesforce/codegen-350M-mono"  # You can use other variants like "codegen-2B-mono"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_code(features):
    # Tokenize the input features
    inputs = tokenizer (features, return_tensors="pt")

    # Generate code using the CodeGen model
    outputs = model.generate(
        inputs.input_ids,
        max_length=100,  # Adjust the length of the generated code
        num_return_sequences=1,  # Nu mber of code snippets to generate
        temperature=0.7,  # Controls randomness (lower = more deterministic)
    )

    # Decode the generated code
    generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_code

if __name__ == "__main__":
    # Example input: Features extracted from NLU module
    features = "Create a to-do list app with reminders."
 
    # Generate code
    generated_code = generate_code(features)
    print("Generated Code:\n", generated_code)