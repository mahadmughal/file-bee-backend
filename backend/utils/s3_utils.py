import boto3
from django.conf import settings
from botocore.exceptions import ClientError


class S3Client:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(S3Client, cls).__new__(cls)
            cls._instance.client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )
        return cls._instance

    def get_object(self, key):
        try:
            response = self.client.get_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=key
            )
            return response['Body'].read()
        except ClientError as e:
            print(f"Error getting object {key} from bucket {
                  settings.AWS_STORAGE_BUCKET_NAME}. Error: {e}")
            return None

    def generate_download_link(self, key, expiration=3600):
        """
        Generate a pre-signed URL for downloading a file.

        :param key: The key of the file in the S3 bucket
        :param expiration: The number of seconds the pre-signed URL is valid for (default is 1 hour)
        :return: A pre-signed URL as a string, or None if there's an error
        """
        try:
            response = self.client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': key
                },
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            print(f"Error generating pre-signed URL for {key}: {e}")
            return None


# Global instance
s3_client = S3Client()
