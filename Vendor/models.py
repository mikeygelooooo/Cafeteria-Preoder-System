from django.db import models


# Create your models here.
class Stall(models.Model):
    stall_no = models.IntegerField()
    stall_name = models.CharField(max_length=100)
    stall_desc = models.TextField(blank=True, null=True)
    is_open = models.BooleanField(default=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return f"Stall No. {self.stall_no} - {self.stall_name}"
    
class Vendor(models.Model):
    user = models.OneToOneField("User.User", on_delete=models.CASCADE)
    stall = models.ForeignKey("Stall", on_delete=models.CASCADE, related_name="vendors")

    def __str__(self):
        return f"{self.user} - {self.stall.stall_name}"