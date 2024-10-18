import subprocess
import tkinter as tk
from tkinter import scrolledtext
from tkinter import font as tkfont
from colorama import init

# Initialize Colorama (for Windows compatibility)
init(autoreset=True)

def list_models():
    """Retrieve and display available models using 'ollama list'."""
    result = subprocess.run(
        ["ollama", "list"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    if result.returncode != 0:
        print(f"Error listing models: {result.stderr.strip()}")
        return []

    models = [line.split()[0] for line in result.stdout.strip().split("\n")[1:]]
    return models

def select_model():
    """Prompt the user to select a model from the command line."""
    models = list_models()
    if not models:
        print("No models found. Please make sure you have models installed.")
        exit(1)

    print("\nAvailable Models:")
    for i, model in enumerate(models):
        print(f"{i + 1}. {model}")

    while True:
        try:
            choice = int(input("\nEnter the number of the model you want to use: ")) - 1
            if 0 <= choice < len(models):
                return models[choice]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def run_model(model, user_input):
    """Run the selected model using 'ollama run'."""
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=user_input,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        if result.returncode != 0:
            return f"Error: {result.stderr.strip()}"

        return result.stdout.strip()

    except Exception as e:
        print(f"Exception while running the model: {e}")
        return f"An error occurred: {e}"

def send_message():
    """Handle sending the user's message and displaying the AI response."""
    user_input = input_box.get("1.0", tk.END).strip()
    if not user_input:
        return  # Ignore empty input

    # Display user message in the chat history
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"You: {user_input}\n", "user")
    chat_history.config(state=tk.DISABLED)

    # Run the model and display the response
    response = run_model(selected_model, user_input)

    # Display the AI response or error in the chat history
    chat_history.config(state=tk.NORMAL)
    chat_history.insert(tk.END, f"{selected_model}: {response}\n\n", "ai" if "Error" not in response else "error")
    chat_history.config(state=tk.DISABLED)

    # Clear the input box
    input_box.delete("1.0", tk.END)

def start_gui():
    """Initialize the GUI and start the chat session."""
    # Initialize the main GUI window
    root = tk.Tk()
    root.title("AI Chat with Ollama")
    root.configure(bg="#2C2C2C")  # Dark grey background

    # Custom font for better readability (bigger and bold)
    chat_font = tkfont.Font(family="Helvetica", size=14, weight="bold")

    # Allow the window to be resizable
    root.rowconfigure(0, weight=1)  # Allow the chat history row to expand
    root.columnconfigure(0, weight=1)  # Allow horizontal resizing

    # Chat history area (scrollable)
    global chat_history
    chat_history = scrolledtext.ScrolledText(
        root, wrap=tk.WORD, state=tk.DISABLED, bg="black", fg="white", 
        insertbackground="white", font=chat_font
    )
    chat_history.tag_config("user", foreground="red")
    chat_history.tag_config("ai", foreground="green")
    chat_history.tag_config("error", foreground="orange")
    chat_history.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    # Input box for user messages
    global input_box
    input_box = tk.Text(
        root, height=3, bg="black", fg="white", insertbackground="white", font=chat_font
    )
    input_box.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

    # Allow the input box to expand horizontally
    root.columnconfigure(0, weight=1)

    # Send button
    send_button = tk.Button(
        root, text="Send", command=send_message, bg="#444", fg="white", font=chat_font
    )
    send_button.grid(row=1, column=1, padx=10, pady=10)

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    # Select the model from the command prompt
    selected_model = select_model()

    # Start the GUI chat interface
    start_gui()
