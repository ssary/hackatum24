from fastapi import FastAPI
from src.application.routers import user_router, activity_router, message_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(activity_router.router)
app.include_router(message_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI DDD example"}
