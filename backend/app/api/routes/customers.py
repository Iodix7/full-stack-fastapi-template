from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.models import Customer, CustomerCreate, CustomerUpdate, CustomersPublic
from app.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Customer)
def create_customer(*, db: Session = Depends(get_db), customer_in: CustomerCreate):
    customer = Customer.from_orm(customer_in)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

@router.get("/", response_model=CustomersPublic)
def read_customers(*, db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return CustomersPublic(data=customers, count=len(customers))

@router.get("/{customer_id}", response_model=Customer)
def read_customer(*, db: Session = Depends(get_db), customer_id: UUID):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=Customer)
def update_customer(*, db: Session = Depends(get_db), customer_id: UUID, customer_in: CustomerUpdate):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in customer_in.dict(exclude_unset=True).items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer

@router.delete("/{customer_id}", response_model=Customer)
def delete_customer(*, db: Session = Depends(get_db), customer_id: UUID):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return customer