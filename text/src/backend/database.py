import sqlite3

conn = sqlite3.connect("Base.md")
cursor = conn.cursor()
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL
)
"""
)
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    deadline TEXT NOT NULL,
    priority TEXT NOT NULL,
    category TEXT NOT NULL,
    user_id TEXT NOT NULL,
    completed_at TEXT NOT NULL,
    reminder_time TEXT NOT NULL
)
"""
)
cursor.execute(
    "INSERT INTO tasks (title, deadline, priority, category, user_id, completed_at, reminder_time) VALUES (?,?,?,?,?,?,?)",
    (
        "Администрирование и поддержка приложения",
        "Бессрочно",
        "Высокий",
        "A",
        "1",
        "Постоянно",
        "Отсутствует",
    ),
)
cursor.execute(
    "INSERT INTO tasks (title, deadline, priority, category, user_id, completed_at, reminder_time) VALUES (?,?,?,?,?,?,?)",
    (
        "Программирование и отладка",
        "4 месяца",
        "Высокий",
        "A",
        "2",
        "Апрель",
        "Каждые 5 минут",
    ),
)
cursor.execute(
    "INSERT INTO tasks (title, deadline, priority, category, user_id, completed_at, reminder_time) VALUES (?,?,?,?,?,?,?)",
    (
        "Дизайн интерфейса и иконки приложения",
        "4 месяца",
        "Средне-высокий",
        "B",
        "3",
        "Апрель",
        "Каждые 5 минут",
    ),
)
cursor.execute(
    "INSERT INTO tasks (title, deadline, priority, category, user_id, completed_at, reminder_time) VALUES (?,?,?,?,?,?,?)",
    ("Поиск багов", "4 месяца", "Высокий", "C", "3", "Апрель", "Отсутствует"),
)
cursor.execute(
    "INSERT INTO tasks (title, deadline, priority, category, user_id, completed_at, reminder_time) VALUES (?,?,?,?,?,?,?)",
    (
        "Разработка креативной рекламы и продвижение",
        "2 месяца",
        "Средний",
        "D",
        "4",
        "Постоянно",
        "Отсутствует",
    ),
)
cursor.execute(
    "INSERT INTO users (name, role) VALUES (?, ?)", ("Иван", "Администратор")
)
cursor.execute("INSERT INTO users (name, role) VALUES (?, ?)", ("Петр", "программист"))
cursor.execute("INSERT INTO users (name, role) VALUES (?, ?)", ("Павел", "дизайнер"))
cursor.execute(
    "INSERT INTO users (name, role) VALUES (?, ?)", ("Степан", "тестировщик")
)
cursor.execute("INSERT INTO users (name, role) VALUES (?, ?)", ("Олег", "тестировщик"))
cursor.execute(
    "INSERT INTO users (name, role) VALUES (?, ?)", ("СТАНИСЛАВ", "СММ-специалист")
)
cursor.fetchall()
cursor.execute(" SELECT * FROM users ")
User = cursor.fetchall()
print(User)
cursor.execute(" SELECT * FROM tasks ")
Tasks = cursor.fetchall()
print(Tasks)
