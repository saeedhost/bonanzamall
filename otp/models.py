from django.db import models
from django.contrib.auth.models import User

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_entries', related_query_name='otp_entry')
    otp = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

