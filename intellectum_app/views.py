from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from intellectum_app import schemas
from intellectum_app.forms import RegistrationForm, UploadFileForm
from intellectum_app.models import Student
from intellectum_app.mws_tables_api import add_solution_file_to_homework, create_student, get_courses, get_homework_for_student, get_lessons_for_student, get_top_ups_for_student
# Create your views here.

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def home_view(request):
    ctx = {
        "homeworks": [{
            "name": homework["fields"].get("fldArS5YpMMcC", "Без названия"),
            "deadline": datetime.fromtimestamp(float(homework["fields"]["fldX7OYBgfiCa"] / 1000)),
            "is_submitted": homework["fields"].get("fldKpDnOEwKj2", False),
            "is_reviewed": homework["fields"].get("fldCSZcH1yrK3", False),
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

@login_required(login_url="login")
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

@login_required(login_url="login")
def assignments_view(request):
    assignments = get_homework_for_student(request.user.student.record_id)
    ctx = {
        "assignments": [{
            "name": homework["fields"].get("fldArS5YpMMcC", "Без названия"),
            "deadline": datetime.fromtimestamp(float(homework["fields"]["fldX7OYBgfiCa"] / 1000)),
            "subject": homework["fields"]["fldfTDM50MknX"],
            "text": homework["fields"].get("flddYDiTNr5Yh", "Без текста").split("\n"),
            "attachments": homework["fields"].get("fldnGDxeNPH3s", []),
            "id": homework["recordId"],
            "is_submitted": homework["fields"].get("fldKpDnOEwKj2", False),
            "mark": homework["fields"].get("fldRVEvZ8YorH", 0),
            "is_reviewed": homework["fields"].get("fldCSZcH1yrK3", False),
            "review": homework["fields"].get("fldZv2Jw9O2xg", "").split("\n")
        } for homework in assignments]
    }

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # add_solution_file_to_homework(request.user.student.record_id, request.POST["id"], request.FILES["file"])
            pass
        else:
            print("form invalid")
            print(form.errors)
    return render(request, "assignments.html", ctx)
