import tkinter as tk
from tkinter import ttk, messagebox

class FinanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("700x500")
        self.root.configure(bg="#f0f0f0")  # Light gray background

        # Temporary storage for transactions
        self.transactions = []

        # Call the method to create the UI
        self.create_ui()

    def create_ui(self):
        # Main Frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(pady=20)

        # Transaction Input Frame
        input_frame = tk.LabelFrame(main_frame, text="Add Transaction", bg="#f0f0f0", font=("Arial", 12, "bold"))
        input_frame.grid(row=0, column=0, padx=10, pady=10)

        # Labels
        tk.Label(input_frame, text="Category:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(input_frame, text="Amount:", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=10)
        tk.Label(input_frame, text="Date:", bg="#f0f0f0", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=10)

        # Entry Fields
        self.category_entry = tk.Entry(input_frame, font=("Arial", 10))
        self.category_entry.grid(row=0, column=1, padx=10, pady=10)

        self.amount_entry = tk.Entry(input_frame, font=("Arial", 10))
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        self.date_entry = tk.Entry(input_frame, font=("Arial", 10))
        self.date_entry.grid(row=2, column=1, padx=10, pady=10)

        # Buttons
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.grid(row=1, column=0, pady=10)

        ttk.Button(button_frame, text="Add Transaction", command=self.add_transaction, style="TButton").grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Edit Transaction", command=self.edit_transaction, style="TButton").grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete Transaction", command=self.delete_transaction, style="TButton").grid(row=0, column=2, padx=5)

        # Listbox to display transactions
        listbox_frame = tk.LabelFrame(main_frame, text="Transactions", bg="#f0f0f0", font=("Arial", 12, "bold"))
        listbox_frame.grid(row=2, column=0, padx=10, pady=10)

        self.transaction_listbox = tk.Listbox(listbox_frame, width=60, height=10, font=("Arial", 10))
        self.transaction_listbox.pack(padx=10, pady=10)

        # Summary Frame
        summary_frame = tk.LabelFrame(main_frame, text="Summary", bg="#f0f0f0", font=("Arial", 12, "bold"))
        summary_frame.grid(row=3, column=0, padx=10, pady=10)

        self.summary_label = tk.Label(summary_frame, text="Total Income: $0 | Total Expenses: $0 | Balance: $0", bg="#f0f0f0", font=("Arial", 10))
        self.summary_label.pack(padx=10, pady=10)

        # Category Filter Frame
        filter_frame = tk.LabelFrame(main_frame, text="Filter Transactions", bg="#f0f0f0", font=("Arial", 12, "bold"))
        filter_frame.grid(row=4, column=0, padx=10, pady=10)

        tk.Label(filter_frame, text="Filter by Category:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=10)
        self.category_filter_entry = tk.Entry(filter_frame, font=("Arial", 10))
        self.category_filter_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(filter_frame, text="Apply Filter", command=self.apply_filter, style="TButton").grid(row=0, column=2, padx=10)

        # Configure ttk button style
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10), background="#4CAF50", foreground="black")  # Green buttons

    def add_transaction(self):
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()

        # Input validation
        if not category or not amount or not date:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return

        # Add transaction to the list
        self.transactions.append({"category": category, "amount": amount, "date": date})
        self.update_transaction_listbox()
        self.update_summary()

    def edit_transaction(self):
        selected_index = self.transaction_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No transaction selected!")
            return

        selected_index = selected_index[0]
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()

        # Input validation
        if not category or not amount or not date:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return

        # Update the transaction
        self.transactions[selected_index] = {"category": category, "amount": amount, "date": date}
        self.update_transaction_listbox()
        self.update_summary()

    def delete_transaction(self):
        selected_index = self.transaction_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No transaction selected!")
            return

        selected_index = selected_index[0]
        del self.transactions[selected_index]
        self.update_transaction_listbox()
        self.update_summary()

    def update_transaction_listbox(self):
        self.transaction_listbox.delete(0, tk.END)
        for transaction in self.transactions:
            self.transaction_listbox.insert(tk.END, f"{transaction['date']} - {transaction['category']}: ${transaction['amount']:.2f}")

    def update_summary(self):
        total_income = sum(t['amount'] for t in self.transactions if t['amount'] > 0)
        total_expenses = sum(t['amount'] for t in self.transactions if t['amount'] < 0)
        balance = total_income + total_expenses

        self.summary_label.config(text=f"Total Income: ${total_income:.2f} | Total Expenses: ${total_expenses:.2f} | Balance: ${balance:.2f}")

    def apply_filter(self):
        category_filter = self.category_filter_entry.get()
        if not category_filter:
            self.update_transaction_listbox()
            return

        filtered_transactions = [t for t in self.transactions if t['category'].lower() == category_filter.lower()]
        self.transaction_listbox.delete(0, tk.END)
        for transaction in filtered_transactions:
            self.transaction_listbox.insert(tk.END, f"{transaction['date']} - {transaction['category']}: ${transaction['amount']:.2f}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTracker(root)
    root.mainloop()