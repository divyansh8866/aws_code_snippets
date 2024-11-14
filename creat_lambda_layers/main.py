import os
import subprocess
import sys
import argparse
import textwrap
import boto3

def run_command(command):
    result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result.stdout

def get_amazon_linux_version(python_version):
    if python_version == '3.7':
        return 'amazonlinux:2'
    elif python_version == '3.8':
        return 'amazonlinux:2'
    elif python_version == '3.9':
        return 'amazonlinux:2023'
    else:
        print(f"Unsupported Python version: {python_version}")
        sys.exit(1)

def create_docker_container(python_version):
    amazon_linux_version = get_amazon_linux_version(python_version)
    print(f"Spinning up Docker container for {amazon_linux_version}...")
    container_id = run_command(f"docker run -d {amazon_linux_version} tail -f /dev/null").strip()
    return container_id

def install_libraries(container_id, libraries, python_version):
    print(f"Installing libraries {libraries} for Python {python_version}...")
    python_command = f"python{python_version}"
    # Install Python, PIP, and required libraries in the container
    commands = [
        f"docker exec {container_id} yum install -y python{python_version} python{python_version}-pip zip",
        f"docker exec {container_id} {python_command} -m pip install {' '.join(libraries)} -t /python/lib/{python_command}/site-packages/"
    ]
    for command in commands:
        run_command(command)

def create_lambda_layer(container_id, python_version):
    print("Creating Lambda Layer zip file...")
    layer_dir = f"/python/lib/python{python_version}/site-packages"
    zip_file = f"lambda_layer_{python_version}.zip"
    # Zip the contents of the library directory
    run_command(f"docker exec {container_id} zip -r /tmp/{zip_file} {layer_dir}")
    # Copy the zip file from the container to the host machine
    run_command(f"docker cp {container_id}:/tmp/{zip_file} ./")
    print(f"Lambda Layer zip file created: {zip_file}")
    return zip_file

def upload_lambda_layer(zip_file, layer_name, python_version):
    print(f"Uploading Lambda Layer {zip_file} to AWS...")
    client = boto3.client('lambda')
    with open(zip_file, 'rb') as f:
        response = client.publish_layer_version(
            LayerName=layer_name,
            Description=f"Lambda layer for Python {python_version} containing specified libraries",
            Content={'ZipFile': f.read()},
            CompatibleRuntimes=[f'python{python_version}']
        )
    layer_arn = response['LayerVersionArn']
    print(f"Lambda Layer uploaded successfully. ARN: {layer_arn}")
    return layer_arn

def cleanup(container_id):
    print("Stopping and removing Docker container...")
    run_command(f"docker stop {container_id}")
    run_command(f"docker rm {container_id}")

def main():
    parser = argparse.ArgumentParser(
        description="Create an AWS Lambda Layer for given Python libraries using an Amazon Linux Docker container",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--libraries', type=str, nargs='+', required=True, help='Names of the libraries to create a Lambda Layer for (e.g., requests numpy)')
    parser.add_argument('--python_version', type=str, choices=['3.7', '3.8', '3.9'], required=True,
                        help=textwrap.dedent('''\
                            Python version to use (must be one of the supported Lambda Python versions):
                            3.7, 3.8, 3.9'''))
    parser.add_argument('--layer_name', type=str, required=True, help='Name of the Lambda Layer to create')

    args = parser.parse_args()
    libraries = args.libraries
    python_version = args.python_version
    layer_name = args.layer_name

    container_id = create_docker_container(python_version)
    try:
        install_libraries(container_id, libraries, python_version)
        zip_file = create_lambda_layer(container_id, python_version)
        upload_lambda_layer(zip_file, layer_name, python_version)
    finally:
        cleanup(container_id)

if __name__ == '__main__':
    main()
