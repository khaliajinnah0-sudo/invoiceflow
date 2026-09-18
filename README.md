# InvoiceFlow

InvoiceFlow is a beginner-friendly small-business invoice and expense management web application.

It allows a business to manage customers, create invoices, track payments, record expenses, and view a basic financial summary from one dashboard.

## Features

- Add and view customers
- Create invoices linked to customers
- Automatically generate invoice numbers
- Track Paid and Unpaid invoices
- Record and delete business expenses
- View total paid income
- View outstanding invoice amounts
- Calculate total expenses
- Calculate net income
- Store application data using SQLite

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Jinja2
- HTML
- CSS
- Uvicorn
- Git and GitHub

## Financial Calculation

InvoiceFlow calculates net income using:

```text
Net Income = Paid Invoice Income - Total Expenses
