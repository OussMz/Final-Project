from fastapi import APIRouter, HTTPException
from utils.task_helpers import load_tasks, save_tasks
from schemas.tasks_schema import InitialTask, FullTask, UpdatedTask
import os

app_folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tasks_file_path = os.path.join(app_folder_path, "tasks.txt")

router = APIRouter()

@router.get("")
def check_completion_status(completed: bool = None):
    if not completed:
        raise HTTPException(status_code=400, detail="Status query parameter is invalid or missing")
    tasks = load_tasks(tasks_file_path)
    completed_tasks = [t for t in tasks if t["completed"] == completed]
    return {"completed_tasks": completed_tasks, "total_tasks": len(tasks)}

@router.get("/")
def read_tasks():
    tasks = load_tasks(tasks_file_path)
    return {"tasks": tasks}

@router.get("/stats")
def get_stats():
    tasks = load_tasks(tasks_file_path)
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t["completed"]])
    pending_tasks = total_tasks - completed_tasks
    completion_percentage = f"{(completed_tasks / total_tasks * 100) if total_tasks > 0 else 0:.2f}%"
    return {"total_tasks": total_tasks, "completed_tasks": completed_tasks, "pending_tasks": pending_tasks, "completion_percentage": completion_percentage}

@router.get("/{id}")
def read_task(task: int):
    tasks = load_tasks(tasks_file_path)
    for t in tasks:
        if t["id"] == task:
            return {"task": t}
    raise HTTPException(status_code=404, detail="Task not found")

@router.post("/")
def create_task(task: InitialTask):
    tasks = load_tasks(tasks_file_path)
    new_id = max([t["id"] for t in tasks], default=0) + 1
    new_task = {"id" : new_id, "title": task.title, "description": task.description, "completed": False}
    tasks.append(new_task)
    save_tasks(tasks_file_path, tasks)
    return {"message": "Task created successfully", "task": new_task}

@router.put("/{id}")
def update_task(task_id: int, task: UpdatedTask):
    tasks = load_tasks(tasks_file_path)
    for t in tasks:
        if t["id"] == task_id:
            t["title"] = task.title
            t["description"] = task.description
            t["completed"] = task.completed
            save_tasks(tasks_file_path, tasks)
            return {"message": "Task updated successfully", "task": t}
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/{id}")
def delete_task(task_id: int):
    tasks = load_tasks(tasks_file_path)
    for t in tasks:
        if t["id"] == task_id:
            tasks.remove(t)
            save_tasks(tasks_file_path, tasks)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/")
def delete_all_tasks():
    save_tasks(tasks_file_path, [])
    return {"message": "All tasks deleted successfully"}
