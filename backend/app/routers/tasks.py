from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timezone
from app.core.auth import get_current_user, require_role
from app.core.database import db
from app.schemas.tasks import (
    SprintCreate, SprintUpdate, SprintResponse,
    TaskCreate, TaskUpdate, TaskStatusUpdate, TaskSubmitPR, TaskScore,
    TaskResponse, SprintProgressResponse
)
from app.services.tasks import (
    validate_transition, get_task_or_404,
    get_sprint_or_404, assert_task_owner, calculate_sprint_progress
)

router = APIRouter()

@router.post("/sprints", response_model=SprintResponse)
async def create_sprint(body: SprintCreate, user: dict = Depends(require_role("mentor", "admin"))):
    result = db.table("sprints").insert({
        "title": body.title, "description": body.description,
        "start_date": str(body.start_date), "end_date": str(body.end_date),
        "is_active": True, "created_by": user["id"],
    }).execute()
    return SprintResponse(**result.data[0])

@router.get("/sprints/active", response_model=list[SprintResponse])
async def list_active_sprints(_: dict = Depends(get_current_user)):
    result = db.table("sprints").select("*").eq("is_active", True).order("created_at", desc=True).execute()
    return [SprintResponse(**s) for s in result.data]

@router.get("/sprints", response_model=list[SprintResponse])
async def list_sprints(_: dict = Depends(get_current_user)):
    result = db.table("sprints").select("*").order("created_at", desc=True).execute()
    return [SprintResponse(**s) for s in result.data]

@router.get("/sprints/{sprint_id}/progress", response_model=SprintProgressResponse)
async def get_sprint_progress(sprint_id: str, _: dict = Depends(get_current_user)):
    get_sprint_or_404(sprint_id)
    return calculate_sprint_progress(sprint_id)

@router.get("/sprints/{sprint_id}", response_model=SprintResponse)
async def get_sprint(sprint_id: str, _: dict = Depends(get_current_user)):
    return SprintResponse(**get_sprint_or_404(sprint_id))

@router.put("/sprints/{sprint_id}", response_model=SprintResponse)
async def update_sprint(sprint_id: str, body: SprintUpdate, _: dict = Depends(require_role("mentor", "admin"))):
    updates = body.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    for field in ["start_date", "end_date"]:
        if field in updates:
            updates[field] = str(updates[field])
    result = db.table("sprints").update(updates).eq("id", sprint_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return SprintResponse(**result.data[0])

@router.get("/my", response_model=list[TaskResponse])
async def get_my_tasks(user: dict = Depends(get_current_user)):
    result = db.table("tasks").select("*").eq("assigned_to", user["id"]).execute()
    return [TaskResponse(**t) for t in result.data]

@router.post("/", response_model=TaskResponse)
async def create_task(body: TaskCreate, user: dict = Depends(require_role("mentor", "admin"))):
    get_sprint_or_404(body.sprint_id)
    now = datetime.now(timezone.utc).isoformat()
    result = db.table("tasks").insert({
        "title": body.title, "description": body.description,
        "sprint_id": body.sprint_id, "assigned_to": body.assigned_to,
        "intern_role": body.intern_role, "priority": body.priority,
        "due_date": str(body.due_date) if body.due_date else None,
        "resources": body.resources, "status": "todo",
        "created_by": user["id"], "created_at": now, "updated_at": now,
    }).execute()
    return TaskResponse(**result.data[0])

@router.get("/sprint/{sprint_id}", response_model=list[TaskResponse])
async def get_sprint_tasks(sprint_id: str, _: dict = Depends(get_current_user)):
    get_sprint_or_404(sprint_id)
    result = db.table("tasks").select("*").eq("sprint_id", sprint_id).execute()
    return [TaskResponse(**t) for t in result.data]

@router.get("/leaderboard/{sprint_id}")
async def get_leaderboard(sprint_id: str, _: dict = Depends(get_current_user)):
    result = db.table("tasks").select("assigned_to, score").eq("sprint_id", sprint_id).eq("status", "done").execute()
    user_scores: dict[str, list[int]] = {}
    for task in result.data:
        if task.get("score") is not None:
            uid = task["assigned_to"]
            user_scores.setdefault(uid, []).append(task["score"])
    leaderboard = []
    for uid, scores in user_scores.items():
        avg = round(sum(scores) / len(scores), 1)
        leaderboard.append({"user_id": uid, "average_score": avg, "tasks_done": len(scores)})
    leaderboard.sort(key=lambda x: x["average_score"], reverse=True)
    for i, entry in enumerate(leaderboard):
        entry["rank"] = i + 1
    return leaderboard

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, _: dict = Depends(get_current_user)):
    return TaskResponse(**get_task_or_404(task_id))

@router.put("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(task_id: str, body: TaskStatusUpdate, user: dict = Depends(get_current_user)):
    task = get_task_or_404(task_id)
    if user["role"] == "intern":
        assert_task_owner(task, user["id"])
    validate_transition(task["status"], body.status)
    result = db.table("tasks").update({
        "status": body.status,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }).eq("id", task_id).execute()
    return TaskResponse(**result.data[0])

@router.put("/{task_id}/submit", response_model=TaskResponse)
async def submit_pr(task_id: str, body: TaskSubmitPR, user: dict = Depends(get_current_user)):
    task = get_task_or_404(task_id)
    if user["role"] == "intern":
        assert_task_owner(task, user["id"])
    if task["status"] != "in_progress":
        raise HTTPException(status_code=400, detail="Task must be 'in_progress' before submitting a PR")
    result = db.table("tasks").update({
        "pr_url": body.pr_url, "status": "review",
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }).eq("id", task_id).execute()
    return TaskResponse(**result.data[0])

@router.put("/{task_id}/score", response_model=TaskResponse)
async def score_task(task_id: str, body: TaskScore, _: dict = Depends(require_role("mentor", "admin"))):
    task = get_task_or_404(task_id)
    if task["status"] != "review":
        raise HTTPException(status_code=400, detail="Task must be in 'review' to be scored")
    if not (0 <= body.score <= 100):
        raise HTTPException(status_code=400, detail="Score must be between 0 and 100")
    result = db.table("tasks").update({
        "score": body.score, "feedback": body.feedback, "status": "done",
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }).eq("id", task_id).execute()
    return TaskResponse(**result.data[0])

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, body: TaskUpdate, _: dict = Depends(require_role("mentor", "admin"))):
    get_task_or_404(task_id)
    updates = body.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    if "due_date" in updates:
        updates["due_date"] = str(updates["due_date"])
    updates["updated_at"] = datetime.now(timezone.utc).isoformat()
    result = db.table("tasks").update(updates).eq("id", task_id).execute()
    return TaskResponse(**result.data[0])

@router.delete("/{task_id}")
async def delete_task(task_id: str, _: dict = Depends(require_role("admin"))):
    get_task_or_404(task_id)
    db.table("tasks").delete().eq("id", task_id).execute()
    return {"message": "Task deleted"}