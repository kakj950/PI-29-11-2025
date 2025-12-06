# tests/test_app.py
import os
import sqlite3
import tempfile
import pytest
from app import app, DATABASE


@pytest.fixture
def client():
    # Создаём временную копию БД во избежание порчи основной
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    
    # Патчим путь к БД в приложении
    app.config["TESTING"] = True
    original_db = app.config.get("DATABASE", DATABASE)
    app.config["DATABASE"] = db_path

    # Инициализируем БД (вручную, т.к. у вас нет schema.sql)
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            deadline TEXT,
            priority TEXT,
            category TEXT,
            user_id TEXT,
            completed_at TEXT,
            reminder_time TEXT
        )
    """)
    conn.commit()
    conn.close()

    with app.test_client() as client:
        yield client

    # Очистка
    os.close(db_fd)
    os.unlink(db_path)


def test_index_page_loads(client):
    """Проверяем, что главная страница загружается без ошибок."""
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"tasks_list.html" not in rv.data  # убеждаемся, что шаблон *рендерится*, но не как строка
    # Можно проверить наличие элементов, например:
    assert b"total" in rv.data or b"tasks" in rv.data.lower()


def test_create_task(client):
    """Тест: создание новой задачи через POST."""
    data = {
        "title": "Test Task",
        "deadline": "2025-12-31",
        "priority": "high",
        "category": "work",
        "user_id": "1",
        "completed_at": "",  # активная задача
        "reminder_time": "09:00",
    }

    rv = client.post("/tasks", data=data, follow_redirects=True)
    assert rv.status_code == 200

    # Проверяем, что задача появилась в списке
    assert b"Test Task" in rv.data


def test_toggle_task(client):
    """Тест: переключение статуса задачи."""
    # Сначала создаём задачу
    data = {
        "title": "Toggle Me",
        "deadline": "2025-12-31",
        "priority": "medium",
        "category": "test",
        "user_id": "1",
        "completed_at": "",  # изначально активна
        "reminder_time": "",
    }
    client.post("/tasks", data=data, follow_redirects=False)

    # Получаем ID задачи (берём первую из БД)
    db = sqlite3.connect(app.config["DATABASE"])
    cur = db.execute("SELECT id FROM tasks WHERE title = ?", ("Toggle Me",))
    task_id = cur.fetchone()[0]
    db.close()

    # Переключаем
    rv = client.post(f"/tasks/{task_id}/toggle", follow_redirects=True)
    assert rv.status_code == 200

    # Проверяем, что статус изменился (теперь не пустой и не 'Постоянно')
    db = sqlite3.connect(app.config["DATABASE"])
    cur = db.execute("SELECT completed_at FROM tasks WHERE id = ?", (task_id,))
    status = cur.fetchone()[0]
    db.close()

    assert status == "Апрель"  # как в коде toggle_task


def test_delete_task(client):
    """Тест: удаление задачи."""
    # Создаём задачу
    data = {"title": "To Delete", "deadline": "", "priority": "low", "category": "test",
            "user_id": "1", "completed_at": "", "reminder_time": ""}
    client.post("/tasks", data=data)

    # Получаем ID
    db = sqlite3.connect(app.config["DATABASE"])
    cur = db.execute("SELECT id FROM tasks WHERE title = ?", ("To Delete",))
    task_id = cur.fetchone()[0]
    db.close()

    # Удаляем
    rv = client.post(f"/tasks/{task_id}/delete", follow_redirects=True)
    assert rv.status_code == 200

    # Проверяем, что её больше нет
    db = sqlite3.connect(app.config["DATABASE"])
    cur = db.execute("SELECT COUNT(*) FROM tasks WHERE id = ?", (task_id,))
    count = cur.fetchone()[0]
    db.close()
    assert count == 0