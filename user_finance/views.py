from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from CashAPI.models import RupifyUser
from CashAPI.utils import decrypt_note
from .serializers import UserSerializer,UserNotePostSerializer,HistorySerializer
from .models import HistoryModel
class UserDetailsView(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,*args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    def post(self,request,*args, **kwargs):
        serializer = UserNotePostSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            saved_notes = serializer.save()
            return Response({"saved_notes": saved_notes}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class HistoryView(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,*args, **kwargs):
        history_instances = HistoryModel.objects.filter(user = request.user)
        serializer = HistorySerializer(history_instances,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        serializer = HistorySerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response({"msg": "Successfully Saved"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetNameView(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,*args, **kwargs):
        note = request.data.get("note")
        
        if not note:
            return Response({"error":"Please Provide note"},status=status.HTTP_400_BAD_REQUEST)
        try:
            note = note.split("::")[0]
        except:
            pass
        
        try:
            note = decrypt_note(note.encode()).split("::")[0]
        except:
            return Response({"error":"Invalid Note"},status=status.HTTP_400_BAD_REQUEST)
    
        user = get_object_or_404(RupifyUser, aadhar_number = note)
        return Response({"first_name":user.first_name,"last_name":user.last_name},status=status.HTTP_200_OK)