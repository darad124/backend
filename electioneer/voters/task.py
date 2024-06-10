import logging
from django.core.cache import cache
from .email_utils import send_email_notification
import pandas as pd
from .models import Student
from .serializers import StudentSerializer
import os
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)

def process_file_task(file_path, file_extension, task_id):
    logger.info(f"Task {task_id} started: processing file {file_path} with extension {file_extension}")
    try:
        result = process_file(file_path, file_extension)
        logger.info(f"Task {task_id} completed: {result}")

        cache.set(task_id, result, timeout=3600)
        logger.info(f"Stored task result in cache with task ID: {task_id}")

        if 'success_count' in result and result['success_count'] > 0:
            logger.info("Sending email notification for successful file processing")
            send_email_notification(
                subject='File Processing Successful',
                body=f'The file has been successfully processed. {result["success_count"]} student records have been updated.',
                recipient_email=settings.ADMIN_EMAIL
            )
            logger.info("Email notification sent")
        return result

    except Exception as e:
        error_message = f"Task {task_id} failed: {str(e)}"
        logger.error(error_message, exc_info=True)
        cache.set(task_id, {'error': error_message}, timeout=3600)
        logger.info(f"Stored error in cache with task ID: {task_id}")
        return {'error': error_message}
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Temporary file {file_path} deleted")
            except Exception as e:
                logger.error(f"Failed to delete temporary file {file_path}: {str(e)}")

def process_file(file_path, file_extension):
    try:
        logger.debug(f"Reading file: {file_path} with extension: {file_extension}")
        
        if file_extension == '.csv':
            data = pd.read_csv(file_path, encoding='utf-8')
        else:
            data = pd.read_excel(file_path)
        logger.debug(f"File read successfully: {file_path}")

        required_columns = ['student_id', 'first_name', 'last_name', 'email', 'year_of_study', 'faculty', 'is_eligible']
        missing_columns = [column for column in required_columns if column not in data.columns]

        if missing_columns:
            error_message = f'Missing columns in file: {", ".join(missing_columns)}'
            logger.error(error_message)
            return {'error': error_message}

        errors = []
        success_count = 0
        existing_count = 0

        for index, row in data.iterrows():
            date_of_birth = row.get('date_of_birth')
            if isinstance(date_of_birth, datetime):
                date_of_birth = date_of_birth.date()
            
            student_data = {
                'student_id': row['student_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'date_of_birth': date_of_birth,
                'year_of_study': row['year_of_study'],
                'faculty': row['faculty'],
                'is_eligible': str(row['is_eligible']).strip().lower() in ['yes', 'y', 'true', 't', '1'],
            }

            logger.debug(f"Processing row {index + 1}: {student_data}")

            if Student.objects.filter(student_id=row['student_id']).exists():
                existing_count += 1
                continue

            serializer = StudentSerializer(data=student_data)
            if not serializer.is_valid():
                logger.debug(f"Validation failed for row {index + 1}: {serializer.errors}")
                errors.append({'row': index + 1, 'errors': serializer.errors})
                continue

            try:
                serializer.save()
                success_count += 1
                logger.debug(f"Successfully saved row {index + 1}")
            except Exception as e:
                logger.error(f"Failed to save student record at row {index + 1}: {str(e)}")
                errors.append({'row': index + 1, 'errors': str(e)})

        result = {
            'message': f'File processed. {success_count} new records added. {existing_count} records already existed.',
            'errors': errors,
            'success_count': success_count,
            'existing_count': existing_count
        }
        logger.info(f"File processed with result: {result}")

        return result

    except pd.errors.EmptyDataError:
        error_message = 'The uploaded file is empty.'
        logger.error(error_message)
        return {'error': error_message}
    except pd.errors.ParserError:
        error_message = 'The uploaded file has a parsing issue.'
        logger.error(error_message)
        return {'error': error_message}
    except UnicodeDecodeError:
        error_message = 'The uploaded file encoding is invalid.'
        logger.error(error_message)
        return {'error': error_message}
    except ValueError as e:
        error_message = f'Value error in file: {e}'
        logger.error(error_message)
        return {'error': error_message}
    except KeyError as e:
        error_message = f'Missing expected column in file: {e}'
        logger.error(error_message)
        return {'error': error_message}
    except Exception as e:
        error_message = f'An unexpected error occurred: {str(e)}'
        logger.error(error_message, exc_info=True)
        return {'error': error_message}
