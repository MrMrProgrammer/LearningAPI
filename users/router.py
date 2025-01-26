from fastapi import HTTPException, APIRouter
from .schemas import User
from typing import List

router = APIRouter()

users_db = {}
books_db = {}


@router.post("/", response_model=User)
def create_user(user: User):
    if user.id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    users_db[user.id] = user
    return user


@router.get("/", response_model=List[User])
def get_users():
    return list(users_db.values())


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    user = users_db.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id] = user
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"detail": "User deleted"}
