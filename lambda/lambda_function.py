import os
import subprocess
from dbfread import DBF
import pandas as pd
from pathlib import Path
import boto3

s3_client = boto3.client('s3')

# fetch and unzip the raw data files
def fetch_data():
	url = "https://www.himalayandatabase.com/downloads/Himalayan%20Database.zip"
	zip_path = "/tmp/data.zip"

	fetch_command = f"curl -s -o {zip_path} {url}"
	fetch_result = subprocess.run(fetch_command.split(), capture_output=True, text=True)

	if fetch_result.returncode == 0:
		unzip_command = f"unzip {zip_path} -d tmp"
		unzip_result = subprocess.run(unzip_command.split(), capture_output=True, text=True)
		return unzip_result.returncode
	else:
		return 1

# read the dbf file into a pandas dataframe with basic data cleaning
def read_dbf(file_path: str) -> pd.DataFrame:
	"""
	Reads in DBF file data and performs basic cleaning
	:param file_path: DBF path file
	:return: pd.DataFrame: (roughly) clean dataset
	"""
	dbf = DBF(file_path)
	df = pd.DataFrame(iter(dbf))

	df.replace('', None, inplace=True)
	df.where(df.notna(), None, inplace=True)

	df.columns = [col.lower() for col in df.columns]

	return df

def upload_to_s3(file_path, bucket_name, key):
	with open(file_path, "rb") as f:
		s3.put_object(
			Bucket=bucket_name,
			Key=key,
			Body=f
		)
		print(f"Uploaded to s3://{bucket_name}/{key}")

def upload_data(bucket_name):
	for filename in os.listdir("/tmp/Himalayan Database/HIMDATA"):
		local_path = os.path.join("/tmp/Himalayan Database/HIMDATA", filename)

		if local_path.endswith("DBF"):
			csv_filename = Path(local_path).stem + ".csv"
			csv_file_path = f"/tmp/{csv_filename}"
			df = read_dbf(local_path)
			df.to_csv(csv_file_path, index=False)

			upload_to_s3(csv_file_path, bucket_name, csv_filename)

# def handler(event, context):
def handler():
	bucket_name = "data_bucket_name"

	fetch_outcome = fetch_data()

	if fetch_outcome == 0:
		upload_data(bucket_name)