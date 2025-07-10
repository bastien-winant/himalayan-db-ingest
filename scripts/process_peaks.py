import pandas as pd
from utils import *
from mappings import *

# read in the raw data
df = read_dbf('./data/raw/peaks.DBF')

# REGION & HOSTS
# define official region id mapping as df
df_regions = pd.DataFrame.from_dict(region_map, orient='index', columns=['name']).reset_index(names='id')

# isolate unique region/host combinations
df_host_regions = df[['region', 'phost']]\
	.drop_duplicates()\
	.rename({'region': 'region_id'}, axis=1)

# retrieve host names from host mapping
df_host_regions['host'] = apply_map(df_host_regions.phost, host_map)
df_host_regions.drop('phost', axis=1, inplace=True)

# explode semicolumn-separated values into scalar values
df_host_regions.host = df_host_regions.host.str.split(';')
df_host_regions = df_host_regions.explode('host', ignore_index=True)

# swap host names with country ids
df_host_regions = update_country_list(df_host_regions, 'host')

# MOUNTAIN & HOSTS
# define official mountain id mapping as df
df_mountains = pd.DataFrame.from_dict(himal_map, orient='index', columns=['name']).reset_index(names='id')

# isolate unique moutain/host combinations and get host names
df_mountain_regions = df[['himal', 'region']]\
	.drop_duplicates(ignore_index=True)\
	.rename({'region': 'region_id', 'himal': 'mountain_id'}, axis=1)

# LOCATIONS
df_locations = df[['location', 'himal', 'region']]\
	.rename({'location': 'location_id', 'himal': 'mountain_id', 'region': 'region_id'}, axis=1)\
	.drop_duplicates(ignore_index=True)\
	.reset_index(names='id')

# LOCAL NAMES
# isolate peakid/local name combinations
df_local_names = df[['peakid', 'pkname2']].dropna().rename({'pkname2': 'name'}, axis=1)

# explode comma-separated names into scalar values
df_local_names.name = df_local_names.name.str.split(',')
df_local_names = df_local_names.explode('name', ignore_index=True)

# clean up names
df_local_names.name = df_local_names.name.str.strip()

# PEAKS
df_peaks = df.drop(
	['pkname2', 'heightf', 'himal', 'region', 'phost', 'pyear', 'pseason',
       'pexpid', 'psmtdate', 'pcountry', 'psummiters', 'psmtnote'], axis=1)\
	.rename({'peakid': 'id', 'pkname': 'name', 'location': 'location_id', 'heightm': 'height', 'pstatus': 'climbed'},
					axis=1)