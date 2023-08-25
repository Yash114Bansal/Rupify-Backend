from django.shortcuts import render,HttpResponse
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import DepositeMoneySerializer
from .models import DepositeUserModel,PendingNoteModel
from CashAPI.models import RupifyUser
from CashAPI.utils import encrypt_note,decrypt_note
from json import loads
from re import sub
class DepositedMoneyView(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = DepositeMoneySerializer(data=request.data)
        if serializer.is_valid():
            note_number = serializer.validated_data["note_number"]
            note_purpose = serializer.validated_data["note_purpose"]
            aadhar_number = serializer.validated_data["aadhar_number"]
            user = RupifyUser.objects.filter(
                aadhar_number=aadhar_number).first()
            if not user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            deposit = DepositeUserModel.objects.create(user=user, note_number=note_number, note_purpose=note_purpose)

            return Response({"message": "Deposit successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetMoneyView(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        notes = DepositeUserModel.objects.filter(user=user)
        list_notes = []
        for n in notes:
            list_notes.append(encrypt_note(n.note_number,user.aadhar_number,n.note_purpose))
        notes.delete()
        return Response({"notes":list_notes},status=status.HTTP_200_OK)

class TransferNoteView(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            list_notes = loads(request.data.get("data"))
        except:
            return Response({"error":"Please Give list of Valid notes"}, status=status.HTTP_400_BAD_REQUEST)
        pending_list = []
        final_return_list = []

        for notes in list_notes:
            try:
                notes = notes.split("::")[0]
            except:
                pass

            try:
                sender_aadhar, note_number = decrypt_note(notes.encode()).split("::")
            except:
                return Response({'error': 'Invalid Note'}, status=status.HTTP_400_BAD_REQUEST)

            if sender_aadhar == request.user.aadhar_number:
                return Response({"error":"Transfer to self not allowed"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = RupifyUser.objects.filter(aadhar_number=sender_aadhar).first()
                if not user:
                    return Response({'error': 'Invalid Note'}, status=status.HTTP_400_BAD_REQUEST)
                pending_notes_database = PendingNoteModel.objects.get(user = user,note_number=notes)
                pending_list.append(pending_notes_database.note_number)
            except:
                pass
        if pending_list:
            return Response({"notes": pending_list},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        for notes in list_notes:
            try:
                notes = notes.split("::")[0]
            except:
                pass
            
            sender_aadhar, note_number = decrypt_note(notes.encode()).split("::")
            note_number = sub(r'[^\x20-\x7E]+', '',note_number.encode().decode("utf-8", "ignore"))
            user = RupifyUser.objects.filter(aadhar_number=sender_aadhar).first()
            PendingNoteModel.objects.create(user=user,note_number = notes)
            new_encrypted_note = encrypt_note(note_number,request.user.aadhar_number,0)
            final_return_list.append(new_encrypted_note)


        return Response({"notes":final_return_list},status=status.HTTP_200_OK)

class GetPendingNoteView(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        pending_list = []
        Pending_Notes = PendingNoteModel.objects.filter(user = request.user)
        for notes in Pending_Notes:
            pending_list.append(notes.note_number)
        Pending_Notes.delete()
        return Response({"notes":pending_list},status=status.HTTP_200_OK)