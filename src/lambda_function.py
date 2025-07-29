import logging
import os
import subprocess
import csv
from dbfread import DBF

def fetch_data(target_filename):
	url = "https://www.himalayandatabase.com/downloads/Himalayan%20Database.zip"
	fetch_command = f"curl -s -o ./tmp/{target_filename} {url}"

	result = subprocess.run(fetch_command.split(), capture_output=True, text=True)
	return result.returncode == 0

def unzip_file(source_filename):
	unzip_command = f"unzip ./tmp/{source_filename} -d ./tmp"
	result = subprocess.run(unzip_command.split(), capture_output=True, text=True)
	return result.returncode == 0

def dbf_to_csv(dbf_filepath, csv_filepath):
	table = DBF(dbf_filepath)

	with open(csv_filepath, 'w') as csvfile:
		writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
		writer.writerow(table.field_names)

		for record in table:
			writer.writerow(list(record.values()))

def upload_dbfs():
	data_folder = f"./tmp/Himalayan Database/HIMDATA"

	for file in os.listdir(data_folder):
		if file.endswith(".DBF"):
			full_dbf_path = os.path.abspath(os.path.join(data_folder, file))
			full_csv_path = os.path.join("./tmp", file.replace(".DBF", ".csv"))
			dbf_to_csv(full_dbf_path, full_csv_path)


def check_directory(path):
	return os.path.exists(path)

def lambda_handler(event, context):
	if not check_directory("./tmp"):
		os.mkdir("./tmp")

	fetch_success = fetch_data("data.zip")

	unzip_success = False
	if fetch_success:
		unzip_success = unzip_file("data.zip")

	if unzip_success:
		upload_dbfs()

if __name__=="__main__":
	lambda_handler(None, None)