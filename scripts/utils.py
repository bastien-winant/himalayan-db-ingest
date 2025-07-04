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

def update_country_list(df, country_col):
	new_country_df = df[[country_col]].reset_index(drop=True)
	new_country_df['country_list_name'] = new_country_df[country_col].str.strip().str.lower()
	new_country_df = new_country_df.drop(country_col, axis=1)

	try:
		country_df = pd.read_csv('../data/processed/countries.csv')
	except:
		country_df = pd.DataFrame(columns=['country_list_name'])

	country_df = pd.concat([country_df, new_country_df])\
		.drop_duplicates(ignore_index=True)

	country_df.to_csv('../data/processed/countries.csv', index=False)

	country_df.reset_index(names='country_list_id', inplace=True)
	df = df.merge(country_df, how='left', left_on=country_col, right_on='country_list_name')\
		.drop([country_col, 'country_list_name'], axis=1)\
		.rename({'country_list_id': f"{country_col}_id"}, axis=1)

	return df

def process_time_str(time_str):
	if time_str is None or len(time_str) != 4:
		return None

	hours = int(time_str[:2])
	minutes = int(time_str[2:])

	return pd.Timedelta(hours=hours, minutes=minutes)