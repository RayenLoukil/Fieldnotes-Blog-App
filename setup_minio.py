"""
One-time setup script — creates bucket and sets public read policy for profile_pics.
Run once with: python setup_minio.py
"""
import json
import boto3
from config import settings

def main():
    client = boto3.client(
        "s3",
        region_name=settings.s3_region,
        aws_access_key_id=settings.s3_access_key_id.get_secret_value(),
        aws_secret_access_key=settings.s3_secret_access_key.get_secret_value(),
        endpoint_url=settings.s3_endpoint_url,
    )

    # Create bucket if it doesn't exist
    try:
        client.create_bucket(Bucket=settings.s3_bucket_name)
        print(f"Bucket '{settings.s3_bucket_name}' created.")
    except client.exceptions.BucketAlreadyOwnedByYou:
        print(f"Bucket '{settings.s3_bucket_name}' already exists.")

    # Set public read policy on profile_pics/ prefix only
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:GetObject"],
                "Resource": [
                    f"arn:aws:s3:::{settings.s3_bucket_name}/profile_pics/*"
                ]
            }
        ]
    }

    client.put_bucket_policy(
        Bucket=settings.s3_bucket_name,
        Policy=json.dumps(policy)
    )
    print("Public read policy set on profile_pics/*.")
    print("Setup complete.")

if __name__ == "__main__":
    main()