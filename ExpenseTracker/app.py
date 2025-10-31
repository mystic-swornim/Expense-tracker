import os
import webbrowser
from flask import Flask
from threading import Timer

# 1. Initialize the Flask application
app = Flask(__name__)
# Suppress Flask's default logging for a cleaner terminal output
app.logger.setLevel('ERROR')

# 2. Define the HTML content as a triple-quoted string
# This string contains ALL HTML, CSS, and JavaScript for the application.
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dynamic Currency Expense Tracker</title>
    <!-- 1. Include Chart.js Library for Data Visualization -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    
    <!-- 2. All CSS Styles (Outstanding UI/UX) -->
    <style>
        /* --- CSS Reset & Variables (Using modern colors) --- */
        :root {
            --font-main: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            
            /* Light Theme */
            --color-bg: #f7f9fb;
            --color-bg-card: #ffffff;
            --color-text-primary: #1e293b;
            --color-text-secondary: #64748b;
            --color-border: #e2e8f0;
            --color-primary: #0f76e6; /* Bright Blue */
            --color-primary-hover: #0a6ad6;
            --color-green: #10b981;
            --color-red: #ef4444;
            --color-shadow: rgba(15, 118, 230, 0.1);
        }

        body.dark-mode {
            /* Dark Theme */
            --color-bg: #1e293b;
            --color-bg-card: #334155;
            --color-text-primary: #f1f5f9;
            --color-text-secondary: #94a3b8;
            --color-border: #475569;
            --color-primary: #3b82f6; 
            --color-primary-hover: #2563eb;
            --color-shadow: rgba(0, 0, 0, 0.4);
        }

        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: var(--font-main);
            background-color: var(--color-bg);
            color: var(--color-text-primary);
            transition: background-color 0.4s, color 0.4s;
            line-height: 1.6;
        }

        /* --- Layout --- */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
        }

        header h1 {
            font-size: 2.2rem;
            font-weight: 800;
            color: var(--color-primary);
        }
        
        .header-controls {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .reset-btn {
            background-color: var(--color-red);
            color: white;
            padding: 8px 16px;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s;
            border: none;
            cursor: pointer;
            font-size: 0.9rem;
        }
        .reset-btn:hover {
            opacity: 0.9;
            transform: translateY(-1px);
            box-shadow: 0 4px 6px rgba(239, 68, 68, 0.3);
        }

        .main-layout {
            display: grid;
            grid-template-columns: 1fr;
            gap: 30px;
        }

        @media (min-width: 1024px) {
            .main-layout {
                grid-template-columns: 2fr 1fr;
            }
            .sidebar {
                grid-row: 1 / span 2;
                grid-column: 2;
            }
        }

        /* --- Components --- */
        .card {
            background-color: var(--color-bg-card);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 25px var(--color-shadow);
            transition: background-color 0.4s;
            border: 1px solid var(--color-border);
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 30px var(--color-shadow);
        }

        .card-header {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 1px solid var(--color-border);
            padding-bottom: 16px;
        }
        
        .card-header-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .card-header h2 {
            font-size: 1.5rem;
            font-weight: 700;
        }

        /* Dashboard Stats */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 16px;
        }

        .stat-item {
            padding: 16px;
            border-radius: 12px;
            background-color: var(--color-bg);
            border: 1px solid var(--color-border);
        }
        
        .stat-item h3 {
            font-size: 0.85rem;
            color: var(--color-text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 8px;
        }

        .stat-item p {
            font-size: 1.5rem;
            font-weight: 700;
            line-height: 1.2;
        }
        
        #money-left.positive { color: var(--color-green); }
        #money-left.negative { 
            color: var(--color-red);
            animation: pulse-red 1s infinite alternate; 
        }
        
        @keyframes pulse-red {
            from { opacity: 1; }
            to { opacity: 0.7; }
        }
        
        #total-budget-container.negative { 
            border: 2px solid var(--color-red); 
            box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
        }

        /* Forms */
        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 0.9rem;
        }

        input:not(.btn), select {
            padding: 12px;
            border-radius: 8px;
            border: 1px solid var(--color-border);
            background-color: var(--color-bg);
            color: var(--color-text-primary);
            font-family: var(--font-main);
            font-size: 1rem;
            appearance: none;
            -webkit-appearance: none;
            transition: all 0.2s;
        }
        
        input:not(.btn):focus, select:focus {
            outline: none;
            border-color: var(--color-primary);
            box-shadow: 0 0 0 3px rgba(15, 118, 230, 0.3);
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            background-color: var(--color-primary);
            color: white;
            border: none;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s, transform 0.1s;
            padding: 12px 20px;
            font-size: 1rem;
            border-radius: 8px;
            width: 100%;
        }

        .btn:hover {
            background-color: var(--color-primary-hover);
            transform: translateY(-1px);
        }
        
        /* Expense List */
        #expense-list {
            list-style: none;
            padding: 0;
            margin-top: 10px;
        }

        .expense-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 0;
            border-bottom: 1px solid var(--color-border);
            transition: background-color 0.2s;
        }
        
        .expense-item:hover {
            background-color: var(--color-bg);
        }

        .expense-item .icon {
            flex-shrink: 0;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            color: white;
            margin-right: 16px;
            box-shadow: 0 2px 5px var(--color-shadow);
        }
        
        .expense-item .details {
            flex-grow: 1;
            min-width: 0;
        }
        
        .expense-item .amount-date {
            text-align: right;
            flex-shrink: 0;
            margin-left: 16px;
        }
        
        .expense-item .amount-date .amount {
            font-weight: 800;
            font-size: 1.2rem;
            color: var(--color-red);
        }

        /* Modal */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.7);
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .modal-content {
            margin: auto;
            width: 95%;
            max-width: 450px;
            animation: fadeIn 0.3s ease-out;
        }
        
        /* Currency input container style */
        .currency-input-group > select {
            width: 100px; 
            flex-shrink: 0;
        }
        
        .currency-input-group > input {
            width: 100%;
        }
    </style>
</head>
<body>

    <!-- Main Application Container -->
    <div class="container">
        
        <!-- Header -->
        <header>
            <h1>FINANCE FLOW</h1>
            <div class="header-controls">
                
                <!-- Primary Currency Selector -->
                <select id="primary-currency-selector" 
                        class="p-2 rounded-lg border border-gray-300 bg-white shadow-sm text-sm" 
                        title="Set Primary Display Currency">
                    <option value="USD" data-symbol="$">USD ($)</option>
                    <option value="EUR" data-symbol="€">EUR (€)</option>
                    <option value="GBP" data-symbol="£">GBP (£)</option>
                    <option value="JPY" data-symbol="¥">JPY (¥)</option>
                    <option value="INR" data-symbol="₹">INR (₹)</option>
                    <option value="NPR" data-symbol="रु">NPR (रु)</option>
                </select>
                
                <!-- Clear All Data Button -->
                <button id="clear-data-btn" class="reset-btn">
                    Reset All Data
                </button>
                
                <!-- Theme Toggle -->
                <div id="theme-toggle" class="theme-switch" title="Toggle dark/light mode" 
                     style="font-size: 1.5rem; cursor: pointer; padding: 5px;">
                    <span id="theme-icon">☀️</span>
                </div>
            </div>
        </header>

        <!-- Main Layout Grid -->
        <div class="main-layout">
            
            <!-- Main Content Area -->
            <main class="main-content">
                
                <!-- Dashboard Stats Card -->
                <div class="card">
                    <div class="card-header">
                        <div class="card-header-row">
                            <h2 id="dashboard-title">Monthly Overview</h2>
                            <div class="month-selector">
                                <input type="month" id="month-picker" style="width: auto; padding: 8px 12px; font-size: 0.9rem;">
                            </div>
                        </div>
                    </div>
                    <div class="stats-grid">
                        <div class="stat-item" id="total-budget-container">
                            <h3 id="budget-label">Monthly Budget</h3>
                            <p id="total-budget">$0.00</p>
                        </div>
                        <div class="stat-item">
                            <h3 id="spent-label">Total Spent</h3>
                            <p id="total-spent">$0.00</p>
                        </div>
                        <div class="stat-item">
                            <h3 id="left-label">Money Left</h3>
                            <p id="money-left" class="positive">$0.00</p>
                        </div>
                    </div>
                </div>

                <!-- Charts Card -->
                <div class="card" style="margin-top: 24px;">
                    <div class="card-header card-header-row">
                        <h2>Spending Analysis (Category)</h2>
                    </div>
                    <div class="charts-container" style="display: flex; justify-content: center;">
                        <div class="chart-wrapper" style="width: 100%; max-width: 500px;">
                            <canvas id="category-pie-chart"></canvas>
                        </div>
                    </div>
                </div>
                
                <!-- Expense List Card -->
                <div class="card" style="margin-top: 24px;">
                    <div class="card-header card-header-row">
                        <h2>Recent Transactions</h2>
                    </div>
                    <ul id="expense-list">
                        <li id="no-expenses-msg" style="text-align: center; padding: 20px; color: var(--color-text-secondary); font-style: italic; display: none;">
                            No expenses recorded for this month.
                        </li>
                    </ul>
                </div>
            </main>

            <!-- Sidebar -->
            <aside class="sidebar">
                
                <!-- Set Budget Card -->
                <div class="card">
                    <h2>Set Monthly Budget</h2>
                    <form id="budget-form">
                        <div class="form-group">
                            <label for="budget-amount">Amount for <strong id="budget-month-label"></strong></label>
                            <input type="number" id="budget-amount" placeholder="Enter amount" min="0" step="1" required>
                        </div>
                        <input type="submit" value="Set Budget" class="btn">
                    </form>
                </div>

                <!-- Add Expense Card -->
                <div class="card" style="margin-top: 24px;">
                    <h2>Record New Expense</h2>
                    <form id="expense-form">
                        <div class="form-group">
                            <label for="expense-amount">Amount & Currency</label>
                            <div class="currency-input-group" style="display: flex; gap: 10px;">
                                <select id="expense-currency" required>
                                    <!-- Options populated by JS for dynamic selection -->
                                </select>
                                <input type="number" id="expense-amount" placeholder="50.00" min="0.01" step="0.01" required>
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="expense-category">Category</label>
                            <input list="categories" id="expense-category" placeholder="Choose or enter category" required>
                            <datalist id="categories">
                                <option value="Food">
                                <option value="Travel">
                                <option value="Shopping">
                                <option value="Utilities">
                                <option value="Health">
                                <option value="Entertainment">
                                <option value="Other">
                            </datalist>
                        </div>
                        <div class="form-group">
                            <label for="expense-date">Date</label>
                            <input type="date" id="expense-date" required>
                        </div>
                        <div class="form-group">
                            <label for="expense-note">Note (Optional)</label>
                            <input type="text" id="expense-note" placeholder="Quick description">
                        </div>
                        <input type="submit" value="Add Expense" class="btn">
                    </form>
                </div>
            </aside>

        </div> <!-- .main-layout -->

    </div> <!-- .container -->

    <!-- Edit Expense Modal (Custom UI instead of alert()) -->
    <div id="edit-modal" class="modal">
        <div class="modal-content card">
            <h2>Edit Expense</h2>
            <form id="edit-expense-form">
                <input type="hidden" id="edit-expense-id">
                <div class="form-group">
                    <label for="edit-expense-amount">Amount & Currency</label>
                    <div class="currency-input-group" style="display: flex; gap: 10px;">
                        <select id="edit-expense-currency" required>
                             <!-- Options populated by JS -->
                        </select>
                        <input type="number" id="edit-expense-amount" min="0.01" step="0.01" required>
                    </div>
                </div>
                <div class="form-group">
                    <label for="edit-expense-category">Category</label>
                    <input list="categories" id="edit-expense-category" required>
                </div>
                <div class="form-group">
                    <label for="edit-expense-date">Date</label>
                    <input type="date" id="edit-expense-date" required>
                </div>
                <div class="form-group">
                    <label for="edit-expense-note">Note (Optional)</label>
                    <input type="text" id="edit-expense-note">
                </div>
                <input type="submit" value="Save Changes" class="btn">
                <button type="button" id="cancel-edit" class="btn" style="background-color: var(--color-text-secondary); margin-top: 10px;">Cancel</button>
            </form>
        </div>
    </div>


    <!-- Confirmation Modal (For Reset) -->
    <div id="confirmation-modal" class="modal">
        <div class="modal-content card">
            <h2 id="modal-title">Confirm Action</h2>
            <p id="modal-message" style="margin-bottom: 20px;">Are you sure you want to proceed?</p>
            <div style="display: flex; justify-content: flex-end; gap: 10px;">
                <button type="button" id="cancel-action-btn" class="btn" style="width: auto; background-color: var(--color-text-secondary);">Cancel</button>
                <button type="button" id="confirm-action-btn" class="btn" style="width: auto; background-color: var(--color-red);">Confirm Reset</button>
            </div>
        </div>
    </div>

    <!-- 3. All JavaScript Logic -->
    <script>
        document.addEventListener('DOMContentLoaded', () => {

            // --- CONSTANTS, RATES & STATE ---
            
            // Fixed Conversion Rates to USD (for internal consistency)
            // This is necessary to compare budget/expenses accurately across different currencies.
            const CURRENCY_RATES_TO_USD = {
                'USD': 1.0,
                'EUR': 1.08, // 1 USD = 0.93 EUR -> 1 EUR = 1.08 USD
                'GBP': 1.25, // 1 USD = 0.8 GBP -> 1 GBP = 1.25 USD
                'JPY': 0.0066, // 1 USD = 150 JPY -> 1 JPY = 0.0066 USD
                'INR': 0.012,  // 1 USD = 83 INR -> 1 INR = 0.012 USD
                'NPR': 0.0077, // 1 USD = 130 NPR -> 1 NPR = 0.0077 USD
            };
            
            const CURRENCY_SYMBOLS = {
                'USD': '$',
                'EUR': '€',
                'GBP': '£',
                'JPY': '¥',
                'INR': '₹',
                'NPR': 'रु',
            };
            
            const CURRENCY_OPTIONS = Object.keys(CURRENCY_RATES_TO_USD);

            let allExpenses = [];
            let allBudgets = {};
            let selectedMonth = ''; 
            let wasOverBudget = false; 
            
            // NEW: Global currency state
            let primaryCurrencyCode = 'USD'; 
            let primaryCurrencySymbol = '$';

            let categoryColorMap = {};
            let categoryPieChart = null;

            const EXPANDED_COLOR_PALETTE = [
                '#0f76e6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', 
                '#06b6d4', '#f97316', '#34d399', '#6366f1', '#fb7185',
                '#3b82f6', '#4ade80', '#fb923c', '#be123c', '#a855f7',
                '#0891b2', '#ea580c', '#059669', '#3730a3', '#e11d48',
            ];


            // --- DOM ELEMENTS & SETUP ---
            const monthPicker = document.getElementById('month-picker');
            const budgetForm = document.getElementById('budget-form');
            const expenseForm = document.getElementById('expense-form');
            const expenseList = document.getElementById('expense-list');
            const noExpensesMsg = document.getElementById('no-expenses-msg');
            const primaryCurrencySelector = document.getElementById('primary-currency-selector');
            const clearDataBtn = document.getElementById('clear-data-btn');
            
            // Modals
            const confirmationModal = document.getElementById('confirmation-modal');
            const confirmActionBtn = document.getElementById('confirm-action-btn');
            const cancelActionBtn = document.getElementById('cancel-action-btn');
            
            // Theme Toggle
            const themeToggle = document.getElementById('theme-toggle');
            const themeIcon = document.getElementById('theme-icon');
            
            // Input Selects
            const expenseCurrencySelect = document.getElementById('expense-currency');
            const editExpenseCurrencySelect = document.getElementById('edit-expense-currency');


            function init() {
                // Load data from localStorage
                allExpenses = JSON.parse(localStorage.getItem('expenses')) || [];
                allBudgets = JSON.parse(localStorage.getItem('budgets')) || {};
                categoryColorMap = JSON.parse(localStorage.getItem('categoryColorMap')) || {};
                
                // Load global currency preference
                primaryCurrencyCode = localStorage.getItem('primaryCurrencyCode') || 'USD';
                primaryCurrencySymbol = CURRENCY_SYMBOLS[primaryCurrencyCode] || '$';


                // Set initial month to current month
                const today = new Date();
                const currentYear = today.getFullYear();
                const currentMonth = String(today.getMonth() + 1).padStart(2, '0');
                selectedMonth = `${currentYear}-${currentMonth}`;
                monthPicker.value = selectedMonth;

                // Set today's date in expense form
                document.getElementById('expense-date').value = dateToHTML(today);

                // Setup currency selectors
                setupCurrencySelectors();

                // Setup event listeners
                monthPicker.addEventListener('change', handleMonthChange);
                budgetForm.addEventListener('submit', handleSetBudget);
                expenseForm.addEventListener('submit', handleAddExpense);
                expenseList.addEventListener('click', handleListActions);
                primaryCurrencySelector.addEventListener('change', handlePrimaryCurrencyChange);
                clearDataBtn.addEventListener('click', showClearDataConfirmation);
                themeToggle.addEventListener('click', toggleTheme);
                
                // Load initial theme
                loadTheme();

                // Initial render
                updateUI();
            }

            /** Populates the currency options in all relevant select elements. */
            function setupCurrencySelectors() {
                primaryCurrencySelector.value = primaryCurrencyCode;
                
                const optionsHTML = CURRENCY_OPTIONS.map(code => 
                    `<option value="${code}" data-symbol="${CURRENCY_SYMBOLS[code]}">${code} (${CURRENCY_SYMBOLS[code]})</option>`
                ).join('');

                expenseCurrencySelect.innerHTML = optionsHTML;
                editExpenseCurrencySelect.innerHTML = optionsHTML;
                
                // Default the input currency to the primary one
                expenseCurrencySelect.value = primaryCurrencyCode;
            }

            // --- DATA & STATE MANAGEMENT ---
            
            function saveData() {
                localStorage.setItem('expenses', JSON.stringify(allExpenses));
                localStorage.setItem('budgets', JSON.stringify(allBudgets));
                localStorage.setItem('categoryColorMap', JSON.stringify(categoryColorMap)); 
                localStorage.setItem('primaryCurrencyCode', primaryCurrencyCode);
            }
            
            function getExpensesForMonth(month) {
                return allExpenses
                    .filter(exp => exp.date.startsWith(month))
                    .sort((a, b) => new Date(b.date) - new Date(a.date));
            }

            function getBudgetForMonth(month) {
                // Budget is stored in the primary currency for that month
                return allBudgets[month] || 0;
            }

            /**
             * Converts an amount from its source currency to the currently selected primary currency.
             * This allows for accurate dashboard calculation regardless of input currency.
             */
            function convertToPrimary(amount, fromCode) {
                if (fromCode === primaryCurrencyCode) {
                    return amount;
                }
                
                // Convert to USD first (intermediate step)
                const amountInUSD = amount * CURRENCY_RATES_TO_USD[fromCode];
                
                // Convert from USD to the Primary Currency
                // Division by rate_to_usd is equivalent to multiplication by rate_from_usd
                return amountInUSD / CURRENCY_RATES_TO_USD[primaryCurrencyCode];
            }
            
            function getCategoryColor(category) {
                if (categoryColorMap[category]) {
                    return categoryColorMap[category];
                }
                
                const categories = Object.keys(categoryColorMap);
                const paletteIndex = categories.length % EXPANDED_COLOR_PALETTE.length;
                const newColor = EXPANDED_COLOR_PALETTE[paletteIndex];
                
                categoryColorMap[category] = newColor;
                saveData();
                return newColor;
            }
            
            // --- MAIN UI RENDERER ---
            
            function updateUI() {
                // Update currency symbols in header and inputs
                document.getElementById('dashboard-title').textContent = `Monthly Overview (${primaryCurrencyCode})`;
                document.getElementById('budget-label').textContent = `Monthly Budget (${primaryCurrencyCode})`;
                document.getElementById('spent-label').textContent = `Total Spent (${primaryCurrencyCode})`;
                document.getElementById('left-label').textContent = `Money Left (${primaryCurrencyCode})`;

                // Update budget form label
                const [year, month] = selectedMonth.split('-');
                const monthName = new Date(year, month - 1, 1).toLocaleString('default', { month: 'long' });
                document.getElementById('budget-month-label').textContent = `${monthName} ${year}`;
                
                // Get current month's data
                const currentBudget = getBudgetForMonth(selectedMonth); 
                const currentExpenses = getExpensesForMonth(selectedMonth);
                
                // Update views
                updateDashboard(currentBudget, currentExpenses);
                renderExpenseList(currentExpenses);
                renderCharts(currentExpenses);
            }

            // --- DASHBOARD UPDATER ---
            function updateDashboard(budget, expenses) {
                // Calculate total spent in Primary Currency
                const spentInPrimary = expenses.reduce((sum, exp) => sum + convertToPrimary(exp.amount, exp.currencyCode), 0);
                const left = budget - spentInPrimary;

                // Dashboard displays are all in the Primary Currency
                document.getElementById('total-budget').textContent = formatCurrency(budget);
                document.getElementById('total-spent').textContent = formatCurrency(spentInPrimary);
                document.getElementById('money-left').textContent = formatCurrency(left);
                
                const moneyLeftEl = document.getElementById('money-left');
                const totalBudgetContainer = document.getElementById('total-budget-container');

                // Reset classes
                moneyLeftEl.classList.remove('positive', 'negative');
                totalBudgetContainer.classList.remove('negative');

                // Apply color and status indicators
                if (left >= 0) {
                    moneyLeftEl.classList.add('positive');
                } else if (left < 0) {
                    moneyLeftEl.classList.add('negative');
                    totalBudgetContainer.classList.add('negative'); 
                }

                // Alert logic for going out of budget
                const isOverBudget = left < 0 && budget > 0;
                if (isOverBudget && !wasOverBudget) {
                    showNotification("🚨 You are going out of budget! 🚨", 'error');
                }
                wasOverBudget = isOverBudget; 
            }

            // --- EXPENSE LIST RENDERER ---
            function renderExpenseList(expenses) {
                expenseList.innerHTML = ''; 

                if (expenses.length === 0) {
                    expenseList.appendChild(noExpensesMsg);
                    noExpensesMsg.style.display = 'block';
                    return;
                }
                noExpensesMsg.style.display = 'none';

                expenses.forEach(exp => {
                    const li = document.createElement('li');
                    li.className = 'expense-item';
                    li.dataset.id = exp.id;

                    const categoryIcon = getCategoryIconEmoji(exp.category);
                    const categoryColor = getCategoryColor(exp.category);
                    
                    // Display amount in the primary currency for comparison
                    const primaryAmount = convertToPrimary(exp.amount, exp.currencyCode);

                    li.innerHTML = `
                        <div class="icon" data-category="${exp.category}" title="${exp.category}">
                            ${categoryIcon}
                        </div>
                        <div class="details">
                            <div class="category">${exp.category} (${exp.currencyCode} recorded)</div>
                            <div class="note">${exp.note || 'No notes'}</div>
                        </div>
                        <div class="amount-date">
                            <div class="amount">-${formatCurrency(primaryAmount)}</div>
                            <div class="date">${exp.date}</div>
                        </div>
                        <div class="actions">
                            <button class="btn-icon btn-edit" title="Edit Expense" onclick="openEditModal(${exp.id})" style="background: none; border: none; cursor: pointer; color: var(--color-primary);">
                                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                            </button>
                        </div>
                    `;
                    li.querySelector('.icon').style.backgroundColor = categoryColor;
                    
                    expenseList.appendChild(li);
                });
            }

            // --- CHART RENDERING (ONLY PIE) ---
            
            function renderCharts(expenses) {
                const ctx = document.getElementById('category-pie-chart').getContext('2d');
                const isDarkMode = document.body.classList.contains('dark-mode');
                const colors = {
                    text: isDarkMode ? '#f1f5f9' : '#1e293b',
                    grid: isDarkMode ? '#475569' : '#e2e8f0'
                };
                
                // Group expenses by category (converted to Primary Currency)
                const categoryTotals = expenses.reduce((acc, exp) => {
                    const amountInPrimary = convertToPrimary(exp.amount, exp.currencyCode);
                    acc[exp.category] = (acc[exp.category] || 0) + amountInPrimary;
                    return acc;
                }, {});

                const labels = Object.keys(categoryTotals);
                const data = Object.values(categoryTotals);
                const backgroundColors = labels.map(label => getCategoryColor(label)); 

                if (categoryPieChart) {
                    categoryPieChart.destroy();
                }

                categoryPieChart = new Chart(ctx, {
                    type: 'pie',
                    data: {
                        labels: labels,
                        datasets: [{
                            data: data,
                            backgroundColor: backgroundColors,
                            borderColor: colors.grid,
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'right',
                                labels: { color: colors.text, boxWidth: 15, padding: 10 }
                            },
                            title: {
                                display: true,
                                text: `Expenses by Category (Total in ${primaryCurrencyCode})`,
                                color: colors.text,
                                font: { size: 14, weight: 'bold' }
                            }
                        }
                    }
                });
            }
            
            // --- EVENT HANDLERS ---
            
            function handlePrimaryCurrencyChange(e) {
                const selectedOption = e.target.options[e.target.selectedIndex];
                primaryCurrencyCode = e.target.value;
                primaryCurrencySymbol = selectedOption.dataset.symbol;
                
                // Save and update the entire UI
                saveData();
                updateUI();
                showNotification(`Primary currency set to ${primaryCurrencyCode}`, 'info');
            }
            
            function handleMonthChange(e) {
                selectedMonth = e.target.value;
                wasOverBudget = false;
                updateUI();
            }

            function handleSetBudget(e) {
                e.preventDefault();
                const amount = parseFloat(document.getElementById('budget-amount').value);
                if (isNaN(amount) || amount < 0) {
                    showNotification("Please enter a valid budget amount.", 'warning');
                    return;
                }
                
                // Budget is stored in the currently selected primary currency
                allBudgets[selectedMonth] = amount;
                saveData();
                updateUI();
                showNotification("Budget set successfully!", 'success');
            }

            function handleAddExpense(e) {
                e.preventDefault();
                const amount = parseFloat(document.getElementById('expense-amount').value);
                // Note: We record the original input currency code, not the primary code
                const currencyCode = document.getElementById('expense-currency').value; 
                const category = document.getElementById('expense-category').value.trim();
                const date = document.getElementById('expense-date').value;
                const note = document.getElementById('expense-note').value.trim();

                if (!amount || !currencyCode || !category || !date) {
                    showNotification("Please fill in all required fields.", 'warning');
                    return;
                }
                
                getCategoryColor(category);

                const newExpense = {
                    id: new Date().getTime(),
                    amount: amount,
                    currencyCode: currencyCode, // Store original code
                    category: category,
                    date: date,
                    note: note
                };

                allExpenses.push(newExpense);
                saveData();
                
                if (newExpense.date.startsWith(selectedMonth)) {
                    updateUI();
                }
                
                // Reset form
                expenseForm.reset();
                document.getElementById('expense-date').value = dateToHTML(new Date());
                document.getElementById('expense-currency').value = primaryCurrencyCode;
                showNotification(`Expense of ${formatCurrency(amount, currencyCode, true)} added.`, 'info');
            }
            
            function handleListActions(e) {
                const button = e.target.closest('.btn-edit'); 
                if (!button) return;
                
                const li = button.closest('.expense-item');
                const id = li.dataset.id;
                
                window.openEditModal(id);
            }
            
            // --- CLEAR/RESET LOGIC ---
            function showClearDataConfirmation() {
                document.getElementById('modal-title').textContent = "Confirm Data Reset";
                document.getElementById('modal-message').textContent = "WARNING: This action is irreversible and will delete ALL your saved budgets and expenses.";
                
                confirmationModal.style.display = 'flex';

                confirmActionBtn.onclick = handleClearAllData;
                cancelActionBtn.onclick = () => confirmationModal.style.display = 'none';
            }

            function handleClearAllData() {
                confirmationModal.style.display = 'none';
                
                // Clear localStorage items
                localStorage.removeItem('expenses');
                localStorage.removeItem('budgets');
                localStorage.removeItem('categoryColorMap');
                localStorage.removeItem('primaryCurrencyCode');
                
                // Reset internal state
                allExpenses = [];
                allBudgets = {};
                categoryColorMap = {};
                primaryCurrencyCode = 'USD';
                primaryCurrencySymbol = '$';
                
                // Re-initialize and update UI
                init();
                
                showNotification("All data has been cleared and reset to default.", 'success');
            }


            // --- EDIT MODAL LOGIC --- (Simplified as a placeholder for now)
            window.openEditModal = function(id) {
                 // For now, we will simply notify that the edit feature needs implementation
                 showNotification("Edit functionality is currently disabled. Use the Reset button to start over.", 'warning');
                 // In a full application, this would populate the edit modal fields and display it.
            }

            // --- THEME & UTILITIES ---
            function toggleTheme() {
                document.body.classList.toggle('dark-mode');
                
                let theme = 'light';
                if (document.body.classList.contains('dark-mode')) {
                    theme = 'dark';
                    themeIcon.innerHTML = '🌙'; 
                } else {
                    themeIcon.innerHTML = '☀️';
                }
                localStorage.setItem('theme', theme);
                
                // Re-render charts to pick up new color scheme
                updateUI();
            }
            
            function loadTheme() {
                const theme = localStorage.getItem('theme');
                if (theme === 'dark') {
                    document.body.classList.add('dark-mode');
                    themeIcon.innerHTML = '🌙';
                } else {
                    themeIcon.innerHTML = '☀️';
                }
            }
            
            /**
             * Formats amount using the primary currency symbol.
             * @param {number} amount - Amount in the primary currency.
             * @param {string} overrideCode - Optional: code to display if this is the original input amount.
             * @param {boolean} useOverride - Optional: use the override code for symbol.
             * @returns {string} Formatted currency string.
             */
            function formatCurrency(amount, overrideCode = primaryCurrencyCode, useOverride = false) {
                const code = useOverride ? overrideCode : primaryCurrencyCode;
                const symbol = useOverride ? CURRENCY_SYMBOLS[overrideCode] : primaryCurrencySymbol;
                
                const formatted = new Intl.NumberFormat('en-US', {
                    style: 'currency',
                    currency: code,
                    currencyDisplay: 'symbol',
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                }).format(Math.abs(amount));

                // Replace the default symbol with our custom one if needed (e.g., 'रु')
                return formatted.replace('$', symbol).replace('£', symbol).replace('€', symbol).replace('¥', symbol).replace('INR', '').replace('NPR', '').replace('Rs.', symbol).trim();
            }
            
            function dateToHTML(date) {
                const y = date.getFullYear();
                const m = String(date.getMonth() + 1).padStart(2, '0');
                const d = String(date.getDate()).padStart(2, '0');
                return `${y}-${m}-${d}`;
            }

            function getCategoryIconEmoji(category) {
                switch (category.toLowerCase()) {
                    case 'food': return '🍔';
                    case 'travel': return '✈️';
                    case 'shopping': return '🛍️';
                    case 'utilities': return '💡';
                    case 'health': return '💊';
                    case 'entertainment': return '🎬';
                    default: return '💰';
                }
            }
            
            // Custom notification system (replacing forbidden native alert())
            function showNotification(message, type = 'info') {
                const notificationId = 'app-notification';
                let notification = document.getElementById(notificationId);
                
                if (!notification) {
                    notification = document.createElement('div');
                    notification.id = notificationId;
                    notification.style.cssText = `
                        position: fixed;
                        top: 20px;
                        right: 20px;
                        padding: 12px 20px;
                        border-radius: 8px;
                        color: white;
                        font-weight: 600;
                        z-index: 2000;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                        transform: translateX(120%);
                        opacity: 0;
                    `;
                    document.body.appendChild(notification);
                }

                let bgColor = 'var(--color-primary)';
                if (type === 'error') bgColor = 'var(--color-red)';
                if (type === 'warning') bgColor = '#fcd34d'; // Tailwind yellow-300
                if (type === 'success') bgColor = 'var(--color-green)';
                
                notification.style.backgroundColor = bgColor;
                notification.textContent = message;
                
                setTimeout(() => {
                    notification.style.transform = 'translateX(0)';
                    notification.style.opacity = '1';
                }, 10);

                setTimeout(() => {
                    notification.style.transform = 'translateX(120%)';
                    notification.style.opacity = '0';
                }, 3000);
            }

            // --- RUN APPLICATION ---
            init();

        });
    </script>
</body>
</html>
"""

# 3. Define the Flask route to serve the embedded HTML
@app.route('/')
def home():
    """Returns the single-file HTML application content."""
    return HTML_CONTENT

def open_browser(port):
    """Opens the web browser to the application URL."""
    try:
        webbrowser.open_new(f'http://127.0.0.1:{port}')
    except Exception as e:
        print(f"Failed to auto-open browser: {e}. Please open http://127.0.0.1:{port} manually.")

if __name__ == '__main__':
    # Flask runs on port 5000 by default
    port = 5000
    print(f"\n==================================================")
    print(f"  🚀 Starting Single-File Expense Tracker...")
    print(f"  💡 Requires Flask: (pip install Flask).")
    print(f"  🌍 View your app at: http://127.0.0.1:{port}")
    print(f"  ℹ️  Press CTRL+C to stop the server.")
    print(f"==================================================")
    
    # Open the browser 1 second after the server starts
    Timer(1, open_browser, args=(port,)).start()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=port, debug=False)
