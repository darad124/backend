from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.core.cache import cache
import logging
import os
import tempfile
import uuid
from .models import Student, Election, VotingRecord
from .serializers import StudentSerializer, ElectionSerializer, VotingRecordSerializer
from .task import process_file_task

# Configure logging
logger = logging.getLogger(__name__)

def home(request):
    return HttpResponse("Welcome to the Election System")

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['year_of_study', 'is_eligible']
    search_fields = ['first_name', 'last_name', 'faculty']

class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer

class VotingRecordViewSet(viewsets.ModelViewSet):
    queryset = VotingRecord.objects.all()
    serializer_class = VotingRecordSerializer

# views.py
class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        logger.debug("Received a file upload request.")
        file = request.FILES.get('file')
        if not file:
            logger.error("No file provided in the request.")
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        file_name, file_extension = os.path.splitext(file.name)
        file_extension = file_extension.lower()

        logger.debug(f"Received file: {file_name} with extension: {file_extension}")

        if file_extension not in ['.csv', '.xlsx', '.xls']:
            logger.error(f"Invalid file extension: {file_extension}")
            return Response({'error': 'The uploaded file is not a CSV or Excel file.'}, status=status.HTTP_400_BAD_REQUEST)

        if file.size > 10 * 1024 * 1024:
            logger.error("Uploaded file size exceeds the limit.")
            return Response({'error': 'The uploaded file is too large.'}, status=status.HTTP_400_BAD_REQUEST)

        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        logger.debug(f"Temporary file created at: {temp_file_path}")

        task_id = str(uuid.uuid4())
        logger.info(f"Processing task {task_id} for file {file.name}")
        
        # Process file synchronously and get the result
        result = process_file_task(temp_file_path, file_extension, task_id)

        logger.info(f"File processed with task ID: {task_id}, result: {result}")
        return Response(result, status=status.HTTP_200_OK)

class TaskResultView(APIView):
    def get(self, request, task_id):
        logger.info(f"Fetching result for task ID {task_id}")
        result = cache.get(task_id)
        if result:
            logger.info(f"Result found for task ID {task_id}: {result}")
            return Response(result, status=status.HTTP_200_OK)
        logger.error(f"Task ID {task_id} not found.")
        return Response({'error': 'Task ID not found.'}, status=status.HTTP_404_NOT_FOUND)
