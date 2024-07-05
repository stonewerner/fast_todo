import os
from fastapi import FastAPI, Depends, Request, Form, status
from dotenv import load_dotenv
load_dotenv()

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session

import api.models as models
from api.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root(request: Request, db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return templates.TemplateResponse("base.html",
                                      {"request": request, "book_list":books})


@app.post("/add")
def add(request: Request, title: str = Form(...), author: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    new_book = models.Book(title=title, author=author, description=description)
    db.add(new_book)
    db.commit()

    url = app.url_path_for("root")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/update/{id}")
def update(request: Request, id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    book.read = not book.read
    db.commit()

    url = app.url_path_for("root")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@app.get("/delete/{id}")
def delete(request: Request, id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    db.delete(book)
    db.commit()

    url = app.url_path_for("root")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)