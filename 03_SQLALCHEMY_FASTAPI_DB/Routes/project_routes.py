from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.project_schemas import ProjectCreate, ProjectReplace, ProjectResponse, ProjectUpdate
from services import project_service

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = project_service.create_project(db, project)
    db.commit()
    return new_project


@router.get("/", response_model=list[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return project_service.get_all_projects(db)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = project_service.get_project_by_id(db, project_id)

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_data: ProjectUpdate, db: Session = Depends(get_db)):
    project = project_service.get_project_by_id(db, project_id)

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    updated_project = project_service.update_project(db, project, project_data)
    db.commit()
    return updated_project


@router.put("/{project_id}", response_model=ProjectResponse)
def replace_project(project_id: int, project_data: ProjectReplace, db: Session = Depends(get_db)):
    project = project_service.get_project_by_id(db, project_id)

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    replaced_project = project_service.replace_project(db, project, project_data)
    db.commit()
    return replaced_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = project_service.get_project_by_id(db, project_id)

    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    project_service.delete_project(db, project)
    db.commit()
