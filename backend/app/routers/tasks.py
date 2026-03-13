from fastapi import APIRouter, Depends, HTTPException
from app.core.auth import get_current_user
from app.core.database import db

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.get("/my-tasks")
async def get_my_tasks(current_user: dict = Depends(get_current_user)):
    """Get tasks for the current intern filtered by their assigned project."""
    user_id = current_user["id"]

    # Get the intern's assigned project
    profile = db.table("profiles").select("project_id").eq("id", user_id).execute()
    project_id = profile.data[0].get("project_id") if profile.data else None

    if project_id:
        # Return tasks for their specific project
        result = db.table("tasks").select("*").eq("assigned_to", user_id).eq("project_id", project_id).execute()
    else:
        # Fallback: return all tasks assigned to them
        result = db.table("tasks").select("*").eq("assigned_to", user_id).execute()

    return result.data or []


@router.get("/sprints/active")
async def get_active_sprint(current_user: dict = Depends(get_current_user)):
    """Get the active sprint for the intern's assigned project."""
    user_id = current_user["id"]

    # Get the intern's assigned project
    profile = db.table("profiles").select("project_id").eq("id", user_id).execute()
    project_id = profile.data[0].get("project_id") if profile.data else None

    if project_id:
        # Find sprint that has tasks for this project
        tasks = db.table("tasks").select("sprint_id").eq("project_id", project_id).limit(1).execute()
        if tasks.data and tasks.data[0].get("sprint_id"):
            sprint_id = tasks.data[0]["sprint_id"]
            sprint = db.table("sprints").select("*").eq("id", sprint_id).execute()
            return sprint.data or []

    # Fallback: return any active sprint
    result = db.table("sprints").select("*").eq("is_active", True).limit(1).execute()
    return result.data or []


@router.get("/{task_id}")
async def get_task(task_id: str, current_user: dict = Depends(get_current_user)):
    """Get a single task by ID."""
    result = db.table("tasks").select("*").eq("id", task_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return result.data[0]


@router.patch("/{task_id}/status")
async def update_task_status(task_id: str, body: dict, current_user: dict = Depends(get_current_user)):
    """Update task status."""
    valid_statuses = ["todo", "in_progress", "review", "done"]
    status = body.get("status")
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")

    result = db.table("tasks").update({"status": status}).eq("id", task_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return result.data[0]


@router.patch("/{task_id}")
async def update_task(task_id: str, body: dict, current_user: dict = Depends(get_current_user)):
    """Update task fields."""
    allowed = {"title", "description", "status", "priority", "due_date", "resources"}
    update_data = {k: v for k, v in body.items() if k in allowed}
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")

    result = db.table("tasks").update(update_data).eq("id", task_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return result.data[0]
