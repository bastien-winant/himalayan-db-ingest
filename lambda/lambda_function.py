import os
import subprocess
from dbfread import DBF
import pandas as pd
from pathlib import Path
import boto3
import logging

# Initialize the S3 client outside of the handler
s3_client = boto3.client('s3')

# fetch and unzip the raw data files
def fetch_data():
	url = "https://www.himalayandatabase.com/downloads/Himalayan%20Database.zip"
	zip_path = "/tmp/data.zip"

	try:
		fetch_command = f"curl -s -o {zip_path} {url}"
		subprocess.run(fetch_command.split(), capture_output=True, text=True)

		unzip_command = f"unzip {zip_path} -d tmp"
		subprocess.run(unzip_command.split(), capture_output=True, text=True)

		logger.info(f"Successfully fetched data and saved to {zip_path}")
	except subprocess.CalledProcessError as e:
		logger.error(f"Unable to fetch the raw data files: {str(e)}")
		raise
	except Exception as e:
		logger.error(f"Unexpected error: {str(e)}")
		raise

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
	try:
		with open(file_path, "rb") as f:
			s3.put_object(
				Bucket=bucket_name,
				Key=key,
				Body=f
			)
			logger.info(f"Successfully uploaded file {file_path} in S3 bucket {bucket_name}")
	except Exception as e:
		logger.error(f"Failed to upload CSV file to S3: {str(e)}")
		raise

def upload_data(bucket_name: str) -> None:
	"""
	Upload DBF data file as CSV to S3
	:param bucket_name: name of the S3 bucket to load the CSV files to
	:return:
	"""
	try:
		for filename in os.listdir("/tmp/Himalayan Database/HIMDATA"):
			local_path = os.path.join("/tmp/Himalayan Database/HIMDATA", filename)

			if local_path.endswith("DBF"):
				csv_filename = Path(local_path).stem + ".csv"
				csv_file_path = f"/tmp/{csv_filename}"
				df = read_dbf(local_path)
				df.to_csv(csv_file_path, index=False)

				# TODO: load dataframe directly to RDS

				upload_to_s3(csv_file_path, bucket_name, csv_filename)
	except Exception as e:
		logger.error(f"Failed to upload CSV files to S3: {str(e)}")
		raise

def handler(event, context):
	"""
	Main Lambda handler function
	Parameters:
			event: Dict containing the Lambda function event data
			context: Lambda runtime context
	Returns:
			Dict containing status message
	"""
	try:
		bucket_name = event["bucket_name"]

		fetch_data()
		upload_data(bucket_name)

		return {
			"statusCode": 200,
			"message": "Himalayan DB data processed sucessfully"
		}

	except Exception as e:
		logger.error(f"Error processing Himalayan DB data: {str(e)}")
		raise