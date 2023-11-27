from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SendOTP, VerifyOTP,
    CenterViewSet, DepartmentViewSet, ProblemTypeViewSet, 
    StaffViewSet, ExpertViewSet, ProblemViewSet,
    FileAttachmentViewSet, NotificationViewSet, CommentViewSet,
    ProblemHistoryViewSet  # Import the new viewset
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'centers', CenterViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'problem_types', ProblemTypeViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'experts', ExpertViewSet)
router.register(r'problems', ProblemViewSet)
router.register(r'file_attachments', FileAttachmentViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'problem_history', ProblemHistoryViewSet, basename='problem-history')  # Register the new viewset

# Combine all urlpatterns
urlpatterns = [
    path('', include(router.urls)),
    path('send_otp/', SendOTP.as_view(), name='send_otp'),
    path('verify_otp/', VerifyOTP.as_view(), name='verify_otp'),
    # ... other url patterns if any
]
