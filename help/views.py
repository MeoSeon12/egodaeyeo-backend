from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import FeedbackSerializer, ReportSerializer
from .models import Report as ReportModel

class FeedbackView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]

    #피드백 작성
    def post(self, request):
        user_id = request.user.id
        request.data['user'] = user_id
        feedback_serializer = FeedbackSerializer(data=request.data, context={"request": request})
        
        if feedback_serializer.is_valid():
            feedback_serializer.save()
            return Response(feedback_serializer.data, status=status.HTTP_200_OK)
        
        return Response(feedback_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReportView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]

    #신고 작성
    def post(self, request, item_id):
        user_id = request.user.id
        try:
            ReportModel.objects.get(user=user_id, item=item_id)
            return Response({'msg': '이미 신고한 물품입니다.'}, status=status.HTTP_208_ALREADY_REPORTED)

        except ReportModel.DoesNotExist:
            request.data['user'] = user_id
            request.data['item'] = item_id
            
            report_serializer = ReportSerializer(data=request.data, context={"request": request})
            
            if report_serializer.is_valid():
                report_serializer.save()
                return Response(report_serializer.data, status=status.HTTP_200_OK)
            
            return Response(report_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            