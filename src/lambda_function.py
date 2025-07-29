import json
import logging
import os
import subprocess
import csv
from dbfread import DBF


def check_directory(path):
	return os.path.exists(path)

def fetch_himal_data(data_folder, zip_file):
	url = "https://www.himalayandatabase.com/downloads/Himalayan%20Database.zip"
	fetch_command = f"curl -s -o {data_folder}/{zip_file} {url}"

	result = subprocess.run(fetch_command.split(), capture_output=True, text=True)
	return result.returncode == 0

def unzip_himal_data(data_folder, zip_file):
	unzip_command = f"unzip {data_folder}/{zip_file} -d {data_folder}"

	result = subprocess.run(unzip_command.split(), capture_output=True, text=True)
	return result.returncode == 0

def upload_himal_data(data_folder):
	data_folder = f"{data_folder}/Himalayan Database/HIMDATA"

	for file in os.listdir(data_folder):
		if file.endswith(".DBF"):
			full_dbf_path = os.path.abspath(os.path.join(data_folder, file))
			file_csv = file.replace("DBF", "CSV")

			table = DBF(full_dbf_path)

			with open(f"./tmp/{file_csv}", 'w') as csvfile:
				writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
				writer.writerow(table.field_names)

				for record in table:
					writer.writerow(list(record.values()))

def lambda_handler(event, context):
	data_path = "./tmp"
	if not check_directory(data_path):
		os.mkdir(data_path)

	fetch_success = fetch_himal_data("./tmp", "data.zip")

	unzip_success = False
	if fetch_success:
		unzip_success = unzip_himal_data("./tmp", "data.zip")

	if unzip_success:
		upload_himal_data("./tmp")
		os.remove("./tmp/data.zip")

if __name__=="__main__":
	lambda_handler(None, None)