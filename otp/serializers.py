from rest_framework import serializers
from otp.models import OTP

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ('otp',)
