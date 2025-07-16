import subprocess

def fetch_file(uri, file_name, file_path):
	fetch_command = f"curl -s -o {file_path}/{file_name} {uri}"
	result = subprocess.run(fetch_command.split(), capture_output=True, text=True)
	return result.returncode

def unzip_file(file_name, file_path):
	unzip_command = f"unzip {file_path}/{file_name} -d tmp"
	result = subprocess.run(unzip_command.split(), capture_output=True, text=True)

	return result.returncode

def cleanup_file(file_name, file_path):
	cleanup_command = f"rm -rf {file_path}/{file_name}"
	result = subprocess.run(cleanup_command.split(), capture_output=True, text=True)
	return result.returncode

if __name__=="__main__":
	uri = "https://www.himalayandatabase.com/downloads/Himalayan%20Database.zip"
	file_name = "data.zip"
	file_path = "tmp"

	fetch_code = fetch_file(uri, file_name, file_path)

	unzip_code = 1
	if fetch_code == 0:
		unzip_code = unzip_file(file_name, file_path)
	print("successful fetch")
	cleanup_code = 1
	if unzip_code == 0:
		cleanup_code = cleanup_file(file_name, file_path)
	print("successlearful unzip")
	if cleanup_code == 0:
		print("Success!")