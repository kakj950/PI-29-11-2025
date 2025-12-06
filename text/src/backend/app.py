import os
import sqlite3

from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

# Путь к базе данных (оставляем как было)
DATABASE = os.path.join(os.path.dirname(__file__), "..", "..", "Base.md")


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    conn = get_db_connection()
    filter_type = request.args.get("filter", "all")

    if filter_type == "active":
        tasks = conn.execute(
            'SELECT * FROM tasks WHERE completed_at = "Постоянно" OR completed_at = ""'
        ).fetchall()
    elif filter_type == "completed":
        tasks = conn.execute(
            'SELECT * FROM tasks WHERE completed_at != "Постоянно" AND completed_at != ""'
        ).fetchall()
    else:  # all
        tasks = conn.execute("SELECT * FROM tasks").fetchall()

    total = len(tasks)
    completed = len(
        [
            t
            for t in tasks
            if t["completed_at"] != "Постоянно" and t["completed_at"] != ""
        ]
    )
    active = total - completed

    conn.close()

    stats = {"total": total, "completed": completed, "active": active}

    return render_template(
        "tasks_list.html", tasks=tasks, stats=stats, filter=filter_type
    )


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.form

    required_fields = [
        "title",
        "deadline",
        "priority",
        "category",
        "user_id",
        "completed_at",
        "reminder_time",
    ]
    for field in required_fields:
        if field not in data:
            return "Missing field: " + field, 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO tasks (title, deadline, priority, category, user_id, completed_at, reminder_time)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            data["title"],
            data["deadline"],
            data["priority"],
            data["category"],
            data["user_id"],
            data["completed_at"],
            data["reminder_time"],
        ),
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    conn = get_db_connection()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not task:
        conn.close()
        return "Task not found", 404

    # Переключаем статус: если было "Постоянно" или пусто — делаем датой, иначе — обратно
    new_status = (
        "Постоянно"
        if task["completed_at"] != "Постоянно" and task["completed_at"] != ""
        else "Апрель"
    )
    # В реальном проекте лучше использовать метку "is_completed" или дату выполнения
    # Здесь упрощённо: меняем на "Апрель" как пример завершения

    conn.execute(
        "UPDATE tasks SET completed_at = ? WHERE id = ?", (new_status, task_id)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
