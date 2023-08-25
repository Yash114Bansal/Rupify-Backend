from rest_framework import serializers
from .models import CashValueModel,OTP

class PostNoteAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashValueModel
        fields = "__all__"

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['aadhar_number', 'otp', 'expiry_time']
        
class VerifyOTPSerializer(serializers.Serializer):
    aadhar_number = serializers.CharField(required=True)
    otp = serializers.CharField(required=True)