# CSV to Parquet on Amazon S3

This script lists CSV objects in an S3 bucket, cleans each file with pandas,
converts it to Parquet, and uploads the result to a target bucket. Files are
processed concurrently with a process pool.

## Requirements

- Python 3.10 or newer
- Access to AWS S3

## Setup on Windows

Open PowerShell in this folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Configure AWS and buckets

In `interview.py`, set `SOURCE_BUCKET` and `TARGET_BUCKET` to the bucket
names you want to use. Configure AWS credentials using a standard Boto3
credential provider, such as an AWS profile or environment variables. Do not
put AWS credentials in this project.

The AWS identity needs permission to list and read objects in the source bucket
and write objects in the target bucket (`s3:ListBucket`, `s3:GetObject`, and
`s3:PutObject` as appropriate).

## Run

From this folder, with the virtual environment activated:

```powershell
python interview.py
```

Successful files are uploaded with the `.parquet` extension. The script reports
failed file names in its output. The timing decorator appends start and end
timestamps to `method_timing.log` in this folder; that generated log is ignored
by Git.
