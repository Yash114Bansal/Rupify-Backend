from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CashValueModel,RupifyUser,OTP
from .serializers import PostNoteAmountSerializer,VerifyOTPSerializer
from random import randint
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken
from time import timezone
from django.utils import timezone
from .utils import SendOTP


class SendOTP(APIView):
        def post(self, request, *args, **kwargs):
            aadhar_number = request.data.get('aadhar_number')

            if not aadhar_number:
                return Response({'error': 'Missing aadhar_number'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = RupifyUser.objects.filter(aadhar_number=aadhar_number).first()
            if not user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            old_otp = OTP.objects.get(user=user)
            if old_otp:
                old_otp.delete()
            
            otp = randint(100000,999999)
                
            SendOTP(otp,user.phone)  
            expiry_time = timezone.now() + timezone.timedelta(minutes=5)
            OTP.objects.create(user=user, otp=otp, expiry_time=expiry_time)

            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)


class VerifyOTP(APIView):
     def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            aadhar_number = serializer.validated_data['aadhar_number']
            otp_value = serializer.validated_data['otp']
            user = RupifyUser.objects.filter(aadhar_number=aadhar_number).first()
            if not user:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            try:    
                otp_object = OTP.objects.get(user=user, otp=otp_value)
            except OTP.DoesNotExist:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
            if otp_object.has_expired():
                return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
            
            access_token = AccessToken.for_user(user)
            
            return Response({
                'access_token': str(access_token),
                'message': 'OTP verified successfully'
            }, status=status.HTTP_200_OK)
            # return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class NoteValue(APIView):
    def post(self,request,format = None):
        serializer = PostNoteAmountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Context":"Successfully saved value"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)