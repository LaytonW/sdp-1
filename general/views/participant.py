from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from ..models import Course,Participant,CompletedEnrollment,Category
from ..models import CurrentEnrollment
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from . import authenticate

@login_required
def participantIndex(request,participantID):
    if "Participant" not in list(map((lambda x:x.name),request.user.groups.all())):
        return redirect("myLogout")
    categoryList = Category.objects.all()
    participant = Participant.objects.get(id=participantID)
    try:
        currentEnrollment=participant.currentenrollment
    except ObjectDoesNotExist as e:
        currentCourse=None
    else:
        currentCourse=currentEnrollment.course
    completedCourses = participant.getCompletedCourses()
    return render(request,'general/participantIndex.html',{'categoryList':categoryList,'currentCourse':currentCourse,
        'completedCourses':completedCourses})

@login_required
def showCourseList(request,participantID):
    if "Participant" not in list(map((lambda x:x.name),request.user.groups.all())):
        return redirect("myLogout")
    if request.method=="POST":
        categoryID = request.POST.get("categoryID")
        courses = Category.objects.get(id=categoryID).getOpenedCourses()
        return HttpResponse(
            render_to_string("general/ajax/showCourseList.html",{'courses':courses})
        )

@login_required
def showCourse(request,participantID):
    if "Participant" not in list(map((lambda x:x.name),request.user.groups.all())):
        return redirect("myLogout")
    if request.method=="POST":
        courseID = request.POST.get('courseID')
        course = Course.objects.get(id=courseID)
        participant = Participant.objects.get(id=participantID)
        modules = course.module_set.all()
        return HttpResponse(
            render_to_string(
                "general/ajax/showCourse.html",
                {'course':course, 'hasEnrolled':participant.hasEnrolled(), 'modules':modules}
            )
        )

@login_required
def enroll(request,participantID):
    if "Participant" not in list(map((lambda x:x.name),request.user.groups.all())):
        return redirect("myLogout")
    if request.method == "POST":
        courseID = request.POST.get('courseID')
        course = Course.objects.get(id=courseID)
        participant = Participant.objects.get(id=participantID)
        result = participant.enroll(course)
        return JsonResponse({'result':result})
    return HttpResponse(status=404)