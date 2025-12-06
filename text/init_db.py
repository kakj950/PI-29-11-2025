# text/init_db.py
import sqlite3

# База будет создана прямо здесь — в папке text
DATABASE = "Base.md"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Создаём таблицы, если их нет
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

# Добавляем тестовые данные, только если таблица пуста
if cursor.execute("SELECT COUNT(*) FROM tasks").fetchone()[0] == 0:
    cursor.executemany(
        "INSERT INTO tasks (title, deadline, priority, category, user_id, completed_at, reminder_time) VALUES (?,?,?,?,?,?,?)",
        [
            (
                "Администрирование и поддержка приложения",
                "Бессрочно",
                "Высокий",
                "A",
                "1",
                "Постоянно",
                "Отсутствует",
            ),
            (
                "Программирование и отладка",
                "4 месяца",
                "Высокий",
                "A",
                "2",
                "Апрель",
                "Каждые 5 минут",
            ),
            (
                "Дизайн интерфейса и иконки приложения",
                "4 месяца",
                "Средне-высокий",
                "B",
                "3",
                "Апрель",
                "Каждые 5 минут",
            ),
            ("Поиск багов", "4 месяца", "Высокий", "C", "3", "Апрель", "Отсутствует"),
            (
                "Разработка креативной рекламы и продвижение",
                "2 месяца",
                "Средний",
                "D",
                "4",
                "Постоянно",
                "Отсутствует",
            ),
        ],
    )

    cursor.executemany(
        "INSERT INTO users (name, role) VALUES (?, ?)",
        [
            ("Иван", "Администратор"),
            ("Петр", "программист"),
            ("Павел", "дизайнер"),
            ("Степан", "тестировщик"),
            ("Олег", "тестировщик"),
            ("СТАНИСЛАВ", "СММ-специалист"),
        ],
    )

conn.commit()
conn.close()
print("✅ База данных Base.md успешно инициализирована в папке 'text'.")
