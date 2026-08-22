"""
Quick diagnostic — verify MinIO/S3 credentials and permissions.
Run with: python check_s3.py
"""
import sys
import boto3
from botocore.exceptions import ClientError
from config import settings


def main():
    print(f"Bucket : {settings.s3_bucket_name}")
    print(f"Region : {settings.s3_region}")
    print(f"Endpoint: {settings.s3_endpoint_url or 'AWS S3 (default)'}")

    kwargs = {"region_name": settings.s3_region}
    if settings.s3_endpoint_url:
        kwargs["endpoint_url"] = settings.s3_endpoint_url
    if settings.s3_access_key_id and settings.s3_secret_access_key:
        kwargs["aws_access_key_id"] = settings.s3_access_key_id.get_secret_value()
        kwargs["aws_secret_access_key"] = settings.s3_secret_access_key.get_secret_value()

    client = boto3.client("s3", **kwargs)
    test_key = "profile_pics/_connection_test.txt"

    try:
        client.put_object(
            Bucket=settings.s3_bucket_name,
            Key=test_key,
            Body=b"test",
            ContentType="text/plain",
        )
        print("Upload : SUCCESS")
    except ClientError as err:
        print(f"Upload : FAILED — {err}")
        sys.exit(1)

    try:
        client.delete_object(Bucket=settings.s3_bucket_name, Key=test_key)
        print("Delete : SUCCESS")
    except ClientError as err:
        print(f"Delete : FAILED — {err}")
        sys.exit(1)

    print("\nAll tests passed. Configuration is working.")


if __name__ == "__main__":
    main()