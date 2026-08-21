from sqlalchemy import select

from db.database import SessionLocal
from db.orm_models import Project, Query, User

session = SessionLocal()

try:
    ada = session.execute(
        select(User).where(User.email == "ada.lovelace@example.com")
    ).scalar_one()

    alan = User(
        first_name="Alan",
        last_name="Turing",
        email="alan.turing@example.com",
    )

    grace = User(
        first_name="Grace",
        last_name="Hopper",
        email="grace.hopper@example.com",
    )

    session.add(alan)
    session.add(grace)

    project_names_by_user = {
        ada: ["RAG Research", "Document Intelligence"],
        alan: ["Agent Framework", "Code Assistant"],
        grace: ["Knowledge Assistant", "API Automation"],
    }

    query_texts = [
        "What is RAG?",
        "Summarize this document",
        "Find relevant sources",
        "Generate an answer",
    ]

    for user, project_names in project_names_by_user.items():
        for project_name in project_names:
            project = Project(project_name=project_name)
            user.projects.append(project)

            for index, query_text in enumerate(query_texts):
                answer_text = None if index % 2 == 0 else f"Answer to: {query_text}"
                query = Query(query_text=query_text, answer_text=answer_text)
                project.queries.append(query)

    session.commit()

    print("Users:", session.execute(select(User)).scalars().all())
    print("Projects:", session.execute(select(Project)).scalars().all())
    print("Queries:", session.execute(select(Query)).scalars().all())
except Exception as e:
    session.rollback()
    print("Failed:", e)
finally:
    session.close()
