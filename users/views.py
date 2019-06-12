from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from projects import models as project_models

BRONZE_HOURS = 20
SILVER_HOURS = 100
GOLD_HOURS = 200

def hours_to_level(hours):
    if hours < BRONZE_HOURS:
        return None
    if hours < SILVER_HOURS:
        return "Bronze"
    if hours < GOLD_HOURS:
        return "Silver"
    return "Gold"

def leaderboard(request):
    users = []
    for user in User.objects.all():
        users.append(user)

    users.sort(key=lambda user : user.profile.total_hours(), reverse=True)
    return render(request, "users/leaderboard.html", {"users": users})

def my_groups(request, username):
    group_membership = models.GroupMember.objects.all()
    groups = []
    for entry in group_membership:
        if entry.user.username == username:
            groups.append(entry.group)
    return render(request, "users/my-groups.html", {"groups": groups})

def create_group(request):
    if request.method == "GET":
        return render(request, "users/create-group.html")
    new_group = models.Group()
    new_group.name = request.POST["name"]
    new_group.description = request.POST["description"]
    new_group.admin = request.user
    new_group.save()
    new_group = models.Group.objects.get(name=new_group.name)

    membershipEntry = models.GroupMember()
    membershipEntry.user = request.user
    membershipEntry.group = new_group
    membershipEntry.save()
    return redirect("view_group_profile", group_id=new_group.id)

def add_member(request):
    user = User.objects.get(username=request.POST["username"])
    membershipEntry = models.GroupMember()
    membershipEntry.user = user
    membershipEntry.group = models.Group.objects.get(id=int(request.POST["groupid"]))
    membershipEntry.save()
    return redirect("view_group_profile", group_id=int(request.POST["groupid"]))

def view_user_profile(request, username):
    user = User.objects.get(username=username)
    user.awards = []
    if hours_to_level(user.profile.total_hours()) != None:
        user.awards.append((hours_to_level(user.profile.total_hours()), "Commitment"))
    if hours_to_level(user.profile.hours_environmental) != None:
        user.awards.append((hours_to_level(user.profile.hours_environmental), "Environmental"))
    if hours_to_level(user.profile.hours_social) != None:
        user.awards.append((hours_to_level(user.profile.hours_social), "Social"))
    if hours_to_level(user.profile.hours_educational) != None:
        user.awards.append((hours_to_level(user.profile.hours_educational), "Educational"))

    user.complete_projects = []
    completed = project_models.CompletedProject.objects.all()
    for entry in completed:
        if entry.user.username == username:
            user.complete_projects.append(entry.project)

    if user.profile.total_hours() < BRONZE_HOURS:
        user.hours_difference = BRONZE_HOURS - user.profile.total_hours()
        user.progress_value = user.profile.total_hours() / BRONZE_HOURS
        user.tier = "ROOKIE"
        user.word_right = "BRONZE"
        user.color = "bronze"
    elif user.profile.total_hours() < SILVER_HOURS:
        user.hours_difference = SILVER_HOURS - user.profile.total_hours()
        user.progress_value = int((user.profile.total_hours() - BRONZE_HOURS) / (SILVER_HOURS - BRONZE_HOURS) * 100)
        user.tier = "BRONZE"
        user.word_right = "SILVER"
        user.tier_img = "Bronze-Commitment"
        user.color = "silver"
    elif user.profile.total_hours() < GOLD_HOURS:
        user.hours_difference = GOLD_HOURS - user.profile.total_hours()
        user.progress_value = int((user.profile.total_hours() - SILVER_HOURS) / (GOLD_HOURS - SILVER_HOURS) * 100)
        user.tier_img = "Silver-Commitment"
        user.tier = "SILVER"
        user.word_right = "GOLD"
        user.color = "gold"
    else:
        user.tier_img = "Gold-Commitment"
        user.tier = "GOLD"

    return render(request, "users/profile.html", { "user": user, "BRONZE_HOURS": BRONZE_HOURS, "SILVER_HOURS": SILVER_HOURS, "GOLD_HOURS": GOLD_HOURS })

def view_group_profile(request, group_id):
    group = models.Group.objects.get(pk=int(group_id))
    group_membership = models.GroupMember.objects.all()
    group.members = []
    for entry in group_membership:
        if int(entry.group.id) == int(group_id):
            group.members.append(entry.user)
    group.num_members = len(group.members)

    return render(request, "users/group.html", { "group": group })

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("view_user_profile", username=user.username)
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("/")

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            if "firstname" in request.POST:
                user.first_name = request.POST["firstname"]
            if "lastname" in request.POST:
                user.last_name = request.POST["lastname"]
            if "bio" in request.POST:
                user.profile.bio = request.POST["bio"]
            if "email" in request.POST:
                user.profile.email = request.POST["email"]
            if "phone" in request.POST:
                user.profile.phone = request.POST["phone"]
            user.profile.type = request.POST["type"]
            user.save()
            login(request, user)
            return redirect("view_user_profile", username=user.username)
    else:
        form = UserCreationForm()
    return render(request, "users/signup.html", {"form": form})
