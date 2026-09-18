from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select

from database import Base, SessionLocal, engine
from models import Customer


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    with SessionLocal() as database:
        customer_count = database.query(Customer).count()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"customer_count": customer_count}
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
        context={"customers": customers}
    )


@app.post("/customers")
def add_customer(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    company: str = Form(...)
):
    customer = Customer(
        name=name,
        email=email,
        phone=phone,
        company=company
    )

    with SessionLocal() as database:
        database.add(customer)
        database.commit()

    return RedirectResponse(url="/customers", status_code=303)
