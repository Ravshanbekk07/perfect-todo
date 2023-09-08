from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task,Category
from django.contrib.auth.password_validation import validate_password

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model=Task
        fields='__all__'

    
    def to_representation(self, instance):
        return {
            'id':instance.id,
            'title':instance.title,
            'description':instance.description,
            'priority':instance.priority,
            'category':instance.category,
            'due_date':instance.due_date,
            'completed':instance.completed,
        }
    
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields='__all__'

    def validate_category(self,value):
        if not Category.objects.filter(user=self.context['request'].user,name=value).exists():
            raise serializers.ValidationError('This category does not exist')
        return value
    
    def validate_priority(self,value):
        if value not in ['low','medium','high']:
            raise serializers.ValidationError('Invalid priority')
        return value
    
    def validate(self,data):
        if Task.objects.filter(user=self.context['request'].user,title=data['title']).exists():
            raise serializers.ValidationError('This tasl already exists')
        return data


    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'title': instance.title,
            'description': instance.description,
            'priority': instance.priority,
            'category': instance.category.name,
            'due_date': instance.due_date,
            'completed': instance.completed
        }
    

