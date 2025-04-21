from django.shortcuts import render
from datetime import datetime
from .mws_tables_api import get_lessons_for_student, get_top_ups_for_student

def profile_widget(request):
    return render(request, "widgets/profile.html")

def upcoming_lessons(request):
    ctx = {
        "lessons": [{
            "name": lesson["fields"]["fldWlV2f1MwD6"],
            "timestamp": datetime.fromtimestamp(float(lesson["fields"].get("fldel098OyCPy", [0])[0] / 1000)).strftime("%m/%d %H:%M"),
            "teacher": lesson["fields"].get("fldtgZIud1ueb", ["Неизвестный преподаватель"]),
        } for lesson in get_lessons_for_student(request.user.student.record_id)],
    }
    return render(request, "widgets/upcoming_lessons.html", ctx)

def my_courses(request):
    top_ups = get_top_ups_for_student(request.user.student.record_id)
    ctx = {

        "remainders": {
            "lessons": sum(top_up["fields"]["fldVQEeC9Kb5W"] for top_up in top_ups if not top_up["fields"].get("fldpavkG8PU1T", False)),
            "webinars": sum(top_up["fields"]["fldVQEeC9Kb5W"] for top_up in top_ups if top_up["fields"].get("fldpavkG8PU1T", False))
        },
        "my_courses": [{
            "name": top_up["fields"]["fldizm0JJHPBk"],
            "lessons_total": top_up["fields"]["fldLi57XZEtSj"],
            "lessons_left": top_up["fields"]["fldVQEeC9Kb5W"],
            "subject": top_up["fields"].get("fldaM4OkDpvsv", "Без названия"),
        } for top_up in top_ups],
    }

    return render(request, "widgets/my_courses.html", ctx)

def top_ups(request):
    top_ups = get_top_ups_for_student(request.user.student.record_id)
    ctx = {
        "top_ups": [{
            "amount": top_up["fields"]["fldLwLp9iloyo"],
            "payment_date": datetime.fromtimestamp(float(top_up["fields"]["fldyKwMfQoxC2"] / 1000)),
            "reason": top_up["fields"]["fldizm0JJHPBk"],
        } for top_up in top_ups],
    }
    return render(request, "widgets/top_ups.html", ctx)
