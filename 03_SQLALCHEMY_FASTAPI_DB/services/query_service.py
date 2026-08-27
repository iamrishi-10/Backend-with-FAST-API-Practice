from sqlalchemy import select
from sqlalchemy.orm import Session

from db.orm_models import Query
from schemas.query_schemas import QueryCreate, QueryReplace, QueryUpdate


def create_query(db: Session, query_data: QueryCreate) -> Query:
    new_query = Query(
        project_id=query_data.project_id,
        query_text=query_data.query_text,
        answer_text=query_data.answer_text,
    )

    db.add(new_query)
    db.flush()
    db.refresh(new_query)

    return new_query


def get_all_queries(db: Session) -> list[Query]:
    return db.scalars(select(Query)).all()


def get_query_by_id(db: Session, query_id: int) -> Query | None:
    return db.get(Query, query_id)


def update_query(db: Session, query: Query, query_data: QueryUpdate) -> Query:
    for field, value in query_data.model_dump(exclude_unset=True).items():
        setattr(query, field, value)

    db.flush()
    db.refresh(query)

    return query


def replace_query(db: Session, query: Query, query_data: QueryReplace) -> Query:
    query.project_id = query_data.project_id
    query.query_text = query_data.query_text
    query.answer_text = query_data.answer_text

    db.flush()
    db.refresh(query)

    return query


def delete_query(db: Session, query: Query) -> None:
    db.delete(query)
    db.flush()
