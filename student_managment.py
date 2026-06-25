
from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

FILE = "students.json"


def load_students():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_students(students):
    with open(FILE, "w") as f:
        json.dump(students, f, indent=4)


@app.route("/")
def home():

    students = load_students()

    search = request.args.get("search", "")

    if search:
        students = [
            s for s in students
            if search.lower() in s["name"].lower()
            or search.lower() in s["roll"].lower()
        ]

    total = len(load_students())

    all_students = load_students()

    if total > 0:
        avg = round(
            sum(float(s["cgpa"]) for s in all_students)
            / total,
            2
        )
    else:
        avg = 0

    departments = len(
        set(
            s["department"]
            for s in all_students
        )
    )

    return render_template(
        "index.html",
        students=students,
        total=total,
        avg=avg,
        departments=departments,
        search=search,
        edit_student=None
    )


@app.route("/add", methods=["POST"])
def add_student():

    students = load_students()

    roll = request.form["roll"]

    for s in students:
        if s["roll"] == roll:
            return redirect("/")

    student = {
        "roll": roll,
        "name": request.form["name"],
        "department": request.form["department"],
        "cgpa": request.form["cgpa"]
    }

    students.append(student)

    save_students(students)

    return redirect("/")


@app.route("/delete/<roll>")
def delete_student(roll):

    students = load_students()

    students = [
        s for s in students
        if s["roll"] != roll
    ]

    save_students(students)

    return redirect("/")


@app.route("/edit/<roll>")
def edit_student_page(roll):

    students = load_students()

    edit_student = None

    for s in students:
        if s["roll"] == roll:
            edit_student = s
            break

    total = len(students)

    if total > 0:
        avg = round(
            sum(float(s["cgpa"]) for s in students)
            / total,
            2
        )
    else:
        avg = 0

    departments = len(
        set(
            s["department"]
            for s in students
        )
    )

    return render_template(
        "index.html",
        students=students,
        total=total,
        avg=avg,
        departments=departments,
        search="",
        edit_student=edit_student
    )


@app.route("/update/<roll>", methods=["POST"])
def update_student(roll):

    students = load_students()

    for s in students:

        if s["roll"] == roll:

            s["name"] = request.form["name"]
            s["department"] = request.form["department"]
            s["cgpa"] = request.form["cgpa"]

    save_students(students)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

