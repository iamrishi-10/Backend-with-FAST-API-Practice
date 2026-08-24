from sqlalchemy import select

from db.database import SessionLocal
from db.orm_models import Project, User


session = SessionLocal()


try:
    #find project by project id 
    project_by_id = session.scalars(
        select(Project).where(Project.project_id == 4)
    ).one_or_none()
    print(f'Found project by Project ID : {project_by_id.project_id}, Project name: {project_by_id.project_name}')

    session.delete(project_by_id)
    print(f'Deleted Project by ID: {project_by_id.project_id},  Project name: {project_by_id.project_name}')
    session.commit()

    #verify deletion using session.get()
    check = session.get(Project, 4)
    print("Verify after delete:", check)

except Exception as e:
    session.rollback()
    print("Failed:", e)

finally:
    session.close()