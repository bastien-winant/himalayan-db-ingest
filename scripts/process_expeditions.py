import pandas as pd
from utils import *
from mappings import *

df = read_dbf('./data/raw/exped.DBF')

# PRIMARY KEY COLUMN
# combine expid and year to form unique pk column
df.expid = df.expid.str.cat(df.year.astype(str), sep='_')

# EXPEDITION HOST
# swap the host ids for country names
df.host = apply_map(df.host, host_map)
df = update_country_list(df, 'host')

# EXPEDITION COUNTRIES
# isolate expedition-countries combinations
df_exped_countries = df[['expid', 'countries']].dropna()

#explode comma-separated entries into scalar values
df_exped_countries.countries = df_exped_countries.countries.str.split(',')
df_exped_countries = df_exped_countries.explode('countries', ignore_index=True)
df_exped_countries.countries = df_exped_countries.countries.str.strip()

# swap country names for ids
df_exped_countries = update_country_list(df_exped_countries, 'countries')

# remove countries column from original df
df.drop('countries', axis=1, inplace=True)

# EXPEDITION NATION
# isolate expeidtion/nation combinations
df_exped_nations = df[['expid', 'nation']].dropna()

# explode slash-separated entries into scalar values
df_exped_nations.nation = df_exped_nations.nation.str.split('/')
df_exped_nations = df_exped_nations.explode('nation', ignore_index=True)
df_exped_nations.nation = df_exped_nations.nation.str.strip()

# swap country names for ids
df_exped_nations = update_country_list(df_exped_nations, 'nation')

# remove countries column from original df
df.drop('nation', axis=1, inplace=True)

# EXPEDITIONS ROUTES
df_route_1 = df.loc[
	(df.route1.notna() & df.route1 != 0) | df.ascent1.notna(),
	['expid', 'route1', 'success1', 'ascent1']]\
	.rename({'route1': 'route', 'success1': 'success', 'ascent1': 'ascent'}, axis=1)
df_route_1['number'] = 1

df_route_2 = df.loc[
	(df.route2.notna() & df.route2 != 0) | df.ascent2.notna(),
	['expid', 'route2', 'success2', 'ascent2']]\
	.rename({'route2': 'route', 'success2': 'success', 'ascent2': 'ascent'}, axis=1)
df_route_2['number'] = 2

df_route_3 = df.loc[
	(df.route3.notna() & df.route3 != 0) | df.ascent3.notna(),
	['expid', 'route3', 'success3', 'ascent3']]\
	.rename({'route3': 'route', 'success3': 'success', 'ascent3': 'ascent'}, axis=1)
df_route_3['number'] = 3

df_route_4 = df.loc[
	(df.route4.notna() & df.route4 != 0) | df.ascent4.notna(),
	['expid', 'route4', 'success4', 'ascent4']]\
	.rename({'route4': 'route', 'success4': 'success', 'ascent4': 'ascent'}, axis=1)
df_route_4['number'] = 4

df_routes = pd.concat([df_route_1, df_route_2, df_route_3, df_route_4], ignore_index=True)

df.drop(['route1', 'success1', 'ascent1', 'route2', 'success2', 'ascent2', 'route3', 'success3', 'ascent3',
				 'route4', 'success4', 'ascent4'], axis=1, inplace=True)

# CLEANUP
# recompute basecamp date where unavailable
df.loc[
	df.bcdate.isna() & df.smtdate.notna() & df.smtdays > 0, 'bcdate'] = df.apply(
	lambda row: row['smtdate'] - pd.Timedelta(days=row['smtdays']), axis=1)

# recompute summit date where unavailable
df.loc[
	df.bcdate.notna() & df.smtdate.isna() & df.smtdays > 0, 'smtdate'] = df.apply(
	lambda row: row['bcdate'] + pd.Timedelta(days=row['smtdays']), axis=1)

# recompute basecamp date where unavailable
df.loc[
	df.bcdate.isna() & df.termdate.notna() & df.totdays > 0, 'bcdate'] = df.apply(
	lambda row: row['termdate'] - pd.Timedelta(days=row['totdays']), axis=1)

# recompute termination date where unavailable
df.loc[
	df.bcdate.notna() & df.termdate.isna() & df.totdays > 0, 'termdate'] = df.apply(
	lambda row: row['bcdate'] + pd.Timedelta(days=row['totdays']), axis=1)

df.drop(['smtdays', 'totdays'], axis=1, inplace=True)

# # PRIMARY KEY
# df.expid = df.expid.str.cat(df.year.astype(str), sep='_')
#
# # EXPEDITION COUNTRIES
# # Hosts
# # replace documentation id mapping with custom mapping
# df.host = apply_map(df.host, host_map)
# df = update_country_list(df, 'host')
#
# # Nations
# # explode slash-separated values into scalar names
# df_nations = df[['expid', 'nation']]
# df_nations.nation = df_nations.nation.str.split('/')
# df_nations = df_nations.explode('nation', ignore_index=True)
#
# # swap names with country ids
# df_nations = update_country_list(df_nations, 'nation')
# df.drop('nation', axis=1, inplace=True)
#
# # Countries
# # explode comma-separated country names into scalar values
# df_countries = df[['expid', 'countries']].rename({'countries': 'country'}, axis=1)
#
# df_countries.country = df_countries.country.str.split(',')
# df_countries = df_countries.explode('country', ignore_index=True)
#
# df_countries.country = df_countries.country.str.split('/')
# df_countries = df_countries.explode('country', ignore_index=True)
#
# # swap names with country ids
# df_countries = update_country_list(df_countries, 'country')
# df.drop('countries', axis=1, inplace=True)
#
# # ROUTES
# route_1_df = df.loc[
# 	df.route1.notna() | df.success1.notna() | df.ascent1.notna(),
# 	['expid', 'route1', 'ascent1', 'success1']
# ]
# route_1_df.rename({'route1': 'route', 'ascent1': 'ascent', 'success1': 'success'}, axis=1, inplace=True)
# route_1_df['number'] = 1
#
# route_2_df = df.loc[
# 	df.route2.notna() | df.success2.notna() | df.ascent2.notna(),
# 	['expid', 'route2', 'ascent2', 'success2']
# ]
# route_2_df.rename({'route2': 'route', 'ascent2': 'ascent', 'success2': 'success'}, axis=1, inplace=True)
# route_2_df['number'] = 2
#
# route_3_df = df.loc[
# 	df.route3.notna() | df.success3.notna() | df.ascent3.notna(),
# 	['expid', 'route3', 'ascent3', 'success3']
# ]
# route_3_df.rename({'route3': 'route', 'ascent3': 'ascent', 'success3': 'success'}, axis=1, inplace=True)
# route_3_df['number'] = 3
#
# route_4_df = df.loc[
# 	df.route4.notna() | df.success4.notna() | df.ascent4.notna(),
# 	['expid', 'route4', 'ascent4', 'success4']
# ]
# route_4_df.rename({'route4': 'route', 'ascent4': 'ascent', 'success4': 'success'}, axis=1, inplace=True)
# route_4_df['number'] = 4
#
# df_routes = pd.concat([route_1_df, route_2_df, route_3_df, route_4_df], ignore_index=True)
#
# # remove route columns
# df.drop(
# 	['route1', 'ascent1', 'success1', 'route2', 'ascent2', 'success2', 'route3', 'ascent3', 'success3',
# 	 'route4', 'ascent4', 'success4'], axis=1, inplace=True)
#
# # TERMINATION REASON
# df.termreason = apply_map(df.termreason, exped_termination_map)
#
# # CLEANUP
# # recompute basecamp date where unavailable
# df.loc[
# 	df.bcdate.isna() & df.smtdate.notna() & df.smtdays.notna(), 'bcdate'] = df.apply(
# 	lambda row: row['smtdate'] - pd.Timedelta(days=row['smtdays']), axis=1)
#
# # recompute summit date where unavailable
# df.loc[
# 	df.bcdate.notna() & df.smtdate.isna() & df.smtdays.notna(), 'smtdate'] = df.apply(
# 	lambda row: row['bcdate'] + pd.Timedelta(days=row['smtdays']), axis=1)
#
# # recompute basecamp date where unavailable
# df.loc[
# 	df.bcdate.isna() & df.termdate.notna() & df.totdays.notna(), 'bcdate'] = df.apply(
# 	lambda row: row['termdate'] - pd.Timedelta(days=row['totdays']), axis=1)
#
# # recompute termination date where unavailable
# df.loc[
# 	df.bcdate.notna() & df.termdate.isna() & df.totdays.notna(), 'termdate'] = df.apply(
# 	lambda row: row['bcdate'] + pd.Timedelta(days=row['totdays']), axis=1)
#
# df.drop(
# 	['season', 'leaders', 'totmembers', 'smtmembers', 'mdeaths', 'tothired', 'smthired', 'hdeaths', 'nohired', 'smtdays', 'totdays'],
# 	axis=1, inplace=True)