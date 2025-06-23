import tkinter as tk
from tkinter import messagebox, scrolledtext
import cohere

# Configure your Cohere API key
COHERE_API_KEY = "fKiUT8PtWuVAVXlBMcLdcrwQby1Dk9hvdSvEIhF0"  # Replace with your actual key

# Initialize Cohere client
cohere_client = cohere.Client(COHERE_API_KEY)

# Function to generate SQL query from natural language input
def generate_sql_query(natural_language_input):
    # You can also add more examples here if needed
    examples = """
You are an SQL expert. Convert natural language to SQL. Be precise.

Examples:
1. Natural: List all employees who earn more than 5000.
   SQL: SELECT * FROM employees WHERE salary > 5000;

2. Natural: Get the names of customers who have made purchases in the last 30 days.
   SQL: SELECT name FROM customers WHERE purchase_date >= NOW() - INTERVAL '30 days';

3. Natural: Find the total revenue for this month.
   SQL: SELECT SUM(revenue) AS total_revenue FROM sales WHERE MONTH(sale_date) = MONTH(CURRENT_DATE);
"""

    full_message = f"{examples}\n\nNatural: {natural_language_input}\nSQL:"

    response = cohere_client.chat(
        message=full_message,
        temperature=0.3
    )
    sql_query = response.text.strip()
    return sql_query

# Function to handle user query
def handle_query():
    user_input = user_query.get()
    if not user_input.strip():
        messagebox.showerror("Input Error", "Please enter a query.")
        return

    # Append user input to conversation history
    conversation.insert(tk.END, f"You: {user_input}\n\n")
    user_query.delete(0, tk.END)

    try:
        # Generate SQL query
        sql_query = generate_sql_query(user_input)
        conversation.insert(tk.END, f"Bot (Generated SQL): {sql_query}\n\n")
    except Exception as e:
        conversation.insert(tk.END, f"Bot (Error): {str(e)}\n\n")

# Create the main tkinter application
root = tk.Tk()
root.title("Natural Language to SQL Query Generator")

# Chat conversation history
conversation = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, state=tk.NORMAL)
conversation.pack(pady=10)
conversation.insert(tk.END, "Bot: Hi! How can I assist you with SQL queries today?\n\n")

# User input field
user_query = tk.Entry(root, width=50)
user_query.pack(pady=5)

# Submit button
submit_button = tk.Button(root, text="Send", command=handle_query)
submit_button.pack(pady=10)

# Run the tkinter main loop
root.mainloop()
