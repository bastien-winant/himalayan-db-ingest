import pandas as pd
from utils import *
from mappings import *

# read in the raw data
df = read_dbf('../data/raw/peaks.DBF')

# MOUNTAINS AND REGIONS
# store documentation defined mappings in dfs
df_mountains = pd.DataFrame.from_dict(himal_map, orient='index', columns=['name']).reset_index(names='id')
df_regions = pd.DataFrame.from_dict(region_map, orient='index', columns=['name']).reset_index(names='id')

# PEAK LOCAL NAMES
# explode comma-separated names into scalar values
df_local_names = df[['peakid', 'pkname2']].dropna()
df_local_names['name'] = df_local_names.pkname2.str.split(',')
df_local_names = df_local_names.drop('pkname2', axis=1).explode('name')

df.drop('pkname2', axis=1, inplace=True)

# PEAK LOCATIONS
# create location id-to-name mapping
df_locations = df[['location']].drop_duplicates(ignore_index=True)\
	.reset_index(names='id')\
	.rename({'location': 'name'}, axis=1)

# replace location names with ids
df = df.merge(df_locations, left_on='location', right_on='name', how='left')\
	.drop(['location', 'name'], axis=1)\
	.rename({'id': 'location_id'}, axis=1)

# PEAK HOSTS
# replace host ids with country names
df['host'] = apply_map(df.phost, host_map).str.split(";")

# explode host names with ids and update country list
df_peak_hosts = df[['peakid', 'host']].explode('host')
df_peak_hosts = update_country_list(df_peak_hosts, 'host')

df.drop(['phost', 'host'], axis=1, inplace=True)

# CLEANUP
df = df.drop(['heightf', 'pexpid', 'psmtdate', 'pcountry', 'psummiters', 'psmtnote'], axis=1)\
	.rename({'pkname': 'name', 'heightm': 'height', 'himal': 'mountain_id', 'region': 'region_id'}, axis=1)