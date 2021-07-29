from rest_framework import serializers
from employee_app.models import  EmpModels

class EmpModelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpModels
        fields = '__all__'