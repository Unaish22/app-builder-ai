from transformers import AutoModelForCausalLM, AutoTokenizer
import re

# Load the CodeGen model and tokenizer
model_name = "Salesforce/codegen-350M-mono"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Fix for padding token issue
tokenizer.pad_token = tokenizer.eos_token  # Set pad_token to be the same as eos_token

def generate_code(prompt, max_length=500):
    # Create a more structured prompt with specific guidance
    enhanced_prompt = f"""
# Python Tkinter Application
# Task: {prompt}

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Todo List Application")
        self.geometry("600x500")
        self.tasks = []
        
        # Create the main UI
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
"""
    
    # Tokenize the input with the enhanced prompt
    encoded_input = tokenizer(
        enhanced_prompt,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=tokenizer.model_max_length
    )
    
    # Generate code with adjusted parameters
    outputs = model.generate(
        input_ids=encoded_input.input_ids,
        attention_mask=encoded_input.attention_mask,
        max_length=max_length,
        do_sample=True,
        temperature=0.6,  # Slightly lower temperature for more focused output
        top_p=0.92,
        top_k=40,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
        repetition_penalty=1.2,  # Add repetition penalty to avoid loops
    )
    
    # Decode the generated code
    generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Post-process to remove repetitive content
    generated_code = post_process_code(generated_code)
    
    return generated_code

def post_process_code(code):
    # Remove repetitive lines (more than 3 consecutive similar lines)
    lines = code.split('\n')
    filtered_lines = []
    repetition_count = 0
    last_line_pattern = ""
    
    for line in lines:
        # Create a simplified pattern of the line (remove numbers)
        current_pattern = re.sub(r'\d+', 'N', line)
        
        if current_pattern == last_line_pattern:
            repetition_count += 1
            if repetition_count <= 2:  # Allow up to 3 similar lines
                filtered_lines.append(line)
        else:
            repetition_count = 0
            filtered_lines.append(line)
            last_line_pattern = current_pattern
    
    return '\n'.join(filtered_lines)

def generate_todo_app_with_template():
    """Generate a complete todo app using a template approach instead of pure generation"""
    
    code = """
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Todo List with Reminders and Priorities")
        self.geometry("700x500")
        self.tasks = []
        
        # Create the main UI
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Task entry section
        task_frame = ttk.LabelFrame(main_frame, text="Add New Task", padding="10")
        task_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(task_frame, text="Task Description:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.task_entry = ttk.Entry(task_frame, width=40)
        self.task_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(task_frame, text="Due Date (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(task_frame, width=20)
        self.date_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(task_frame, text="Priority:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.priority_var = tk.StringVar()
        self.priority_combo = ttk.Combobox(task_frame, textvariable=self.priority_var, width=15)
        self.priority_combo['values'] = ('High', 'Medium', 'Low')
        self.priority_combo.current(1)  # Set default to Medium
        self.priority_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        add_button = ttk.Button(task_frame, text="Add Task", command=self.add_task)
        add_button.grid(row=3, column=1, sticky=tk.E, pady=10)
        
        # Task list section
        list_frame = ttk.LabelFrame(main_frame, text="Tasks", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create treeview for tasks
        columns = ('description', 'due_date', 'priority', 'status')
        self.task_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Define headings
        self.task_tree.heading('description', text='Task')
        self.task_tree.heading('due_date', text='Due Date')
        self.task_tree.heading('priority', text='Priority')
        self.task_tree.heading('status', text='Status')
        
        # Define columns
        self.task_tree.column('description', width=250)
        self.task_tree.column('due_date', width=100)
        self.task_tree.column('priority', width=80)
        self.task_tree.column('status', width=80)
        
        self.task_tree.pack(fill=tk.BOTH, expand=True)
        
        # Buttons for task management
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Complete Task", command=self.complete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Check Reminders", command=self.check_reminders).pack(side=tk.RIGHT, padx=5)
    
    def add_task(self):
        description = self.task_entry.get()
        due_date = self.date_entry.get()
        priority = self.priority_var.get()
        
        if not description:
            messagebox.showerror("Error", "Task description cannot be empty!")
            return
        
        try:
            if due_date:
                # Validate date format
                datetime.strptime(due_date, '%Y-%m-%d')
            else:
                due_date = "None"
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
            return
        
        # Add to treeview
        self.task_tree.insert('', tk.END, values=(description, due_date, priority, "Pending"))
        
        # Clear entries
        self.task_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", "Task added successfully!")
    
    def complete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to complete")
            return
        
        # Update status to Completed
        self.task_tree.item(selected_item, values=(
            self.task_tree.item(selected_item)['values'][0],
            self.task_tree.item(selected_item)['values'][1],
            self.task_tree.item(selected_item)['values'][2],
            "Completed"
        ))
    
    def delete_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to delete")
            return
        
        self.task_tree.delete(selected_item)
    
    def check_reminders(self):
        today = datetime.now().date()
        upcoming_tasks = []
        
        for item in self.task_tree.get_children():
            task_values = self.task_tree.item(item)['values']
            due_date = task_values[1]
            status = task_values[3]
            
            if due_date != "None" and status == "Pending":
                try:
                    task_date = datetime.strptime(due_date, '%Y-%m-%d').date()
                    days_left = (task_date - today).days
                    
                    if days_left <= 2 and days_left >= 0:
                        upcoming_tasks.append(f"{task_values[0]} - Due in {days_left} days (Priority: {task_values[2]})")
                except ValueError:
                    continue
        
        if upcoming_tasks:
            reminder_text = "Upcoming tasks:\\n" + "\\n".join(upcoming_tasks)
            messagebox.showinfo("Reminders", reminder_text)
        else:
            messagebox.showinfo("Reminders", "No upcoming tasks due soon!")

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
"""
    return code

if __name__ == "__main__":
    try:
        # Example input
        features = "Create a to-do list app with reminders"
        
        # Generate code using the model
        print("Generating code with the model...")
        generated_code = generate_code(features)
        print("Generated Code:\n", generated_code)
        
        # For the more complex example, use the template approach
        print("\nGenerating a complete to-do app with template approach...")
        template_code = generate_todo_app_with_template()
        print("\nTemplate-based Code:\n", template_code)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("\nFalling back to template-based approach only...")
        template_code = generate_todo_app_with_template()
        print("\nTemplate-based Code:\n", template_code)