# Spend Smart

An interactive web application that helps users track their daily expenses, visualize their spending patterns, and manage their budget. The Expense Tracker includes voice command capabilities, enabling users to add or remove expenses using speech recognition.

## Features

* **Add and List Expenses**: Users can input expenses with details such as description, amount, and category. The app dynamically lists all the expenses.
* **Expense Visualization**: A pie chart visualizes the distribution of expenses across different categories.
* **Total Expenses Calculation**: The total amount spent is updated in real-time as new expenses are added or removed.
* **Voice Command Integration**: Users can add or remove expenses using voice commands. The app listens to commands such as "Add 20 dollars for food" or "Remove expense for rent."
* **Responsive Design**: A user-friendly, mobile-compatible interface designed with Bootstrap for optimal use on different devices.
* **Speech Recognition**: The app uses the Web Speech API (speech recognition) to process spoken commands, making the application interactive and conversational.

## Getting Started

### Prerequisites

* Python 3.10
* Flask
* JavaScript libraries: Bootstrap, Chart.js, Font Awesome

### Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/duanshi-26/Spend_Smart.git
    cd expense-tracker
    ```

2. Install Flask and other dependencies:
    ```bash
    pip install Flask
    ```

3. Run the Flask application:
    ```bash
    python app.py
    ```

4. Open your browser and go to `http://localhost:5000` to use the app.

### File Structure

* `index.html`: The main HTML file for the front-end interface.
* `app.py`: The Flask server-side application to manage expenses.
* `expenses.json`: A JSON file to store the expenses data.

### Voice Command Examples

* **Add Expense**: "Add 20 dollars for transportation."
* **Remove Expense**: "Remove expense for rent."

The app listens to and processes these voice commands using the built-in microphone of your device.

## Future Enhancements

* **User Authentication**: Allow multiple users to maintain separate expense lists.
* **Currency Conversion**: Support for multi-currency expense tracking.
* **Detailed Reporting**: Downloadable monthly or yearly reports of expenses.

