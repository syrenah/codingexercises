from concurrent.futures import ProcessPoolExecutor
from io import BytesIO
import logging
from pathlib import PurePosixPath
from typing import List

import boto3
import pandas as pd
from mydecorators import log_times, retry

SOURCE_BUCKET = "source-bucket"
TARGET_BUCKET = "target-bucket"
MAX_WORKERS = 4

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(processName)s %(message)s",
)
logger = logging.getLogger(__name__)


def build_s3_client():
    return boto3.client("s3")


@retry(tries=3)
def list_csv_files(bucket: str) -> List[str]:
    """
    Return all CSV object keys from an S3 bucket.
    """

    s3 = build_s3_client()

    paginator = s3.get_paginator("list_objects_v2")

    csv_files = []

    for page in paginator.paginate(Bucket=bucket):
        for obj in page.get("Contents", []):
            key = obj["Key"]

            if key.lower().endswith(".csv"):
                csv_files.append(key)

    return csv_files


@log_times
def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    df = df.drop_duplicates()
    df = df.dropna(how="all")

    return df


def convert_key_to_parquet(key: str) -> str:
    return str(
        PurePosixPath(key).with_suffix(".parquet")
    )


@retry(tries=3)
def download_csv(s3, key: str):
    return s3.get_object(
        Bucket=SOURCE_BUCKET,
        Key=key,
    )


@log_times
@retry(tries=3)
def upload_parquet(
    key: str,
    s3,
    target_key: str,
    parquet_buffer: BytesIO,
) -> None:
    logger.debug("Uploading Parquet for %s to %s.", key, target_key)
    s3.put_object(
        Bucket=TARGET_BUCKET,
        Key=target_key,
        Body=parquet_buffer.getvalue(),
    )


@log_times
def process_file(key: str) -> dict:
    """
    Download CSV, clean data,
    convert to parquet, upload result.
    """

    try:
        s3 = build_s3_client()

        obj = download_csv(s3, key)

        df = pd.read_csv(obj["Body"])
        df = clean_dataframe(df)

        parquet_buffer = BytesIO()
        df.to_parquet(
            parquet_buffer,
            engine="pyarrow",
            compression="snappy",
            index=False,
        )

        target_key = convert_key_to_parquet(key)
        upload_parquet(key, s3, target_key, parquet_buffer)

        return {
            "status": "success",
            "source": key,
            "target": target_key,
        }
    except Exception as exc:
        logger.error("Failed to process %s: %s", key, exc)
        return {
            "status": "failed",
            "source": key,
            "error": str(exc),
        }


def main():

    csv_files = list_csv_files(SOURCE_BUCKET)
    logger.info("Found %d CSV files to process.", len(csv_files))

    # Separate processes can run the pandas cleanup and Parquet conversion in
    # parallel, using multiple CPU cores rather than being limited by the GIL.
    with ProcessPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        results = list(
            executor.map(
                process_file,
                csv_files,
            )
        )

    success_count = sum(
        1
        for r in results
        if r["status"] == "success"
    )

    failed_files = [
        result["source"]
        for result in results
        if result["status"] == "failed"
    ]
    logger.info("Finished: %d succeeded.", success_count)

    if failed_files:
        logger.error("Failed files: %s", ", ".join(failed_files))
        print("Failed files:")
        for key in failed_files:
            print(key)
    else:
        logger.info("No files failed.")
        print("No files failed.")


if __name__ == "__main__":
    main()