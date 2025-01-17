from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware

origins = ['*']


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specify allowed origins
    allow_credentials=True,  # Allow credentials
    allow_methods=["*"],     # Allow all methods
    allow_headers=["*"],     # Allow all headers
)

app.include_router(router,prefix="/api")