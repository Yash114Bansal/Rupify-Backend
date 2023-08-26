from rest_framework import serializers
from CashAPI.models import RupifyUser
from .models import PurposeModel,UserNotesModel

class AadharNumberField(serializers.CharField):
    def to_representation(self, value):
        if value:
            return value[:4] + '*' * (len(value) - 4)
        return value

class PurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurposeModel
        fields = ["purpose"]

class UserNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotesModel
        fields = ["note"]

class UserSerializer(serializers.ModelSerializer):
    aadhar_number = AadharNumberField(max_length=12)
    purposes = serializers.SerializerMethodField()
    notes = serializers.SerializerMethodField()
    def get_notes(self, obj):
        notes = UserNotesModel.objects.filter(user=obj).values_list("note", flat=True)
        return list(notes)

    def get_purposes(self, obj):
        purposes = PurposeModel.objects.filter(user=obj).values_list("purpose", flat=True)
        return list(purposes)
    
    def create(self, validated_data):
        user = self.context["request"].user  # Get the user from request.user
        notes_data = self.context["request"].data.get("notes", [])  # Get notes_data from request data
        print(notes_data)
        user_serializer = UserSerializer(user, data=validated_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        for note_number in notes_data:
            UserNotesModel.objects.create(user=user, note_number=note_number)
            print(note_number)

        return user    
    class Meta:
        model = RupifyUser
        fields = ["aadhar_number","phone","user_Picture", "first_name", "last_name","purposes","notes"]
