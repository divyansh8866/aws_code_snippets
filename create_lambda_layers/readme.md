"""
Documentation for Creating AWS Lambda Layers with Docker
========================================================

This script allows users to create an AWS Lambda Layer for specified Python libraries using an Amazon Linux Docker container. The script will install the required libraries, package them, and upload the layer to AWS Lambda.

**Requirements**
----------------
- Docker must be installed and running.
- AWS CLI and `boto3` must be installed and configured with the appropriate credentials and permissions to publish Lambda layers.
- Python 3.7, 3.8, or 3.9 (installed in the Docker container).

**Usage**
---------
Run the script with the following flags:

- `--libraries`: List of Python libraries to include in the Lambda layer.
  - Example: `--libraries requests numpy`
- `--python_version`: Python version to use (`3.7`, `3.8`, `3.9`).
  - Example: `--python_version 3.8`
- `--layer_name`: Name of the Lambda Layer to create.
  - Example: `--layer_name my_layer`

**Example Command**
-------------------
```sh
python main.py --libraries requests numpy --python_version 3.8 --layer_name my_layer
```

**Steps Performed by the Script**
---------------------------------
1. **Docker Container Creation**: Spins up an Amazon Linux Docker container compatible with the given Python version.
2. **Library Installation**: Installs the specified libraries in the Docker container.
3. **Layer Packaging**: Packages the installed libraries into a `.zip` file suitable for AWS Lambda.
4. **Layer Upload**: Uploads the zip file to AWS Lambda using `boto3` to create a Lambda layer.
5. **Cleanup**: Stops and removes the Docker container after the layer is created.

**Notes**
---------
- Ensure that you have proper AWS credentials configured to use `boto3` for uploading the layer.
- The Docker container will be stopped and removed automatically after the script completes.
- The script requires network access to download the Python libraries and interact with AWS services.
"""
