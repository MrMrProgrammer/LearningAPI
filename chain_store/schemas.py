from pydantic import BaseModel
from typing import Optional
from datetime import date

class StaffBase(BaseModel):
    name_and_surname: str
    national_code: str
    date_of_entry: date
    date_of_birth: date

class StaffCreate(StaffBase):
    pass

class Staff(StaffBase):
    employee_code: int

    class Config:
        from_attributes=True

class CustomersBase(BaseModel):
    name_and_surname: str

class CustomersCreate(CustomersBase):
    pass

class Customers(CustomersBase):
    customer_id: int

    class Config:
        from_attributes=True

class ProductsBase(BaseModel):
    product_name: str
    price: float

class ProductsCreate(ProductsBase):
    pass

class Products(ProductsBase):
    product_code: int

    class Config:
        from_attributes=True

class CartBase(BaseModel):
    product_code: int
    quantity: int = 1

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    cart_id: int

    class Config:
        from_attributes=True

class BranchesBase(BaseModel):
    address: str

class BranchesCreate(BranchesBase):
    pass

class Branches(BranchesBase):
    branch_id: int

    class Config:
        from_attributes=True

class PaymentBase(BaseModel):
    amount: float
    customer_id: int
    branch_id: int

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    payment_id: int

    class Config:
        from_attributes=True