from fastapi import APIRouter, HTTPException, status, Depends
# from models.users import User, UserSignIn
from models.mongo_users import User, TokenResponse
from typing import List
from database.mongo_connection import Database
from auth.hash_password import HashPassword
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token



user_router = APIRouter(
    tags=["User"],
)

# users = {}
user_database = Database(User)
hash_password = HashPassword()
'''
이거는 예전 sql 코드
'''
# @user_router.post("/signup")
# async def sign_new_user(data: User) -> dict:
#     if data.email in users:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="User with supplied username exists"
#         )
#     users[data.email] = data
#     return {
#         "message": "User successfully registered!"
#     }

@user_router.get("/", response_model=List[User])
async def all_user() -> List[User]:
    users = await user_database.get_all()
    return users

@user_router.post("/signup")
async def sign_new_user(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already"
        )
    hashed_password = hash_password.create_hash(user.password)
    user.password = hashed_password
    await user_database.save(user)
    return {
        "message": "User successfully registered!"
    }

# 예전 sql코드    
# @user_router.post("/signin")
# async def sign_user_in(user: UserSignIn) -> dict:
#     if user.email not in users:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User does not exist"
#         )
#     if users[user.email].password != user.password:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Wrong credentials passed"
#         )
    
#     return {
#         "message": "User signed in successfully."
#     }

@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_exist = await User.find_one(User.email == user.username)
    if not user_exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with email does not exist"
        )
    if user_exist.password == user.password:
        return {
            "message": "User signed in successfully."
        }
    if hash_password.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.email)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid details passed"
    )
        
    
    