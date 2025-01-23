from django.db import models
from django.contrib.auth.models import User as DjangoUser
from datetime import datetime
import os


# Create your models here.
def photo_path(instance, filename):
    ext = filename.split(".")[-1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return f"profile_photos/{instance.user}_{timestamp}.{ext}"


class User(models.Model):
    user = models.OneToOneField(
        DjangoUser, on_delete=models.CASCADE, related_name="profile"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)
    profile_photo = models.ImageField(
        upload_to=photo_path, default="profile_photos/blank.jpg"
    )

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = User.objects.get(pk=self.pk)
                if (
                    old_instance.profile_photo
                    and old_instance.profile_photo != self.profile_photo
                    and old_instance.profile_photo.name != "profile_photos/blank.jpg"
                ):

                    try:
                        os.remove(old_instance.profile_photo.path)
                    except (ValueError, FileNotFoundError):
                        pass
            except User.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
