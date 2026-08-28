from fastapi import APIRouter
from pydantic import BaseModel
from typing import List


router = APIRouter(
    prefix="/api/v1/projects",
    tags=["Projects"],
)


# ============================================================
# DATA MODEL
# ============================================================

class ProjectCreate(BaseModel):
    name: str
    repository: str


class Project(ProjectCreate):
    id: int
    status: str


# ============================================================
# TEMPORARY PROJECT STORAGE
# ============================================================

projects: List[Project] = []

next_project_id = 1


# ============================================================
# GET PROJECTS
# ============================================================

@router.get("")
def get_projects():
    return {
        "projects": projects
    }


# ============================================================
# CREATE PROJECT
# ============================================================

@router.post("")
def create_project(project: ProjectCreate):
    global next_project_id

    new_project = Project(
        id=next_project_id,
        name=project.name,
        repository=project.repository,
        status="Connected",
    )

    projects.append(new_project)

    next_project_id += 1

    return {
        "message": "Project created successfully",
        "project": new_project,
    }


# ============================================================
# GET SINGLE PROJECT
# ============================================================

@router.get("/{project_id}")
def get_project(project_id: int):

    for project in projects:
        if project.id == project_id:
            return {
                "project": project
            }

    return {
        "message": "Project not found"
    }