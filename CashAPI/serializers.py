from rest_framework import serializers
from .models import CashValueModel

class PostNoteAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashValueModel
        fields = "__all__"
