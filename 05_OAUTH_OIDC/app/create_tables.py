from db.base import Base
from db.database import engine
from db.orm_models import auth_identity, user

Base.metadata.create_all(engine)


print("Tables created:", list(Base.metadata.tables.keys()))
