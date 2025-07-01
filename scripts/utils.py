from dbfread import DBF
import pandas as pd

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