import pandas as pd
from utils import *
from mappings import *

# read in the raw data
df = read_dbf('./data/raw/peaks.DBF')

# MOUNTAINS
# store documentation defined mapping in dfs
df_mountains = pd.DataFrame.from_dict(himal_map, orient='index', columns=['name']).reset_index(names='id')

# merge in host countries
df_mountains = df_mountains.merge(df[['himal', 'phost']], how='left', left_on='id', right_on='himal')\
	.drop_duplicates(ignore_index=True)

df_mountains.phost = float_to_int(df_mountains.phost)
df_mountains.drop('himal', axis=1, inplace=True)

# convert host ids to names and explode into scalar values
df_mountains['host'] = apply_map(df_mountains.phost, host_map).str.split(';')
df_mountains = df_mountains.explode('host').drop('phost', axis=1).drop_duplicates()
df_mountains = update_country_list(df_mountains, 'host')

# isolate mountain-host many-to-many relationship
df_mountain_host_links = df_mountains[['id', 'host_id']].rename({'id': 'mountain_id'}, axis=1)
df_mountains = df_mountains.drop('host_id', axis=1).drop_duplicates()

# REGIONS
# store documentation defined mapping in df
df_regions = pd.DataFrame.from_dict(region_map, orient='index', columns=['name']).reset_index(names='id')

# merge in host country ids
df_regions = (df_regions.merge(df[['region', 'phost']], how='left', left_on='id', right_on='region')\
							.drop_duplicates(ignore_index=True))

df_regions.phost = float_to_int(df_regions.phost)
df_regions.drop('region', axis=1, inplace=True)

# convert host ids to names and explode into scalar values
df_regions['host'] = apply_map(df_regions.phost, host_map).str.split(';')
df_regions = df_regions.explode('host').drop('phost', axis=1).drop_duplicates()
df_regions = update_country_list(df_regions, 'host')

# isolate region-host many-to-many relationship
df_region_host_links = df_regions[['id', 'host_id']].rename({'id': 'region_id'}, axis=1)
df_regions = df_regions.drop('host_id', axis=1).drop_duplicates()

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

# PEAKS CLEANUP
df = df.drop(['heightf', 'pexpid', 'psmtdate', 'pcountry', 'psummiters', 'psmtnote'], axis=1)\
	.rename({'pkname': 'name', 'heightm': 'height', 'himal': 'mountain_id', 'region': 'region_id'}, axis=1)