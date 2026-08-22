import uuid
from io import BytesIO

import boto3
from botocore.exceptions import ClientError
from PIL import Image, ImageOps
from starlette.concurrency import run_in_threadpool

from config import settings

PROFILE_PICS_PREFIX = "profile_pics"


def _get_s3_client():
    if settings.s3_access_key_id and settings.s3_secret_access_key:
        return boto3.client(
            "s3",
            region_name=settings.s3_region,
            aws_access_key_id=settings.s3_access_key_id.get_secret_value(),
            aws_secret_access_key=settings.s3_secret_access_key.get_secret_value(),
            endpoint_url=settings.s3_endpoint_url,
        )
    return boto3.client(
        "s3",
        region_name=settings.s3_region,
        endpoint_url=settings.s3_endpoint_url,
    )


def process_profile_image(content: bytes) -> tuple[bytes, str]:
    with Image.open(BytesIO(content)) as original:
        img = ImageOps.exif_transpose(original)
        img = ImageOps.fit(img, (300, 300), method=Image.Resampling.LANCZOS)
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")
        filename = f"{uuid.uuid4().hex}.jpg"
        output = BytesIO()
        img.save(output, "JPEG", quality=85, optimize=True)
        output.seek(0)
        return output.read(), filename


def _upload_to_s3(file_bytes: bytes, key: str) -> None:
    client = _get_s3_client()
    client.put_object(
        Bucket=settings.s3_bucket_name,
        Key=key,
        Body=file_bytes,
        ContentType="image/jpeg",
    )


def _delete_from_s3(key: str) -> None:
    client = _get_s3_client()
    client.delete_object(
        Bucket=settings.s3_bucket_name,
        Key=key,
    )


async def upload_profile_image(file_bytes: bytes, filename: str) -> None:
    key = f"{PROFILE_PICS_PREFIX}/{filename}"
    await run_in_threadpool(_upload_to_s3, file_bytes, key)


async def delete_profile_image(filename: str | None) -> None:
    if filename is None:
        return
    key = f"{PROFILE_PICS_PREFIX}/{filename}"
    await run_in_threadpool(_delete_from_s3, key)