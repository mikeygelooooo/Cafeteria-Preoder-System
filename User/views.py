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
    ChangePhotoForm,
    ChangePasswordForm,
    DeleteAccountForm,
)
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
import sys


# Create your views here.
@login_required(login_url="user-login")
def profile(request):
    profile = request.user.profile

    context = {
        "profile": profile,
    }

    return render(request, "user/profile.html", context)


@login_required(login_url="user-login")
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()

            messages.success(request, "Profile edited successfully!")

            return redirect("user-profile")

    else:
        form = EditProfileForm(instance=request.user.profile)

    context = {
        "profile": profile,
        "form": form,
    }

    return render(request, "user/edit_profile.html", context)


def crop_photo(image):
    image = image.convert("RGB")

    # Get dimensions
    width, height = image.size
    crop_size = min(width, height)

    # Center crop
    left = (width - crop_size) // 2
    top = (height - crop_size) // 2
    right = left + crop_size
    bottom = top + crop_size

    image = image.crop((left, top, right, bottom))
    image = image.resize((300, 300), Image.Resampling.LANCZOS)

    return image


@login_required(login_url="user-login")
def change_photo(request):
    user_profile = request.user.profile

    if request.method == "POST":
        form = ChangePhotoForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            try:
                # Open and process the uploaded image
                upload = request.FILES["profile_photo"]
                photo = Image.open(upload)
                processed_photo = crop_photo(photo)

                # Save processed image to in-memory file
                buffer = BytesIO()
                processed_photo.save(buffer, format="JPEG", quality=90)
                buffer.seek(0)

                # Create InMemoryUploadedFile
                processed_file = InMemoryUploadedFile(
                    buffer,
                    "ImageField",
                    f"{upload.name.split('.')[0]}.jpg",
                    "image/jpeg",
                    buffer.getbuffer().nbytes,
                    None,
                )

                user_profile.profile_photo = processed_file
                user_profile.save()

                messages.success(request, "Profile photo updated successfully.")
            except Exception as e:
                messages.error(request, f"Error processing image: {str(e)}")
        else:
            messages.error(request, "Invalid form submission")

        return redirect("user-profile")
    else:
        form = ChangePhotoForm(instance=user_profile)

    context = {
        "form": form,
    }

    return render(request, "user/change_photo.html", context)


@login_required(login_url="user-login")
def order_history(request):
    profile = request.user.profile

    context = {
        "profile": profile,
    }

    return render(request, "user/order_history.html", context)


@login_required(login_url="user-login")
def account_settings(request):
    profile = request.user.profile

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
        "profile": profile,
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
