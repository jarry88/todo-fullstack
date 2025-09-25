from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/todos/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos/", response_model=List[schemas.Todo])
def read_todos(
    skip: int = 0,
    limit: int = 100,
    filter: str = Query(None, enum=["all", "active", "completed"]),
    db: Session = Depends(get_db)
):
    query = db.query(models.Todo)
    if filter == "active":
        query = query.filter(models.Todo.completed == False)
    elif filter == "completed":
        query = query.filter(models.Todo.completed == True)
    return query.offset(skip).limit(limit).all()

@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}

@app.delete("/todos/clear/completed")
def clear_completed(db: Session = Depends(get_db)):
    db.query(models.Todo).filter(models.Todo.completed == True).delete()
    db.commit()
    return {"message": "Completed todos cleared successfully"}

@app.delete("/todos/clear/all")
def clear_all(db: Session = Depends(get_db)):
    db.query(models.Todo).delete()
    db.commit()
    return {"message": "All todos cleared successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
