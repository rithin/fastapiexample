from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from pydantic import BaseModel
from typing import List  # Import List from typing module

# Replace 'your_postgres_username', 'your_postgres_password', 'your_postgres_host', 'your_postgres_port', and 'your_postgres_db' with your actual PostgreSQL credentials
#DATABASE_URL = "postgresql+psycopg2://your_postgres_username:your_postgres_password@your_postgres_host:your_postgres_port/your_postgres_db"

DATABASE_URL = "postgresql+psycopg2://postgres:bigcity123@localhost:5433/fastapiexample"

# Create a SQLAlchemy database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# SQLAlchemy model for 'items' table
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create 'items' table in the database
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for creating an item
class ItemCreate(BaseModel):
    name: str
    description: str

# Pydantic model for the response
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

# CRUD operations
def create_item(db: Session, item: Item):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Item).offset(skip).limit(limit).all()

def update_item(db: Session, item_id: int, new_item: ItemCreate):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        for key, value in new_item.dict().items():
            setattr(item, key, value)
        db.commit()
        db.refresh(item)
    return item

def delete_item(db: Session, item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item

# FastAPI app instance
app = FastAPI()

# FastAPI routes
@app.post("/items/", response_model=ItemResponse)
def create_item_api(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(name=item.name, description=item.description)
    created_item = create_item(db, db_item)
    return ItemResponse(id=created_item.id, name=created_item.name, description=created_item.description)

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return ItemResponse(id=db_item.id, name=db_item.name, description=db_item.description)

@app.get("/items/", response_model=List[ItemResponse])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = get_items(db, skip=skip, limit=limit)
    return [ItemResponse(id=item.id, name=item.name, description=item.description) for item in items]

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item_api(item_id: int, new_item: ItemCreate, db: Session = Depends(get_db)):
    updated_item = update_item(db, item_id, new_item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return ItemResponse(id=updated_item.id, name=updated_item.name, description=updated_item.description)

@app.delete("/items/{item_id}", response_model=ItemResponse)
def delete_item_api(item_id: int, db: Session = Depends(get_db)):
    deleted_item = delete_item(db, item_id)
    if deleted_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return ItemResponse(id=deleted_item.id, name=deleted_item.name, description=deleted_item.description)