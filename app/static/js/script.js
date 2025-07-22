// # static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    const expenseForm = document.getElementById('expense-form');
    const expenseList = document.getElementById('expense-list');
    const ctx = document.getElementById('expense-chart').getContext('2d');
    let chart;

    expenseForm.addEventListener('submit', addExpense);
    loadExpenses();

    function addExpense(e) {
        e.preventDefault();
        const description = document.getElementById('description').value;
        const amount = document.getElementById('amount').value;
        const category = document.getElementById('category').value;

        fetch('/expenses', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ description, amount, category }),
        })
        .then(response => response.json())
        .then(expense => {
            addExpenseToList(expense);
            updateChart();
            expenseForm.reset();
        });
    }

    function loadExpenses() {
        fetch('/expenses')
            .then(response => response.json())
            .then(expenses => {
                expenses.forEach(addExpenseToList);
                updateChart();
            });
    }

    function addExpenseToList(expense) {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.innerHTML = `
            <span>${expense.description} - $${expense.amount.toFixed(2)} (${expense.category})</span>
            <button class="btn btn-danger btn-sm delete-expense" data-id="${expense.id}">Delete</button>
        `;
        li.querySelector('.delete-expense').addEventListener('click', deleteExpense);
        expenseList.appendChild(li);
    }
});
