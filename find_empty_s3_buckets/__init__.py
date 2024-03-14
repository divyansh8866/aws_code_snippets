import boto3
import configparser

def read_config(filename='main.config'):
    config = configparser.ConfigParser()
    config.read(filename)
    aws_access_key_id = config['AWS']['aws_access_key_id']
    aws_secret_access_key = config['AWS']['aws_secret_access_key']
    aws_region = config['AWS']['aws_region']
    return aws_access_key_id, aws_secret_access_key, aws_region

def list_empty_buckets():
    # Read AWS credentials and region from config file
    aws_access_key_id, aws_secret_access_key, aws_region = read_config()

    # Create an S3 client
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

    # List all S3 buckets
    response = s3.list_buckets()

    # Iterate through each bucket and check if it's empty
    empty_buckets = []
    for bucket in response['Buckets']:
        bucket_name = bucket['Name']

        # List objects in the bucket
        objects = s3.list_objects_v2(Bucket=bucket_name)

        # Check if the bucket is empty
        if 'Contents' not in objects or len(objects['Contents']) == 0:
            empty_buckets.append(bucket_name)

    return empty_buckets

if __name__ == "__main__":
    empty_buckets = list_empty_buckets()

    if empty_buckets:
        print("Empty buckets:")
        for bucket in empty_buckets:
            print(bucket)
    else:
        print("No empty buckets found.")
