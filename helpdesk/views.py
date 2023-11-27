from django.shortcuts import render
from rest_framework import viewsets, filters
from .serializers import ProblemHistorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from .models import Center, Department, ProblemType, Staff, Expert, Problem, FileAttachment, Notification, Comment
from .serializers import (
    CenterSerializer, DepartmentSerializer, ProblemTypeSerializer, 
    StaffSerializer, ExpertSerializer, ProblemSerializer, 
    FileAttachmentSerializer, NotificationSerializer, CommentSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
#OTP Faraz SMS
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import OTP, User  # Import OTP and User models
from .utils import send_sms_via_farazsms
import random

class CenterViewSet(viewsets.ModelViewSet):
    queryset = Center.objects.all()
    serializer_class = CenterSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class ProblemTypeViewSet(viewsets.ModelViewSet):
    queryset = ProblemType.objects.all()
    serializer_class = ProblemTypeSerializer

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'department', 'role']
    search_fields = ['name', 'email', 'phone_number']
    ordering_fields = ['name', 'date_joined']

class ExpertViewSet(viewsets.ModelViewSet):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'specialization', 'status']
    search_fields = ['name', 'email']
    ordering_fields = ['name']

class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'status', 'problem_type', 'staff', 'expert']
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'submission_date', 'status']

    @action(detail=True, methods=['post'], url_path='upload-files')
    def upload_files(self, request, pk=None):
        problem = self.get_object()
        files = request.FILES.getlist('files')
        for file in files:
            FileAttachment.objects.create(problem=problem, staff=request.user.staff, file_path=file)
        return Response({"message": "Files uploaded successfully"}, status=status.HTTP_201_CREATED)

class ProblemHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProblemHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Assuming that the staff member is related to the user model via a OneToOne field
        staff_member = self.request.user.staff
        return Problem.objects.filter(staff=staff_member).order_by('-submission_date')        

class FileAttachmentViewSet(viewsets.ModelViewSet):
    queryset = FileAttachment.objects.all()
    serializer_class = FileAttachmentSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

#Send OTP End Point
class SendOTP(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp_code = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
        OTP.objects.create(phone_number=phone_number, otp_code=otp_code)  # Save OTP to the database
        send_sms_via_farazsms(phone_number, otp_code)  # Send OTP via SMS
        return Response({"message": "OTP sent successfully"}, status=200)

#Verify OTP Endpoint
class VerifyOTP(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp_code = request.data.get("otp_code")
        otp_instance = OTP.objects.filter(phone_number=phone_number, otp_code=otp_code).first()

        if otp_instance and otp_instance.is_valid():
            user, created = User.objects.get_or_create(phone_number=phone_number)
            # A session or token for the authenticated user
            return Response({"message": "OTP verified, user logged in"}, status=200)
        else:
            return Response({"message": "Invalid OTP"}, status=400)
