from rest_framework.views import APIView
from rest_framework_simplejwt import authentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from CashAPI.models import RupifyUser
from .serializers import UserSerializer,UserNotePostSerializer

class UserDetailsView(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request,*args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        print(serializer.data)
        return Response(serializer.data)
    def post(self,request,*args, **kwargs):
        serializer = UserNotePostSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            saved_notes = serializer.save()
            return Response({"saved_notes": saved_notes}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)