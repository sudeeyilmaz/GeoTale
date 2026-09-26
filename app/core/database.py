from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Engine configuration
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """pgvector extension'ını (PostgreSQL ise) ve tabloları oluşturur."""
    if settings.DATABASE_URL.startswith("postgresql"):
        try:
            with engine.connect() as conn:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
                conn.commit()
                print("pgvector extension initialized successfully.")
        except Exception as e:
            print(f"Warning: Could not initialize pgvector extension: {e}")
            
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

def get_db():
    """FastAPI Depends ile veritabanı oturumu sağlar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

