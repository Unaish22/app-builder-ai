import requests
import os
import json
import random
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file (keeping this for compatibility)
load_dotenv()

# UI component templates
UI_COMPONENTS = {
    "todo_list": {
        "type": "frame",
        "name": "TodoList",
        "children": [
            {
                "type": "text",
                "name": "Title",
                "characters": "To-Do List",
                "style": {"fontWeight": "bold", "fontSize": 24}
            },
            {
                "type": "rectangle",
                "name": "AddTaskContainer",
                "children": [
                    {
                        "type": "text",
                        "name": "AddTaskPlaceholder",
                        "characters": "Add a new task..."
                    },
                    {
                        "type": "rectangle",
                        "name": "AddButton",
                        "children": [
                            {
                                "type": "text",
                                "name": "AddButtonText",
                                "characters": "Add"
                            }
                        ]
                    }
                ]
            },
            {
                "type": "rectangle",
                "name": "TaskList",
                "children": []  # Will be populated with tasks
            }
        ]
    },
    "reminder": {
        "type": "rectangle",
        "name": "ReminderSection",
        "children": [
            {
                "type": "text",
                "name": "ReminderTitle",
                "characters": "Reminders",
                "style": {"fontWeight": "bold", "fontSize": 18}
            },
            {
                "type": "rectangle",
                "name": "DatePicker",
                "children": [
                    {
                        "type": "text",
                        "name": "DatePickerLabel",
                        "characters": "Set Date:"
                    }
                ]
            },
            {
                "type": "rectangle",
                "name": "TimePicker",
                "children": [
                    {
                        "type": "text",
                        "name": "TimePickerLabel",
                        "characters": "Set Time:"
                    }
                ]
            }
        ]
    },
    "priority_selector": {
        "type": "rectangle",
        "name": "PrioritySelector",
        "children": [
            {
                "type": "text",
                "name": "PriorityLabel",
                "characters": "Priority:"
            },
            {
                "type": "rectangle",
                "name": "PriorityOptions",
                "children": [
                    {
                        "type": "text",
                        "name": "HighPriority",
                        "characters": "High"
                    },
                    {
                        "type": "text",
                        "name": "MediumPriority",
                        "characters": "Medium"
                    },
                    {
                        "type": "text",
                        "name": "LowPriority",
                        "characters": "Low"
                    }
                ]
            }
        ]
    },
    "task_item": {
        "type": "rectangle",
        "name": "TaskItem",
        "children": [
            {
                "type": "boolean",
                "name": "Checkbox",
                "value": False
            },
            {
                "type": "text",
                "name": "TaskText",
                "characters": "Sample task"
            },
            {
                "type": "text",
                "name": "DueDate",
                "characters": "Tomorrow"
            },
            {
                "type": "rectangle",
                "name": "PriorityIndicator",
                "style": {"backgroundColor": "#FF4D4D"}  # Red for high priority
            }
        ]
    }
}

# Color themes
COLOR_THEMES = [
    {
        "name": "Blue Theme",
        "primary": "#3498db",
        "secondary": "#2980b9",
        "background": "#ecf0f1",
        "text": "#2c3e50",
        "accent": "#e74c3c"
    },
    {
        "name": "Green Theme",
        "primary": "#2ecc71",
        "secondary": "#27ae60",
        "background": "#f5f5f5",
        "text": "#333333",
        "accent": "#e67e22"
    },
    {
        "name": "Purple Theme",
        "primary": "#9b59b6",
        "secondary": "#8e44ad",
        "background": "#f9f9f9",
        "text": "#34495e",
        "accent": "#f1c40f"
    },
    {
        "name": "Dark Theme",
        "primary": "#34495e",
        "secondary": "#2c3e50",
        "background": "#1a1a1a",
        "text": "#ecf0f1",
        "accent": "#3498db"
    }
]

def analyze_features(features_text):
    """
    Analyze the features text to determine what UI components to include
    
    Args:
        features_text (str): Description of the desired features
        
    Returns:
        dict: Features analysis
    """
    features = {
        "has_todo_list": "todo" in features_text.lower() or "to-do" in features_text.lower() or "task" in features_text.lower(),
        "has_reminders": "remind" in features_text.lower(),
        "has_priority": "priority" in features_text.lower(),
        "has_categories": "categor" in features_text.lower(),
        "has_dark_mode": "dark" in features_text.lower() or "theme" in features_text.lower(),
        "has_search": "search" in features_text.lower(),
        "has_filter": "filter" in features_text.lower(),
        "has_sort": "sort" in features_text.lower(),
    }
    
    return features

def generate_ui_layout(features_text):
    """
    Generate a UI layout based on the features text
    
    Args:
        features_text (str): Description of the desired features
        
    Returns:
        dict: UI layout data
    """
    # Analyze features
    features = analyze_features(features_text)
    
    # Select a color theme
    theme = random.choice(COLOR_THEMES)
    if features["has_dark_mode"]:
        theme = COLOR_THEMES[3]  # Dark theme
    
    # Create the base layout
    ui_layout = {
        "name": "Todo App UI Design",
        "lastModified": datetime.now().isoformat(),
        "version": "1.0",
        "theme": theme,
        "document": {
            "type": "document",
            "children": [
                {
                    "type": "canvas",
                    "name": "Main",
                    "children": [
                        {
                            "type": "frame",
                            "name": "Mobile App",
                            "width": 375,
                            "height": 812,
                            "backgroundColor": theme["background"],
                            "children": []
                        }
                    ]
                }
            ]
        }
    }
    
    # Get the main frame
    main_frame = ui_layout["document"]["children"][0]["children"][0]
    
    # Add header
    header = {
        "type": "rectangle",
        "name": "Header",
        "backgroundColor": theme["primary"],
        "width": 375,
        "height": 80,
        "children": [
            {
                "type": "text",
                "name": "AppTitle",
                "characters": "Todo App",
                "style": {
                    "color": "#FFFFFF",
                    "fontWeight": "bold",
                    "fontSize": 20
                },
                "x": 20,
                "y": 40
            }
        ]
    }
    main_frame["children"].append(header)
    
    # Add components based on features
    components = []
    
    if features["has_todo_list"]:
        todo_list = UI_COMPONENTS["todo_list"].copy()
        
        # Add sample tasks
        task_list = next((c for c in todo_list["children"] if c["name"] == "TaskList"), None)
        if task_list:
            for i in range(3):
                task = UI_COMPONENTS["task_item"].copy()
                task["children"][1]["characters"] = f"Sample task {i+1}"
                task_list["children"].append(task)
        
        components.append(todo_list)
    
    if features["has_reminders"]:
        components.append(UI_COMPONENTS["reminder"].copy())
    
    if features["has_priority"]:
        components.append(UI_COMPONENTS["priority_selector"].copy())
    
    # Add components to the main frame
    y_offset = 100  # Start below header
    for component in components:
        component["y"] = y_offset
        component["x"] = 20
        component["width"] = 335
        main_frame["children"].append(component)
        y_offset += 200  # Space between components
    
    # Add search bar if needed
    if features["has_search"]:
        search_bar = {
            "type": "rectangle",
            "name": "SearchBar",
            "backgroundColor": "#FFFFFF",
            "width": 335,
            "height": 40,
            "x": 20,
            "y": 90,
            "children": [
                {
                    "type": "text",
                    "name": "SearchPlaceholder",
                    "characters": "Search tasks...",
                    "style": {"color": "#999999"},
                    "x": 10,
                    "y": 10
                }
            ]
        }
        main_frame["children"].append(search_bar)
    
    return ui_layout

def save_ui_layout(ui_layout, filename="ui_layout.json"):
    """
    Save the UI layout to a file
    
    Args:
        ui_layout (dict): UI layout data
        filename (str): Output filename
    """
    with open(filename, "w") as f:
        json.dump(ui_layout, f, indent=2)
    
    # Also save a sample version
    sample = {
        "name": ui_layout.get("name", "Unknown"),
        "lastModified": ui_layout.get("lastModified", "Unknown"),
        "version": ui_layout.get("version", "Unknown"),
        "theme": ui_layout.get("theme", {}),
        "components": [child["name"] for child in ui_layout["document"]["children"][0]["children"][0]["children"]]
    }
    
    with open("figma_response_sample.json", "w") as f:
        json.dump(sample, f, indent=2)

if __name__ == "__main__":
    features = "Create a to-do list app with reminders."
    print(f"Generating UI layout for: {features}")
    
    ui_layout = generate_ui_layout(features)
    save_ui_layout(ui_layout)
    
    print("UI Layout generated successfully")
    print(f"Saved full UI layout to ui_layout.json")
    print(f"Saved sample response to figma_response_sample.json")
    
    # Print a summary of the generated UI
    theme = ui_layout.get("theme", {})
    print("\nUI Layout Summary:")
    print(f"Theme: {theme.get('name', 'Unknown')}")
    print(f"Primary Color: {theme.get('primary', 'Unknown')}")
    
    components = []
    try:
        main_frame = ui_layout["document"]["children"][0]["children"][0]
        components = [child["name"] for child in main_frame["children"]]
    except (KeyError, IndexError):
        pass
    
    print(f"Components: {', '.join(components)}")