from sqlmodel import create_engine, SQLModel, Session

database_name = "linda_db.db"
database_path = f"sqlite:///{database_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(database_path, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)

def get_engine():
    return engine