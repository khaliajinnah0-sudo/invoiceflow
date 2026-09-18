from decimal import Decimal

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select

from database import Base, SessionLocal, engine
from models import Customer, Expense, Invoice


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    with SessionLocal() as database:
        customer_count = database.query(Customer).count()
        invoices = database.scalars(select(Invoice)).all()
        expenses = database.scalars(select(Expense)).all()

        invoice_count = len(invoices)

        paid_total = sum(
            (
                invoice.amount
                for invoice in invoices
                if invoice.status == "Paid"
            ),
            Decimal("0"),
        )

        outstanding_total = sum(
            (
                invoice.amount
                for invoice in invoices
                if invoice.status == "Unpaid"
            ),
            Decimal("0"),
        )

        expense_total = sum(
            (expense.amount for expense in expenses),
            Decimal("0"),
        )

        net_income = paid_total - expense_total

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "customer_count": customer_count,
            "invoice_count": invoice_count,
            "paid_total": paid_total,
            "outstanding_total": outstanding_total,
            "expense_total": expense_total,
            "net_income": net_income,
        },
    )


@app.get("/customers", response_class=HTMLResponse)
def customers_page(request: Request):
    with SessionLocal() as database:
        customers = database.scalars(
            select(Customer).order_by(Customer.id.desc())
        ).all()

    return templates.TemplateResponse(
        request=request,
        name="customers.html",
        context={"customers": customers},
    )


@app.post("/customers")
def add_customer(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    company: str = Form(...),
):
    customer = Customer(
        name=name,
        email=email,
        phone=phone,
        company=company,
    )

    with SessionLocal() as database:
        database.add(customer)
        database.commit()

    return RedirectResponse(url="/customers", status_code=303)


@app.get("/invoices", response_class=HTMLResponse)
def invoices_page(request: Request):
    with SessionLocal() as database:
        customers = database.scalars(
            select(Customer).order_by(Customer.name)
        ).all()

        invoices = database.execute(
            select(Invoice, Customer)
            .join(Customer, Invoice.customer_id == Customer.id)
            .order_by(Invoice.id.desc())
        ).all()

    return templates.TemplateResponse(
        request=request,
        name="invoices.html",
        context={
            "customers": customers,
            "invoices": invoices,
        },
    )


@app.post("/invoices")
def add_invoice(
    customer_id: int = Form(...),
    description: str = Form(...),
    amount: Decimal = Form(...),
    due_date: str = Form(...),
):
    with SessionLocal() as database:
        latest_id = database.scalar(select(func.max(Invoice.id))) or 0
        invoice_number = f"INV-{latest_id + 1:04d}"

        invoice = Invoice(
            invoice_number=invoice_number,
            customer_id=customer_id,
            description=description,
            amount=amount,
            due_date=due_date,
            status="Unpaid",
        )

        database.add(invoice)
        database.commit()

    return RedirectResponse(url="/invoices", status_code=303)


@app.post("/invoices/{invoice_id}/paid")
def mark_invoice_paid(invoice_id: int):
    with SessionLocal() as database:
        invoice = database.get(Invoice, invoice_id)

        if invoice is not None:
            invoice.status = "Paid"
            database.commit()

    return RedirectResponse(url="/invoices", status_code=303)


@app.get("/expenses", response_class=HTMLResponse)
def expenses_page(request: Request):
    with SessionLocal() as database:
        expenses = database.scalars(
            select(Expense).order_by(Expense.id.desc())
        ).all()

    return templates.TemplateResponse(
        request=request,
        name="expenses.html",
        context={"expenses": expenses},
    )


@app.post("/expenses")
def add_expense(
    category: str = Form(...),
    description: str = Form(...),
    amount: Decimal = Form(...),
    expense_date: str = Form(...),
):
    expense = Expense(
        category=category,
        description=description,
        amount=amount,
        expense_date=expense_date,
    )

    with SessionLocal() as database:
        database.add(expense)
        database.commit()

    return RedirectResponse(url="/expenses", status_code=303)

@app.post("/expenses/{expense_id}/delete")
def delete_expense(expense_id: int):
    with SessionLocal() as database:
        expense = database.get(Expense, expense_id)

        if expense is not None:
            database.delete(expense)
            database.commit()

    return RedirectResponse(url="/expenses", status_code=303)