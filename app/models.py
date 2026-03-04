from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Boolean,
    Enum,
    Text,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base


# ==========================================
# ENUMS
# ==========================================

class UserRole(enum.Enum):
    CUSTOMER = "CUSTOMER"
    INSTALLER = "INSTALLER"
    COOPERATIVE_ADMIN = "COOPERATIVE_ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class PaymentStatus(enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    DEFAULTED = "DEFAULTED"
    FAILED = "FAILED"


class SystemStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    DISCONNECTED = "DISCONNECTED"
    MAINTENANCE = "MAINTENANCE"


# ==========================================
# USERS (AUTH TABLE)
# ==========================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, index=True)
    password_hash = Column(String, nullable=False)

    role = Column(Enum(UserRole), default=UserRole.CUSTOMER)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ==========================================
# CUSTOMER PROFILE
# ==========================================

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    location = Column(String, nullable=False)

    monthly_income = Column(Float, nullable=False)
    monthly_expenses = Column(Float, nullable=False)

    credit_score = Column(Integer)
    bureau_score = Column(Integer)
    default_probability = Column(Float)

    risk_grade = Column(String)

    is_flagged = Column(Boolean, default=False)
    fraud_notes = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User")
    solar_systems = relationship("SolarSystem", back_populates="customer")
    payments = relationship("Payment", back_populates="customer")


# ==========================================
# COOPERATIVES
# ==========================================

class Cooperative(Base):
    __tablename__ = "cooperatives"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    location = Column(String)

    group_risk_score = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

    members = relationship("CooperativeMember", back_populates="cooperative")


class CooperativeMember(Base):
    __tablename__ = "cooperative_members"

    id = Column(Integer, primary_key=True)
    cooperative_id = Column(Integer, ForeignKey("cooperatives.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))

    cooperative = relationship("Cooperative", back_populates="members")


# ==========================================
# SOLAR SYSTEMS
# ==========================================

class SolarSystem(Base):
    __tablename__ = "solar_systems"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
        index=True
    )

    system_kw = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)

    inverter_serial = Column(String, unique=True)

    status = Column(Enum(SystemStatus), default=SystemStatus.ACTIVE)

    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="solar_systems")


# ==========================================
# PAYMENTS
# ==========================================

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
        index=True
    )

    amount = Column(Float, nullable=False)

    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)

    due_date = Column(DateTime, index=True)
    paid_at = Column(DateTime)

    transaction_reference = Column(String, unique=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="payments")

# ==========================================
# PORTFOLIO ANALYTICS
# ==========================================

class PortfolioMetrics(Base):
    __tablename__ = "portfolio_metrics"

    id = Column(Integer, primary_key=True)

    total_active_loans = Column(Integer)
    total_defaulted_loans = Column(Integer)
    total_revenue = Column(Float)
    average_default_probability = Column(Float)

    snapshot_date = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("snapshot_date", name="unique_snapshot_per_day"),
    )