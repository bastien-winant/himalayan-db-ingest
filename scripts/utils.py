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

def apply_map(series: pd.Series, map: dict) -> pd.Series:
	"""
	Applies a key value mapping to the input series
	:param series: key values
	:param map: key-value mapping
	:return: mapped values
	"""
	return series.apply(lambda x: map.get(x))

def float_to_int(series: pd.Series) -> pd.Series:
	"""
	Convert a series of non-negative floats to integer
	:param series: non-negative floating point values
	:return: integer value
	"""
	return series.fillna(-1).astype(int).replace(-1, None)