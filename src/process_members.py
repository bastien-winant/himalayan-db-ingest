import pandas as pd
from .utils import *
from .mappings import *

df = read_dbf('./data/raw/members.DBF')

# EXPEDITION PRIMARY KEY
df.expid = df.expid.str.cat(df.myear.astype(str), sep='_')

# CLIMBERS
# create unique ids for climbers and swap in the original df
df_climbers = df[['fname', 'lname', 'sex', 'yob', 'residence', 'occupation', 'necrology', 'hcn']]\
	.drop_duplicates(ignore_index=True)\
	.reset_index(names='id')

df = df.merge(df_climbers, how='left').rename({'id': 'climber_id'}, axis=1)\
	.drop(['fname', 'lname', 'sex', 'yob', 'residence', 'occupation', 'necrology', 'age', 'birthdate',
				 'calcage', 'hcn'], axis=1)

# CITIZENSHIPS
# isolate climber-citizenship combinations
df_citizenships = df[['climber_id', 'citizen']].drop_duplicates()

# explode slash-separated entries into scaler values
df_citizenships.citizen = df_citizenships.citizen.str.split("/")
df_citizenships = df_citizenships.explode('citizen', ignore_index=True)

# swap country names for ids
df_citizenships = update_country_list(df_citizenships, 'citizen')

df.drop('citizen', axis=1, inplace=True)

# ASCENTS
df_ascent_1 = df.loc[
	df.msmtdate1.notna() |
	df.msmttime1.notna() |
	(df.mroute1 > 0) |
	(df.mascent1 > 0) |
	df.msmtnote1.notna(),
	['expid', 'msmtdate1', 'msmttime1', 'mroute1', 'mascent1', 'msmtnote1']].\
	rename({'msmtdate1': 'summit_date', 'msmttime1': 'summit_time', 'mroute1': 'route_number',
					'mascent1': 'ascent_number', 'msmtnote1': 'summit_note'}, axis=1)
df_ascent_1['number'] = 1

df_ascent_2 = df.loc[
	df.msmtdate2.notna() |
	df.msmttime2.notna() |
	(df.mroute2 > 0) |
	(df.mascent2 > 0) |
	df.msmtnote2.notna(),
	['expid', 'msmtdate2', 'msmttime2', 'mroute2', 'mascent2', 'msmtnote2']].\
	rename({'msmtdate2': 'summit_date', 'msmttime2': 'summit_time', 'mroute2': 'route_number',
					'mascent2': 'ascent_number', 'msmtnote2': 'summit_note'}, axis=1)
df_ascent_2['number'] = 2

df_ascent_3 = df.loc[
	df.msmtdate3.notna() |
	df.msmttime3.notna() |
	(df.mroute3 > 0) |
	(df.mascent3 > 0) |
	df.msmtnote3.notna(),
	['expid', 'msmtdate3', 'msmttime3', 'mroute3', 'mascent3', 'msmtnote3']].\
	rename({'msmtdate3': 'summit_date', 'msmttime3': 'summit_time', 'mroute3': 'route_number',
					'mascent3': 'ascent_number', 'msmtnote3': 'summit_note'}, axis=1)
df_ascent_3['number'] = 3

df_ascents = pd.concat([df_ascent_1, df_ascent_2, df_ascent_3], ignore_index=True)
df_ascents.summit_note = apply_map(df_ascents.summit_note, summit_note_map)

df.drop(
	['msmtdate1', 'msmttime1', 'mroute1', 'mascent1', 'msmtnote1', 'msmtdate2', 'msmttime2', 'mroute2', 'mascent2',
				 'msmtnote2', 'msmtdate3', 'msmttime3', 'mroute3', 'mascent3', 'msmtnote3'], axis=1, inplace=True)

# CALAMITIES
df_deaths = df.loc[
	df.death,
	['expid', 'climber_id', 'deathdate', 'deathtime', 'deathtype', 'deathhgtm', 'deathclass', 'deathnote', 'deathrte']]\
	.rename({'deathdate': 'date', 'deathtime': 'time', 'deathtype': 'cause', 'deathhgtm': 'height', 'deathclass': 'class',
					 'deathrte': 'route_number', 'deathnote': 'note'}, axis=1)
df_deaths['type'] = 'death'

df_injuries = df.loc[
	df.injury,
	['expid', 'climber_id', 'injurydate', 'injurytime', 'injurytype', 'injuryhgtm', 'deathnote']]\
	.rename({'injurydate': 'date', 'injurytime': 'time', 'injurytype': 'cause', 'injuryhgtm': 'height',
					 'deathnote': 'note'}, axis=1)
df_injuries['type'] = 'injury'

# combine injuries and deaths dfs
df_calamities = pd.concat([df_deaths, df_injuries], ignore_index=True)

df_calamities['class'] = float_to_int(df_calamities['class'])
df_calamities['route_number'] = float_to_int(df_calamities['route_number'])

df_calamities.cause = apply_map(df_calamities.cause, cause_map)
df_calamities['class'] = apply_map(df_calamities['class'], death_class_map)

df.drop(['death', 'deathdate', 'deathtime', 'deathtype', 'deathhgtm', 'deathclass', 'deathnote', 'deathrte',
				 'injury', 'injurydate', 'injurytime', 'injurytype', 'injuryhgtm', 'ams', 'weather'], axis=1, inplace=True)

df['mo2used'] = (df.mo2climb | df.mo2descent | df.mo2medical | df.mo2sleep) | df.mo2used
df['mo2unkwn'] = ~df.mo2used & ~df.mo2none

df.drop(['peakid', 'myear', 'mseason', 'mo2none'], axis=1, inplace=True)

# apply summit bid mappings
df.msmtbid = apply_map(df.msmtbid, bid_map)
df.msmtterm = apply_map(df.msmtterm, bid_termination_map)