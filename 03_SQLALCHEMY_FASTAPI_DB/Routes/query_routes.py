from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.query_schemas import QueryCreate, QueryReplace, QueryResponse, QueryUpdate
from services import query_service

router = APIRouter(
    prefix="/queries",
    tags=["queries"]
)


@router.post("/", response_model=QueryResponse, status_code=status.HTTP_201_CREATED)
def create_query(query: QueryCreate, db: Session = Depends(get_db)):
    new_query = query_service.create_query(db, query)
    db.commit()
    return new_query


@router.get("/", response_model=list[QueryResponse])
def get_queries(db: Session = Depends(get_db)):
    return query_service.get_all_queries(db)


@router.get("/{query_id}", response_model=QueryResponse)
def get_query(query_id: int, db: Session = Depends(get_db)):
    query = query_service.get_query_by_id(db, query_id)

    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Query not found")

    return query


@router.patch("/{query_id}", response_model=QueryResponse)
def update_query(query_id: int, query_data: QueryUpdate, db: Session = Depends(get_db)):
    query = query_service.get_query_by_id(db, query_id)

    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Query not found")

    updated_query = query_service.update_query(db, query, query_data)
    db.commit()
    return updated_query


@router.put("/{query_id}", response_model=QueryResponse)
def replace_query(query_id: int, query_data: QueryReplace, db: Session = Depends(get_db)):
    query = query_service.get_query_by_id(db, query_id)

    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Query not found")

    replaced_query = query_service.replace_query(db, query, query_data)
    db.commit()
    return replaced_query


@router.delete("/{query_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_query(query_id: int, db: Session = Depends(get_db)):
    query = query_service.get_query_by_id(db, query_id)

    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Query not found")

    query_service.delete_query(db, query)
    db.commit()
