from sqlalchemy import select

from db.database import SessionLocal
from db.orm_models import Project, User



session = SessionLocal()


try:
    #Find alan by email 
    alan = session.scalars(
        select(User).where(User.email == "alan.turing@example.com")
    ).one()
    print("Found by email:", alan.user_id, alan.first_name, alan.last_name)

    #Change alan's last name
    alan.last_name = "Mathew"

    print("Updated user:", alan.user_id, alan.first_name, alan.last_name)

    #find one of Ada's projects and update its status
    project_name = "Document Intelligence"
    project = session.scalars(
        select(Project).where(Project.project_name == project_name)
    ).one()

    print(f"Project '{project_name}' belongs to user:  {project.user.user_id}, {project.project_id}, {project.user.first_name} {project.user.last_name}, {project.status} ")


    #change the status to completed
    project.status = 'completed'


    #Commit the changes to the database
    session.commit()

    #refresh the instance to get the updated values from the database
    session.refresh(alan)
    session.refresh(project)

    print("Updated user:", alan.user_id, alan.first_name, alan.last_name)
    print(f"Project '{project_name}' status:", project.status)
except Exception as e:
    session.rollback()
    print("Failed:", e)
finally:
    session.close()
