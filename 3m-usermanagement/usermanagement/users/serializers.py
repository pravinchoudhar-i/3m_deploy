from rest_framework import serializers
from .models import *
from django.contrib.admin.models import LogEntry

# serializer to Retrieve, update or delete the Analysis model
class AnalysisDeleteSerializer(serializers.ModelSerializer):
    feedback = serializers.CharField(required=False)
    prediction = serializers.CharField(required=False)
    class Meta:
        model = Analysis
        fields = ['id', 'feedback', 'prediction', 'status']

# serializer to get or post the data of Analysis model
class AnalysisSerializer(serializers.ModelSerializer):
    # user_id = serializers.PrimaryKeyRelatedField(
    #    many=False, write_only=True, queryset=UserRegistration.objects.all()
    #     ,source='user',required=True
    #     )
    class Meta:
        model = Analysis
        fields = ['id','location', 'feedback', 'image', 'predictionType', 'predictionColor', 'feedbackType', 'feedbackColor', 'createdBy', 'createdAt','updatedBy','updatedAt', 'isFlash' ]

    # def get_image_url(self, analys):
    #     request = self.context.get('request')
    #     image_url = analys.image.url
    #     return request.build_absolute_uri(image_url)

class VersionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = VersionLog
        fields = ['id', 'versionNumber', 'description', 'dateOfRelease','askUpgrade']

 
