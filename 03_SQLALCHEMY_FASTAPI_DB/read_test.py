from sqlalchemy import select

from db.database import SessionLocal
from db.orm_models import Project, User

session = SessionLocal()

try:
    # 1. Get all users
    # users = session.scalars(select(User)).all()
    # print("All users:", [(u.user_id, u.first_name, u.last_name, u.email, u.created_at) for u in users])

    # # 2. Find Alan by email
    # alan = session.scalars(
    #     select(User).where(User.email == "alan.turing@example.com")
    # ).one()
    # print("Found by email:", alan.user_id, alan.first_name, alan.last_name)

    # # 3. Get one user by primary key using session.get()
    # user_by_pk = session.get(User, alan.user_id)
    # print("Found by PK:", user_by_pk.user_id, user_by_pk.first_name)

    # # 4. Get all projects belonging to one user
    # alans_projects = session.scalars(
    #     select(Project).where(Project.user_id == alan.user_id)
    # ).all()
    # print("Alan's projects:", [p.project_name for p in alans_projects])

    # first_project = alan.projects[0]

    # print(first_project.project_name)
    # print([q.query_text for q in first_project.queries])

    # print(first_project.user.first_name)


    #Find users for a specific project
    project_name = "Knowledge Assistant"
    project = session.scalars(
        select(Project).where(Project.project_name == project_name)
    ).one_or_none()
    print(f"Project '{project_name}' belongs to user: {project.user.first_name} {project.user.last_name}")
finally:
    session.close()
