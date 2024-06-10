from rest_framework import serializers
from .models import Student, Election, VotingRecord
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

class StudentSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField()

    def to_internal_value(self, data):
        # Ensure we log the incoming data for debugging
        logger.debug(f"Incoming data for to_internal_value: {data}")
        
        if 'date_of_birth' in data and isinstance(data['date_of_birth'], str):
            try:
                data['date_of_birth'] = datetime.fromisoformat(data['date_of_birth']).date()
            except ValueError as e:
                logger.error(f"Error parsing date_of_birth: {e}")
        
        internal_value = super().to_internal_value(data)
        return internal_value

    def validate_date_of_birth(self, value):
        logger.debug(f"Validating date_of_birth: {value}")

        # Ensure value is a date object
        if isinstance(value, datetime):
            logger.debug(f"Converting datetime {value} to date.")
            return value.date()
        if not isinstance(value, date):
            logger.error(f"Invalid type for date_of_birth: {type(value)}")
            raise serializers.ValidationError("Invalid date format")
        return value

    class Meta:
        model = Student
        fields = '__all__'

class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = '__all__'

class VotingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotingRecord
        fields = '__all__'
