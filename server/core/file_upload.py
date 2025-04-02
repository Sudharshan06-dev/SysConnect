from fastapi import UploadFile, Depends
from fastapi.responses import FileResponse
from typing import List
from sqlalchemy.orm import Session
from config.database import get_db
import boto3
import os
from concurrent.futures import ThreadPoolExecutor
from core.constants import SUCCESS, ERROR
from core.utility import create_response
from core.envs import Envs
from models import DocumentsModel
from constants import FileCategoryStatus
from context_vars import user_id_ctx
import asyncio

s3_client = boto3.client(
        "s3",
        aws_access_key_id = Envs.AWS_ACCESS_KEY,
        aws_secret_access_key = Envs.AWS_SECRET_KEY,
        region=Envs.S3_REGION
)

executor = ThreadPoolExecutor(max_workers=5)

def upload_to_s3(file, bucket, s3_key):
    """Upload file synchronously to S3"""
    s3_client.upload_fileobj(file, bucket, s3_key)
    return f"{Envs.S3_BASE_URL}/{bucket}/{s3_key}"

async def upload_files(files: List[UploadFile], reference_name: str, db: Session = Depends(get_db)):

    try:
        bucket_name, file_reference_name = reference_name.split("_", 1)
    except:
        return create_response(400, "invalid_bucket_name", ERROR)
    
    uploaded_files = []

    for file in files:

        file_ext = os.path.splitext(file.filename)[1]

        s3_key = f"{file_reference_name}/"

        if file_reference_name == FileCategoryStatus.ASSIGNMENT:
            s3_key += f"{user_id_ctx}/"

        s3_key += f"{file.filename}"

        #Run s3 upload in seperate thread to prevent blocking
        file_url = await asyncio.get_event_loop().run_in_executor(executor, upload_to_s3, file.file, bucket_name, s3_key)

        new_document = DocumentsModel(
            reference_id = user_id_ctx,
            file_name = file.filename,
            bucket_name=bucket_name,
            reference_link = file_url,
            reference_name = file_reference_name,
            extension = file_ext
        )

        db.add(new_document)
        db.commit()
        db.refresh(new_document)

        uploaded_files.append({"file": file.filename, "url": file_url})
    
    return create_response(200, "files_uploaded", SUCCESS)

async def download_file(filepath: str, file_name: str, ext: str):
    return FileResponse(filepath, media_type= f"application/{ext}", filename=file_name)