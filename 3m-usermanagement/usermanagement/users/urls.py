from django.urls import path
from .views import *

urlpatterns = [
    
    # login
    path('', AdminLogin.as_view(), name='admin-login'),
    # tables
    path('users/', ViewUsers.as_view(), name='view-users'),
    path('view-admin/', ViewAdmin.as_view(), name='view-admins'),
    path('feedback/', FeedbackTable.as_view(), name='view-feedback'),

    # apis
    path('api/analysis', FeedbackAPIView.as_view(),name="analysis-api"),
    path('api/analysis/<int:pk>/', FeedbackAPIViewDetail.as_view(),name="analysis-details-api"),
    path('api/otp', SendOtpAPIView.as_view(),name="otp-api"),
    path('api/bulk-feedback', BulkFeedbackAPIView.as_view(),name="bulk-feedback-api"),
    path('api/version/update', VersionLogAPIView.as_view(),name="version-api"),
    path('api/feedback-entry', FeedbackEntriesAPIView.as_view(),name="feedback-entry-api"),
    path('api/fetch-data',FetchData.as_view(), name='fetch-data-api'),
  

]