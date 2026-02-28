from fastapi import FastAPI
from routes.tasks_route import router as task_router

app = FastAPI()

app.include_router(task_router, prefix="/tasks", tags=["tasks"])

@app.get("/")
def root_check():
    return {"message": "Welcome to the Task Management API!"}