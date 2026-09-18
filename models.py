from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150))
    phone: Mapped[str] = mapped_column(String(30))
    company: Mapped[str] = mapped_column(String(100))


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    invoice_number: Mapped[str] = mapped_column(String(30), unique=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    description: Mapped[str] = mapped_column(String(250))
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    due_date: Mapped[str] = mapped_column(String(10))
    status: Mapped[str] = mapped_column(String(20), default="Unpaid")
    