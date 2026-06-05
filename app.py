from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

FILE_NAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", encoding="utf-8") as file:
        return json.load(file)


def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=4)


@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    tasks = load_tasks()

    title = request.form["title"]

    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "completed": False
    }

    tasks.append(new_task)

    save_tasks(tasks)

    return redirect("/")


@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]

    save_tasks(tasks)

    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    tasks = load_tasks()

    tasks = [task for task in tasks if task["id"] != task_id]

    save_tasks(tasks)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)