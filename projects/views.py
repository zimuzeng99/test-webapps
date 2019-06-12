from django.shortcuts import render, redirect
from django.http import HttpResponse
import geopy.distance
from . import models
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from users import models as users_models

@csrf_exempt
def project_signup(request):
    if request.method == "POST":
        signup_user(request.user, models.Project.objects.get(id=int(request.POST["projectid"])))
        return redirect("view_project", project_id=int(request.POST["projectid"]))

def signup_user(user, project):
    entries = models.Volunteer.objects.all()
    for entry in entries:
        if entry.user.username == user.username and entry.project.id == project.id:
            return False
    volunteerEntry = models.Volunteer()
    volunteerEntry.user = user
    volunteerEntry.project = project
    volunteerEntry.save()
    return True

def my_projects(request):
    projects = models.Project.objects.all()
    volunteer_projects = []
    organise_projects = []
    for project in projects:
        if project.organiser.username == request.user.username:
            organise_projects.append(project)

    volunteers = models.Volunteer.objects.all()
    for entry in volunteers:
        if entry.user.username == request.user.username:
            volunteer_projects.append(entry.project)

    return render(request, "projects/my-projects.html", {"volunteer_projects": volunteer_projects, "organise_projects": organise_projects})

def signup_group(request):
    if request.method == "POST":
        group_names = request.POST.getlist("groups")
        membership = users_models.GroupMember.objects.all()
        users = []
        visited = []
        for entry in membership:
            for name in group_names:
                if entry.group.name == name and entry.user.username not in visited:
                    visited.append(entry.user.username)
                    users.append(entry.user)
                    break
        project = models.Project.objects.get(id=int(request.POST["projectid"]))
        for user in users:
            signup_user(user, project)
        return redirect("view_project", project_id=project.id)


def certify_project(request):
    if request.method == "POST":
        project = models.Project.objects.get(id=int(request.POST["projectid"]))

        for key in request.POST:
            if key == "projectid" or key == "csrfmiddlewaretoken":
                continue

            user = User.objects.get(username=key)
            if project.type == "Environmental":
                user.profile.hours_environmental += int(request.POST[key])
            elif project.type == "Social":
                user.profile.hours_social += int(request.POST[key])
            elif project.type == "Educational":
                user.profile.hours_educational += int(request.POST[key])

            user.save()

            completedEntry = models.CompletedProject()
            completedEntry.user = user
            completedEntry.project = project
            completedEntry.save()

        project.completed = True
        project.save()

        return redirect("/")

def filter_projects(projects, minduration, maxduration, maxdistance, latitude, longitude):
    output = []

    if latitude == None:
        latitude = 51.498833
    if longitude == None:
        longitude = -0.175113

    for project in projects:
        if minduration != None and project.duration < minduration:
            continue
        if maxduration != None and project.duration > maxduration:
            continue

        user_location = (latitude, longitude)
        project_location = (project.latitude, project.longitude)
        distance = geopy.distance.distance(user_location, project_location).km

        if maxdistance != None and distance > maxdistance:
            continue

        project.distance = int(distance)

        if project.completed:
            continue

        output.append(project)
    return output


def homepage(request):
    projects = models.Project.objects.all()
    for project in projects:
        project.duration = int(project.duration)

    minduration = None
    if "minduration" in request.GET and request.GET["minduration"]:
        minduration = float(request.GET["minduration"])

    maxduration = None
    if "maxduration" in request.GET and request.GET["maxduration"]:
        maxduration = float(request.GET["maxduration"])

    maxdistance = None
    if "maxdistance" in request.GET and request.GET["maxdistance"]:
        maxdistance = float(request.GET["maxdistance"])

    latitude = None
    longitude = None
    if "latitude" in request.GET and request.GET["latitude"]:
        latitude = float(request.GET["latitude"])
        longitude = float(request.GET["longitude"])

    output = filter_projects(projects, minduration, maxduration, maxdistance, latitude, longitude)
    output.sort(key=lambda project : project.distance)

    if latitude == None:
        latitude = 51.498833
        longitude = -0.175113

    return render(request, "projects/home.html", { "projects": output, "minduration": minduration, "maxduration": maxduration, "maxdistance": maxdistance, "latitude": latitude, "longitude": longitude })

def create_project(request):
    if request.method == "POST":
        project = models.Project()
        project.title = request.POST["title"]
        project.description = request.POST["description"]
        project.latitude = request.POST["latitude"]
        project.longitude = request.POST["longitude"]
        project.type = request.POST["type"]
        project.duration = float(request.POST["duration"])
        project.organiser = User.objects.all()[0]
        project.save()

        project = models.Project.objects.get(title=project.title)

        return redirect("/projects/" + str(project.id) + "/")

def view_project(request, project_id):
    project = models.Project.objects.get(pk=int(project_id))
    project.duration = int(project.duration)
    project.volunteers = []
    volunteerEntries = models.Volunteer.objects.all()
    for entry in volunteerEntries:
        if int(entry.project.id) == int(project_id):
            project.volunteers.append(entry.user)
    project.num_volunteers = len(project.volunteers)
    all_groups = users_models.Group.objects.all()
    groups = []
    for group in all_groups:
        if group.admin == request.user:
            groups.append(group)
    return render(request, "projects/project.html", { "project": project, "groups": groups })
