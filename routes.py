from typing import Optional
from fastapi import APIRouter, HTTPException , Header
from fastapi.responses import RedirectResponse
import requests
from datetime import datetime
from database import collection, user_helper
from models import User
from settings import settings

router = APIRouter()
expire_time = 3600

@router.get("/")
async def read_root():
    print("Root endpoint accessed")
    return {"message": "Welcome to the FastAPI GitHub Login Example"}

@router.get("/login/")
async def login():
    redirect_url = f"https://github.com/login/oauth/authorize?client_id={settings.CLIENT_ID}&scope=user"
    print("redirecting to",redirect_url)
    return RedirectResponse(url=redirect_url)

@router.get("/callback")
async def callback(code: str):
   
    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
            "code": code,
        },
        headers={"Accept": "application/json"},
    )
    
    token_response_data = token_response.json()
    access_token = token_response_data.get("access_token")
    
    if not access_token:
        print("failed to retrieve token")
        raise HTTPException(status_code=400, detail="Could not retrieve access token")

    
    user_response = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    user_data = user_response.json()

    user = User(
        login=user_data.get("login"),
        email=user_data.get("email"),  
        avatar_url=user_data.get("avatar_url"),
        html_url=user_data.get("html_url"),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        token=access_token
    )

  
    user_dict = user.dict()
    await collection.insert_one(user_dict)

    return user_helper(user_dict)

@router.get("/authorize")
async def authorize_user(token:str):
    print("Authorization endpoint accessed with token",token)

    user = await collection.find_one({"token":token})
    print(user)

    if not user:
        raise HTTPException(status_code=400,detail="Invalid Token")
    
    creation = user.get("created_at")
    print(creation)
    return{
        "token":token,
        "created_at":creation,
        

    }


   


