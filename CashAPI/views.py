from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CashValueModel
from .serializers import PostNoteAmountSerializer
# Create your views here.

class NoteValue(APIView):

    def post(self,request,format = None):
        serializer = PostNoteAmountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Context":"Successfully saved value"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)