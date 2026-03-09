from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


# -----------------------------
# USERS (Authentication)
# -----------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    cooperatives = relationship("CooperativeMember", back_populates="user")


# -----------------------------
# COOPERATIVES
# -----------------------------
class Cooperative(Base):
    __tablename__ = "cooperatives"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    members = relationship("CooperativeMember", back_populates="cooperative")
    customers = relationship("Customer", back_populates="cooperative")


# -----------------------------
# COOPERATIVE MEMBERS
# -----------------------------
class CooperativeMember(Base):
    __tablename__ = "cooperative_members"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    cooperative_id = Column(Integer, ForeignKey("cooperatives.id"))

    role = Column(String, default="member")

    user = relationship("User", back_populates="cooperatives")
    cooperative = relationship("Cooperative", back_populates="members")


# -----------------------------
# CUSTOMERS
# -----------------------------
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    phone = Column(String)
    address = Column(String)

    cooperative_id = Column(Integer, ForeignKey("cooperatives.id"))

    cooperative = relationship("Cooperative", back_populates="customers")
    solar_systems = relationship("SolarSystem", back_populates="customer")
    payments = relationship("Payment", back_populates="customer")


# -----------------------------
# SOLAR SYSTEMS
# -----------------------------
class SolarSystem(Base):
    __tablename__ = "solar_systems"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"))

    system_size_kw = Column(Float)
    battery_kwh = Column(Float)
    inverter_kw = Column(Float)

    installation_date = Column(DateTime, default=datetime.utcnow)
    system_cost = Column(Float)

    customer = relationship("Customer", back_populates="solar_systems")


# -----------------------------
# PAYMENTS
# -----------------------------
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"))

    amount = Column(Float)
    due_date = Column(DateTime)
    paid = Column(Boolean, default=False)

    customer = relationship("Customer", back_populates="payments")


# -----------------------------
# PORTFOLIO METRICS
# -----------------------------
class PortfolioMetrics(Base):
    __tablename__ = "portfolio_metrics"

    id = Column(Integer, primary_key=True, index=True)

    cooperative_id = Column(Integer, ForeignKey("cooperatives.id"))

    total_customers = Column(Integer)
    active_systems = Column(Integer)
    total_revenue = Column(Float)
    default_rate = Column(Float)

    updated_at = Column(DateTime, default=datetime.utcnow)