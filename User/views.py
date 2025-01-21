from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
    update_session_auth_hash,
)
from django.contrib import messages
from .forms import (
    LoginForm,
    SignupForm,
    EditProfileForm,
    ChangePasswordForm,
    DeleteAccountForm,
)


# Create your views here.
@login_required(login_url="user-login")
def profile(request):
    user = request.user

    profile = user.profile

    context = {
        "profile": profile,
    }

    return render(request, "user/profile.html", context)


@login_required(login_url="user-login")
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()

            messages.success(request, "Profile edited successfully!")

            return redirect("user-profile")

    else:
        form = EditProfileForm(instance=request.user.profile)

    context = {
        "form": form,
    }

    return render(request, "user/edit_profile.html", context)


@login_required(login_url="user-login")
def order_history(request):
    return render(request, "user/order_history.html")


@login_required(login_url="user-login")
def account_settings(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()

            update_session_auth_hash(request, user)

            messages.success(request, "Password successfully updated!")

            return redirect("user-profile")

    else:
        form = ChangePasswordForm(request.user)

    context = {
        "form": form,
    }

    return render(request, "user/account_settings.html", context)


@login_required
def delete_account(request):
    if request.method == "POST":
        form = DeleteAccountForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data["password"]

            if request.user.check_password(password):
                user_profile = request.user.profile

                logout(request)

                user_profile.delete()

                messages.success(request, "Your account has been successfully deleted.")

                return redirect("index")
            else:
                messages.error(request, "Incorrect password. Please try again.")
    else:
        form = DeleteAccountForm()

    return render(request, "user/delete_account.html", {"form": form})


def signup(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()

            auth_login(request, user)

            messages.success(request, "Account created successfully!")

            return redirect("index")

    else:
        form = SignupForm()

    context = {"form": form}

    return render(request, "user/signup.html", context)


def login(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get("remember_me")

            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)

                if not remember_me:
                    request.session.set_expiry(0)

                next_page = request.GET.get("next", "index")

                return redirect(next_page)

            else:
                messages.error(request, "Invalid username or password.")

    else:
        form = LoginForm()

    context = {"form": form}

    return render(request, "user/login.html", context)


@login_required(login_url="user-login")
def logout(request):
    if request.method == "POST":
        auth_logout(request)

    return redirect("user-login")
