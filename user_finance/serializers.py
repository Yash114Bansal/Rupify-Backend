from rest_framework import serializers
from CashAPI.models import RupifyUser
from .models import PurposeModel,UserNotesModel,HistoryModel
from json import loads
class AadharNumberField(serializers.CharField):
    def to_representation(self, value):
        if value:
            return value[:4] + '*' * (len(value) - 4)
        return value

class PurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurposeModel
        fields = ["purpose"]

class UserNotePostSerializer(serializers.Serializer):
    notes = serializers.ListField(child=serializers.CharField(max_length=200))

    def create(self, validated_data):
        notes_data = loads(validated_data.get('notes')[0])
        user = self.context['request'].user
        
        saved_notes = []
        
        for note_content in notes_data:
            try:
                user_note = UserNotesModel.objects.create(user=user, note=note_content)
                saved_notes.append(user_note.note)
            except:
                pass
        
        return saved_notes

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

    class Meta:
        model = RupifyUser
        fields = ["aadhar_number","phone","user_Picture", "first_name", "last_name","purposes","notes"]

class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = HistoryModel
        fields = ['second_user', 'amount', 'time']