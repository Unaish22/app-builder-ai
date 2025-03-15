from nlu_module.nlu import extract_features
from code_generation_module.code_gen import generate_code
from ui_design_module.ui_design import generate_ui_layout

def main():
    # Example user input
    user_input = "I want a to-do list app with reminders."

    # Step 1: Extract features
    features = extract_features(user_input)
    print("Extracted Features:", features)

    # Step 2: Generate code
    code = generate_code(features)
    print("Generated Code:", code)

    # Step 3: Generate UI layout
    ui_layout = generate_ui_layout(features)
    print("UI Layout:", ui_layout)

if __name__ == "__main__":
    main()

    