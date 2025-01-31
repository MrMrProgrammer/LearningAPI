from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .models import Staff, Customers, Products, Cart, Branches, Payment
from .models import SessionLocal
from .schemas import *

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------- Staff -----------------
@router.post("/staff/", response_model=Staff)
def create_staff(staff: Staff, db: Session = Depends(get_db)):
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff

@router.get("/staff/{employee_code}", response_model=Staff)
def read_staff(employee_code: int, db: Session = Depends(get_db)):
    db_staff = db.query(Staff).filter(Staff.employee_code == employee_code).first()
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    return db_staff

@router.put("/staff/{employee_code}", response_model=Staff)
def update_staff(employee_code: int, staff: Staff, db: Session = Depends(get_db)):
    db_staff = db.query(Staff).filter(Staff.employee_code == employee_code).first()
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    
    db_staff.name_and_surname = staff.name_and_surname
    db_staff.national_code = staff.national_code
    db_staff.date_of_entry = staff.date_of_entry
    db_staff.date_of_birth = staff.date_of_birth

    db.commit()
    db.refresh(db_staff)
    return db_staff

@router.delete("/staff/{employee_code}", response_model=dict)
def delete_staff(employee_code: int, db: Session = Depends(get_db)):
    db_staff = db.query(Staff).filter(Staff.employee_code == employee_code).first()
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    
    db.delete(db_staff)
    db.commit()
    return {"detail": "Staff deleted"}


# ----------------- Customers -----------------
@router.post("/customers/", response_model=Customers)
def create_customer(customer: Customers, db: Session = Depends(get_db)):
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

@router.get("/customers/{customer_id}", response_model=Customers)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(Customers).filter(Customers.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.put("/customers/{customer_id}", response_model=Customers)
def update_customer(customer_id: int, customer: Customers, db: Session = Depends(get_db)):
    db_customer = db.query(Customers).filter(Customers.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db_customer.name_and_surname = customer.name_and_surname

    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.delete("/customers/{customer_id}", response_model=dict)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(Customers).filter(Customers.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(db_customer)
    db.commit()
    return {"detail": "Customer deleted"}

# ----------------- Products -----------------
@router.post("/products/", response_model=Products)
def create_product(product: Products, db: Session = Depends(get_db)):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/products/{product_code}", response_model=Products)
def read_product(product_code: int, db: Session = Depends(get_db)):
    db_product = db.query(Products).filter(Products.product_code == product_code).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/products/{product_code}", response_model=Products)
def update_product(product_code: int, product: Products, db: Session = Depends(get_db)):
    db_product = db.query(Products).filter(Products.product_code == product_code).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_product.product_name = product.product_name
    db_product.price = product.price

    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/products/{product_code}", response_model=dict)
def delete_product(product_code: int, db: Session = Depends(get_db)):
    db_product = db.query(Products).filter(Products.product_code == product_code).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted"}

# ----------------- Cart -----------------
@router.post("/cart/", response_model=Cart)
def create_cart(cart_item: Cart, db: Session = Depends(get_db)):
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

@router.get("/cart/{cart_id}", response_model=Cart)
def read_cart(cart_id: int, db: Session = Depends(get_db)):
    db_cart_item = db.query(Cart).filter(Cart.cart_id == cart_id).first()
    if db_cart_item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return db_cart_item

@router.put("/cart/{cart_id}", response_model=Cart)
def update_cart(cart_id: int, cart_item: Cart, db: Session = Depends(get_db)):
    db_cart_item = db.query(Cart).filter(Cart.cart_id == cart_id).first()
    if db_cart_item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db_cart_item.product_code = cart_item.product_code
    db_cart_item.quantity = cart_item.quantity

    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

@router.delete("/cart/{cart_id}", response_model=dict)
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    db_cart_item = db.query(Cart).filter(Cart.cart_id == cart_id).first()
    if db_cart_item is None:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(db_cart_item)
    db.commit()
    return {"detail": "Cart item deleted"}

# ----------------- Branches -----------------
@router.post("/branches/", response_model=Branches)
def create_branch(branch: Branches, db: Session = Depends(get_db)):
    db.add(branch)
    db.commit()
    db.refresh(branch)
    return branch

@router.get("/branches/{branch_id}", response_model=Branches)
def read_branch(branch_id: int, db: Session = Depends(get_db)):
    db_branch = db.query(Branches).filter(Branches.branch_id == branch_id).first()
    if db_branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    return db_branch

@router.put("/branches/{branch_id}", response_model=Branches)
def update_branch(branch_id: int, branch: Branches, db: Session = Depends(get_db)):
    db_branch = db.query(Branches).filter(Branches.branch_id == branch_id).first()
    if db_branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    db_branch.address = branch.address

    db.commit()
    db.refresh(db_branch)
    return db_branch

@router.delete("/branches/{branch_id}", response_model=dict)
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    db_branch = db.query(Branches).filter(Branches.branch_id == branch_id).first()
    if db_branch is None:
        raise HTTPException(status_code=404, detail="Branch not found")
    
    db.delete(db_branch)
    db.commit()
    return {"detail": "Branch deleted"}

# ----------------- Payment -----------------
@router.post("/payment/", response_model=Payment)
def create_payment(payment: Payment, db: Session = Depends(get_db)):
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

@router.get("/payment/{payment_id}", response_model=Payment)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment

@router.put("/payment/{payment_id}", response_model=Payment)
def update_payment(payment_id: int, payment: Payment, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    db_payment.amount = payment.amount
    db_payment.customer_id = payment.customer_id
    db_payment.branch_id = payment.branch_id

    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.delete("/payment/{payment_id}", response_model=dict)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    db.delete(db_payment)
    db.commit()
    return {"detail": "Payment deleted"}