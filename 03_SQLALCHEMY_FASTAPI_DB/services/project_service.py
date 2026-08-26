from sqlalchemy import select
from sqlalchemy.orm import Session

from db.orm_models import Project
from schemas.project_schemas import ProjectCreate, ProjectReplace, ProjectUpdate


def create_project(db: Session, project_data: ProjectCreate) -> Project:
    new_project = Project(
        user_id=project_data.user_id,
        project_name=project_data.project_name,
    )
    if project_data.status is not None:
        new_project.status = project_data.status

    db.add(new_project)
    db.flush()
    db.refresh(new_project)

    return new_project


def get_all_projects(db: Session) -> list[Project]:
    return db.scalars(select(Project)).all()


def get_project_by_id(db: Session, project_id: int) -> Project | None:
    return db.get(Project, project_id)


def update_project(db: Session, project: Project, project_data: ProjectUpdate) -> Project:
    for field, value in project_data.model_dump(exclude_unset=True).items():
        setattr(project, field, value)

    db.flush()
    db.refresh(project)

    return project


def replace_project(db: Session, project: Project, project_data: ProjectReplace) -> Project:
    project.user_id = project_data.user_id
    project.project_name = project_data.project_name
    project.status = project_data.status

    db.flush()
    db.refresh(project)

    return project


def delete_project(db: Session, project: Project) -> None:
    db.delete(project)
    db.flush()
