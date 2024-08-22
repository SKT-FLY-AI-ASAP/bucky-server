from datetime import datetime
from starlette import status
from fastapi import File

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

from core.config import settings
from core.exceptions import BaseCustomException


def datetime_to_str(date: datetime):
    if not date:
        return None

    return date.strftime('%Y-%m-%d %H:%M:%S')


def check_file_extension(filename, valid_ext):
    return filename.lower().endswith(valid_ext)


def add_to_s3(object_name: str, file: File):
    S3_ACCESS_KEY = settings.S3_ACCESS_KEY
    S3_PRIVATE_KEY = settings.S3_PRIVATE_KEY
    S3_BUCKET_NAME = settings.S3_BUCKET_NAME

    s3_cli = boto3.client(
        's3',
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_PRIVATE_KEY,
        region_name='ap-northeast-2'
    )

    try:
        s3_cli.upload_fileobj(
            file.file,
            S3_BUCKET_NAME,
            object_name,
            ExtraArgs={'ContentType': 'image/png'})
        return f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{object_name}"
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
