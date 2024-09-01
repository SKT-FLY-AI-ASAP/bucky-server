from datetime import datetime
from starlette import status
from fastapi import UploadFile

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import io

from core.config import settings
from core.exceptions import BaseCustomException


S3_ACCESS_KEY = settings.S3_ACCESS_KEY
S3_PRIVATE_KEY = settings.S3_PRIVATE_KEY
S3_BUCKET_NAME = settings.S3_BUCKET_NAME
S3_REGION_NAME = settings.S3_REGION_NAME


def datetime_to_str(date: datetime):
    if not date:
        return None

    return date.strftime('%Y-%m-%d %H:%M:%S')


def check_file_extension(filename, valid_ext):
    return filename.lower().endswith(valid_ext)

async def add_to_s3(object_name: str, file: UploadFile, content_type: str = 'image/png'):
    s3_cli = boto3.client(
        's3',
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_PRIVATE_KEY,
        region_name=S3_REGION_NAME
    )

    try:
        with file.file as file_obj:
            s3_cli.upload_fileobj(
                Fileobj=file_obj,
                Bucket=S3_BUCKET_NAME,
                Key=object_name,
                ExtraArgs={'ContentType': content_type})
        return f"https://{S3_BUCKET_NAME}.s3.{S3_REGION_NAME}.amazonaws.com/{object_name}"
    except NoCredentialsError:
        raise BaseCustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AWS credentials not found."
        )
    except PartialCredentialsError:
        raise BaseCustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Incomplete AWS credentials provided."
        )
    except Exception as e:
        raise BaseCustomException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )
