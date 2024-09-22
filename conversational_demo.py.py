import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import speech_recognition as sr
import pyttsx3
import threading
import time
import difflib

class EnhancedExpenseTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Enhanced Expense Tracker")
        self.master.geometry("1000x800")
        self.master.configure(bg="#f0f0f0")

        self.expenses = self.load_expenses()
        self.categories = ["Food", "Transportation", "Entertainment", "Utilities", "Rent", "Other"]

        self.create_widgets()
        self.update_expense_list()
        self.update_pie_chart()

        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

        self.is_listening = False
        self.listen_thread = None
        self.wake_word = "hey expense tracker"

    def create_widgets(self):
        # Main Frame
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Input Frame
        input_frame = ttk.LabelFrame(main_frame, text="Add Expense", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        ttk.Label(input_frame, text="Description:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.description_entry = ttk.Entry(input_frame, width=30)
        self.description_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Amount:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.amount_entry = ttk.Entry(input_frame, width=10)
        self.amount_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="Category:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.category_combobox = ttk.Combobox(input_frame, values=self.categories, width=15)
        self.category_combobox.grid(row=0, column=5, padx=5, pady=5)

        add_button = ttk.Button(input_frame, text="Add Expense", command=self.add_expense)
        add_button.grid(row=0, column=6, padx=5, pady=5)

        self.voice_button = ttk.Button(input_frame, text="🎤 Start Listening", command=self.toggle_voice_command)
        self.voice_button.grid(row=0, column=7, padx=5, pady=5)

        # Expense List Frame
        list_frame = ttk.LabelFrame(main_frame, text="Expense List", padding="10")
        list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.expense_tree = ttk.Treeview(list_frame, columns=("Description", "Amount", "Category", "Date"), show="headings")
        self.expense_tree.heading("Description", text="Description")
        self.expense_tree.heading("Amount", text="Amount")
        self.expense_tree.heading("Category", text="Category")
        self.expense_tree.heading("Date", text="Date")
        self.expense_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.expense_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.expense_tree.configure(yscrollcommand=scrollbar.set)

        # Remove Button
        remove_button = ttk.Button(list_frame, text="Remove Selected", command=self.remove_expense)
        remove_button.pack(side=tk.BOTTOM, pady=5)

        # Pie Chart Frame
        self.chart_frame = ttk.LabelFrame(main_frame, text="Expense Distribution", padding="10")
        self.chart_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

    def add_expense(self):
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        category = self.category_combobox.get()

        if description and amount and category:
            try:
                amount = float(amount)
                expense = {
                    "id": datetime.now().strftime("%Y%m%d%H%M%S"),
                    "description": description,
                    "amount": amount,
                    "category": category,
                    "date": datetime.now().strftime("%Y-%m-%d")
                }
                self.expenses.append(expense)
                self.save_expenses()
                self.update_expense_list()
                self.update_pie_chart()
                self.clear_inputs()
                self.speak(f"Expense added: {description} for ${amount:.2f} in {category} category.")
            except ValueError:
                messagebox.showerror("Error", "Invalid amount. Please enter a number.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def remove_expense(self):
        selected_item = self.expense_tree.selection()
        if selected_item:
            item = self.expense_tree.item(selected_item)
            description = item['values'][0]
            amount = item['values'][1]
            category = item['values'][2]
            date = item['values'][3]
            
            for expense in self.expenses:
                if (expense['description'] == description and
                    f"${expense['amount']:.2f}" == amount and
                    expense['category'] == category and
                    expense['date'] == date):
                    self.expenses.remove(expense)
                    break
            
            self.save_expenses()
            self.update_expense_list()
            self.update_pie_chart()
            self.speak(f"Expense removed: {description} for {amount} in {category} category.")
        else:
            messagebox.showerror("Error", "Please select an expense to remove.")

    def update_expense_list(self):
        self.expense_tree.delete(*self.expense_tree.get_children())
        for expense in self.expenses:
            self.expense_tree.insert("", tk.END, values=(
                expense["description"],
                f"${expense['amount']:.2f}",
                expense["category"],
                expense["date"]
            ))

    def update_pie_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        category_totals = {}
        for expense in self.expenses:
            category = expense["category"]
            amount = expense["amount"]
            category_totals[category] = category_totals.get(category, 0) + amount

        if category_totals:
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.pie(category_totals.values(), labels=category_totals.keys(), autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            ax.set_title("Expense Distribution")

            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        else:
            ttk.Label(self.chart_frame, text="No expenses to display").pack()

    def clear_inputs(self):
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_combobox.set("")

    def load_expenses(self):
        try:
            with open("expenses.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_expenses(self):
        with open("expenses.json", "w") as file:
            json.dump(self.expenses, file)

    def toggle_voice_command(self):
        if not self.is_listening:
            self.is_listening = True
            self.voice_button.config(text="🛑 Stop Listening")
            self.listen_thread = threading.Thread(target=self.listen_for_wake_word)
            self.listen_thread.start()
            self.speak(f"Listening for wake word: {self.wake_word}")
        else:
            self.is_listening = False
            self.voice_button.config(text="🎤 Start Listening")
            self.speak("Voice commands deactivated.")

    def listen_for_wake_word(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            while self.is_listening:
                try:
                    self.master.update_idletasks()  # Update UI to show listening status
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    text = self.recognizer.recognize_google(audio).lower()
                    print(f"Heard: {text}")  # Debug print
                    if self.is_wake_word(text):
                        self.speak("How can I help you?")
                        self.listen_for_commands()
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    print("Could not request results from Google Speech Recognition service")
                    time.sleep(5)  # Wait before retrying
                except Exception as e:
                    print(f"An error occurred: {e}")
                    time.sleep(5)  # Wait before retrying

    def is_wake_word(self, text):
        return difflib.SequenceMatcher(None, self.wake_word, text).ratio() > 0.8

    def listen_for_commands(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"Command: {command}")  # Debug print
                self.process_command(command)
            except sr.WaitTimeoutError:
                self.speak("I didn't hear a command. Please try again.")
            except sr.UnknownValueError:
                self.speak("I didn't catch that. Can you please repeat?")
            except sr.RequestError:
                self.speak("Sorry, there was an error processing your request. Please try again.")
            except Exception as e:
                print(f"An error occurred: {e}")
                self.speak("An unexpected error occurred. Please try again.")

    def process_command(self, command):
        if "add expense" in command:
            self.add_expense_voice()
        elif "remove expense" in command:
            self.speak("Please select the expense you want to remove from the list, then say 'remove selected'.")
        elif "remove selected" in command:
            self.remove_expense()
        elif "show expenses" in command:
            self.show_expenses_summary()
        elif "stop listening" in command:
            self.is_listening = False
            self.voice_button.config(text="🎤 Start Listening")
            self.speak("Voice commands deactivated.")
        else:
            self.speak("Sorry, I didn't understand that command. You can say 'add expense', 'remove expense', 'show expenses', or 'stop listening'.")

    def add_expense_voice(self):
        try:
            self.speak("What's the description of the expense?")
            description = self.listen_for_response()
            
            self.speak(f"How much was the expense for {description}?")
            amount_str = self.listen_for_response()
            amount = self.parse_amount(amount_str)
            
            self.speak(f"What category does {description} belong to?")
            category = self.listen_for_response()
            category = self.find_closest_category(category)
            
            if description and amount is not None and category:
                self.description_entry.delete(0, tk.END)
                self.description_entry.insert(0, description)
                self.amount_entry.delete(0, tk.END)
                self.amount_entry.insert(0, str(amount))
                self.category_combobox.set(category)
                
                self.add_expense()
            else:
                self.speak("Sorry, I couldn't add the expense. Please try again.")
        except Exception as e:
            print(f"An error occurred while adding expense: {e}")
            self.speak("An error occurred while adding the expense. Please try again.")

    def parse_amount(self, amount_str):
        try:
            # Remove currency symbols and commas
            amount_str = amount_str.replace("$", "").replace(",", "")
            return float(amount_str)
        except ValueError:
            self.speak(f"Sorry, I couldn't understand the amount: {amount_str}. Please try again.")
            return None

    def find_closest_category(self, spoken_category):
        return max(self.categories, key=lambda x: difflib.SequenceMatcher(None, x.lower(), spoken_category.lower()).ratio())

    def show_expenses_summary(self):
        if not self.expenses:
            self.speak("You have no expenses recorded.")
        else:
            total = sum(expense['amount'] for expense in self.expenses)
            num_expenses = len(self.expenses)
            self.speak(f"You have {num_expenses} expenses totaling ${total:.2f}.")
            
            category_totals = {}
            for expense in self.expenses:
                category = expense["category"]
                amount = expense["amount"]
                category_totals[category] = category_totals.get(category, 0) + amount
            
            for category, amount in category_totals.items():
                percentage = (amount / total) * 100
                self.speak(f"{category}: ${amount:.2f}, which is {percentage:.1f}% of your total expenses.")

    def listen_for_response(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                response = self.recognizer.recognize_google(audio)
                print(f"Recognized: {response}")  # Debug print
                return response
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that. Can you please repeat?")
                return self.listen_for_response()
            except sr.RequestError:
                self.speak("Sorry, there was an error processing your request. Please try again.")
                return
    
    def speak(self, text):
        def speak_thread():
            self.engine.say(text)
            self.engine.runAndWait()
        
        threading.Thread(target=speak_thread).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedExpenseTracker(root)
    root.mainloop()
    