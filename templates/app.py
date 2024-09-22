from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import json
import os
import re

app = Flask(__name__)

def load_expenses():
    try:
        with open('expenses.json', 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_expenses(expenses):
    with open('expenses.json', 'w') as f:
        json.dump(expenses, f, indent=2)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    if request.method == 'POST':
        expenses = load_expenses()
        new_expense = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'description': request.json['description'],
            'amount': float(request.json['amount']),
            'category': request.json['category'],
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        expenses.append(new_expense)
        save_expenses(expenses)
        return jsonify(new_expense), 201
    else:
        return jsonify(load_expenses())

@app.route('/expenses/<string:id>', methods=['DELETE'])
def delete_expense(id):
    expenses = load_expenses()
    expenses = [expense for expense in expenses if expense['id'] != id]
    save_expenses(expenses)
    return '', 204

@app.route('/process_voice_command', methods=['POST'])
def process_voice_command():
    command = request.json['command'].lower()
    
    # Process "add" commands
    add_match = re.match(r'add (\d+(?:\.\d+)?)\s*(dollars?)?\s*for\s*(.+)', command)
    if add_match:
        amount = float(add_match.group(1))
        description = add_match.group(3).strip()
        category = "Other"  # Default category
        
        # Try to extract category
        categories = ["Food", "Transportation", "Entertainment", "Utilities", "Rent"]
        for cat in categories:
            if cat.lower() in description.lower():
                category = cat
                break
        
        new_expense = {
            'id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'description': description,
            'amount': amount,
            'category': category,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        expenses = load_expenses()
        expenses.append(new_expense)
        save_expenses(expenses)
        return jsonify({"message": f"Added expense: {description} for ${amount:.2f}", "expense": new_expense}), 201
    
    # Process "remove" commands
    remove_match = re.match(r'remove (?:expense )?(.+)', command)
    if remove_match:
        description_to_remove = remove_match.group(1).strip()
        expenses = load_expenses()
        removed = False
        for expense in expenses:
            if description_to_remove.lower() in expense['description'].lower():
                expenses.remove(expense)
                removed = True
                break
        
        if removed:
            save_expenses(expenses)
            return jsonify({"message": f"Removed expense: {description_to_remove}"}), 200
        else:
            return jsonify({"message": f"No expense found matching: {description_to_remove}"}), 404
    
    return jsonify({"message": "Sorry, I didn't understand that command."}), 400

if __name__ == '__main__':
    app.run(debug=True)