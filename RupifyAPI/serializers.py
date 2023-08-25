
from rest_framework import serializers
from .models import DepositeUserModel
class DepositeMoneySerializer(serializers.Serializer):
    note_number = serializers.CharField(max_length=200)
    note_purpose = serializers.IntegerField()
    aadhar_number = serializers.CharField(max_length = 12)