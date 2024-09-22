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

    function deleteExpense(e) {
        const id = e.target.getAttribute('data-id');
        fetch(`/expenses/${id}`, { method: 'DELETE' })
            .then(() => {
                e.target.closest('li').remove();
                updateChart();
            });
    }

    function updateChart() {
        fetch('/expenses')
            .then(response => response.json())
            .then(expenses => {
                const categories = {};
                expenses.forEach(expense => {
                    categories[expense.category] = (categories[expense.category] || 0) + expense.amount;
                });

                const data = {
                    labels: Object.keys(categories),
                    datasets: [{
                        data: Object.values(categories),
                        backgroundColor: [
                            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
                        ]
                    }]
                };

                if (chart) {
                    chart.destroy();
                }

                chart = new Chart(ctx, {
                    type: 'pie',
                    data: data,
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Expense Distribution'
                        }
                    }
                });
            });
    }
});