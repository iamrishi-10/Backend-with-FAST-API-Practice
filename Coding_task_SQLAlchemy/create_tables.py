from db.database import Base, engine
from db import orm_models

Base.metadata.create_all(engine)


print("Tables created:", list(Base.metadata.tables.keys()))
