from rest_framework import serializers
from django.contrib.auth import get_user_model


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'is_student', 'is_teacher']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        is_student = validated_data.get('is_student')
        is_teacher = validated_data.get('is_teacher')

        if is_student is None and is_teacher is None:
            raise serializers.ValidationError(
                "One must either be a student or a teacher")

        if is_student and is_teacher:
            raise serializers.ValidationError(
                "One cannot be a teacher and student at the same time")

        is_student = bool(is_student)
        is_teacher = bool(is_teacher)

        return get_user_model().objects.create_user(username=validated_data['username'],
                                                    email=validated_data['email'],
                                                    password=validated_data['password'],
                                                    is_student=is_student,
                                                    is_teacher=is_teacher,
                                                    )
