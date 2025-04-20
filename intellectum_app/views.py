from datetime import datetime
from itertools import count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login

from intellectum_app import schemas
from intellectum_app.forms import RegistrationForm
from intellectum_app.models import Student
from intellectum_app.mws_tables_api import create_student, get_courses, get_homework_for_student, get_lessons_for_student, get_top_ups_for_student
# Create your views here.

@login_required(login_url="login")
def home_view(request):
    top_ups = get_top_ups_for_student(request.user.student.record_id)
    ctx = {
        "lessons": [{
            "name": lesson["fields"]["fldWlV2f1MwD6"],
            "timestamp": datetime.fromtimestamp(float(lesson["fields"]["fldel098OyCPy"] / 1000)).strftime("%m/%d %H:%M"),
            "teacher": lesson["fields"]["fldtgZIud1ueb"],
        } for lesson in get_lessons_for_student(request.user.student.record_id)],
        "top_ups": [{
            "amount": top_up["fields"]["fldLwLp9iloyo"],
            "payment_date": datetime.fromtimestamp(float(top_up["fields"]["fldyKwMfQoxC2"] / 1000)),
            "reason": top_up["fields"]["fldizm0JJHPBk"],
        } for top_up in top_ups],
        "remainders": {
            "lessons": sum(top_up["fields"]["fldVQEeC9Kb5W"] for top_up in top_ups if not top_up["fields"].get("fldpavkG8PU1T", False)),
            "webinars": sum(top_up["fields"]["fldVQEeC9Kb5W"] for top_up in top_ups if top_up["fields"].get("fldpavkG8PU1T", False))
        },
        "my_courses": [{
            "name": top_up["fields"]["fldizm0JJHPBk"],
            "lessons_total": top_up["fields"]["fldLi57XZEtSj"],
            "lessons_left": top_up["fields"]["fldVQEeC9Kb5W"],
            "subject": top_up["fields"]["fldaM4OkDpvsv"],
            "teacher": top_up["fields"]["fldv8OBSrmomJ"],
        } for top_up in top_ups],
        "homeworks": [{
            "name": homework["fields"]["fldArS5YpMMcC"],
            "deadline": datetime.fromtimestamp(float(homework["fields"]["fldX7OYBgfiCa"] / 1000)),
            "subject": homework["fields"]["fldfTDM50MknX"],
        } for homework in get_homework_for_student(request.user.student.record_id)]
    }
    return render(request, "home.html", context=ctx)


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid(): 
            user = form.save(commit=False)
            response = create_student(schemas.Student(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                phone_number=form.cleaned_data["phone_number"]
            ))
            print(response)

            student = Student(
                user=user,
                record_id=response["data"]["records"][0]["recordId"],
                phone_number=form.cleaned_data["phone_number"]
            )
            user.save()
            student.save()
            login(request, user, backend="axes.backends.AxesBackend")
            return redirect("home")
    else:
        form = RegistrationForm()
    return render(request, "auth/registration.html", {"form": form})

def courses_view(request):
    courses = get_courses()
    ctx = {
        "lesson_packs": [{
            "name": course["fields"]["fldY5f13r1xgH"],
            "amount_of_lessons": course["fields"]["fldTBASKhdEKR"],
            "price": course["fields"]["fld4NtsH75kp3"],
        } for course in courses if not course["fields"].get("fldOAMaXPHe84", False) ],
        "webinar_subscriptions": [{
            "name": course["fields"]["fldY5f13r1xgH"],
            "amount_of_lessons": course["fields"]["fldTBASKhdEKR"],
            "price": course["fields"]["fld4NtsH75kp3"],
        } for course in courses if course["fields"].get("fldOAMaXPHe84", False) ]
    }
    return render(request, "courses.html", ctx)

