Here is the complete FastAPI code for CRUD operations with SQLite, along with the `requirements.txt` file, saved under the `backend` directory.

**backend/main.py**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

DATABASE = 'news_website.db'

class Article(BaseModel):
    id: int = None
    title: str
    content: str
    category: str

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        category TEXT NOT NULL
                      )''')
    conn.commit()
    conn.close()

@app.on_event("startup")
async def startup():
    init_db()

@app.post("/articles/", response_model=Article)
async def create_article(article: Article):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO articles (title, content, category) VALUES (?, ?, ?)",
                   (article.title, article.content, article.category))
    article.id = cursor.lastrowid
    conn.commit()
    conn.close()
    return article

@app.get("/articles/", response_model=List[Article])
async def read_articles():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content, category FROM articles")
    articles = cursor.fetchall()
    conn.close()
    return [Article(id=row[0], title=row[1], content=row[2], category=row[3]) for row in articles]

@app.get("/articles/{article_id}", response_model=Article)
async def read_article(article_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content, category FROM articles WHERE id = ?", (article_id,))
    article = cursor.fetchone()
    conn.close()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return Article(id=article[0], title=article[1], content=article[2], category=article[3])

@app.put("/articles/{article_id}", response_model=Article)
async def update_article(article_id: int, article: Article):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE articles SET title = ?, content = ?, category = ? WHERE id = ?",
                   (article.title, article.content, article.category, article_id))
    conn.commit()
    conn.close()
    return article

@app.delete("/articles/{article_id}", response_model=Article)
async def delete_article(article_id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles WHERE id = ?", (article_id,))
    conn.commit()
    conn.close()
    return {"message": "Article deleted successfully"}
```

**backend/requirements.txt**

```
fastapi==0.95.2
uvicorn==0.21.1
pydantic==1.10.8
sqlite3
```

This setup provides a simple CRUD API for managing news articles, utilizing FastAPI for its performance and SQLite for its lightweight database needs. The `requirements.txt` lists necessary dependencies to run the application. The `init_db()` function initializes the SQLite database with a table for articles if it doesn't already exist.