import pandas as pd
from utils import *
from mappings import *

df = read_dbf('../data/raw/members.DBF')

# PRIMARY KEY
df.expid = df.expid.str.cat(df.myear.astype(str), sep='_')

# CLIMBERS
# isolate columns pertaining to an individual climber
df_climbers = df[['fname', 'lname', 'sex', 'yob', 'occupation', 'residence', 'citizen', 'hcn']]\
	.drop_duplicates(ignore_index=True)\
	.reset_index(names='id')

# swap climber info for climber id in expeditions df
df = df.merge(df_climbers, how='left')\
	.rename({'id': 'climber_id'}, axis=1)\
	.drop(['fname', 'lname', 'sex', 'yob', 'occupation', 'residence', 'citizen', 'age', 'calcage',
				 'birthdate', 'hcn'], axis=1)

# CLIMBER CITIZENSHIPS
# explode slash-separated countries into scalar values
df_citizenships = df_climbers[['id', 'citizen']].drop_duplicates().rename({'id': 'climber_id'}, axis=1)
df_citizenships.citizen = df_citizenships.citizen.str.split('/')
df_citizenships = df_citizenships.explode('citizen').drop_duplicates(ignore_index=True)

df_citizenships = update_country_list(df_citizenships, 'citizen')

df_climbers.drop('citizen', axis=1, inplace=True)

# ASCENSIONS
ascent_1_df = df.loc[
	df.msmtdate1.notna() |
	df.msmttime1.notna() |
	(df.mroute1.notna() & df.mroute1 != 0) |
	(df.mascent1.notna() & df.mascent1 != 0),
	['expid', 'climber_id', 'msmtdate1', 'msmttime1', 'mroute1', 'mascent1', 'msmtnote1']]\
	.rename({'msmtdate1': 'date', 'msmttime1': 'time', 'mroute1': 'route', 'mascent1': 'ascent', 'msmtnote1': 'note'}, axis=1)
ascent_1_df['number'] = 1

ascent_2_df = df.loc[
	df.msmtdate2.notna() |
	df.msmttime2.notna() |
	(df.mroute2.notna() & df.mroute2 != 0) |
	(df.mascent2.notna() & df.mascent2 != 0),
	['expid', 'climber_id', 'msmtdate2', 'msmttime2', 'mroute2', 'mascent2', 'msmtnote2']]\
	.rename({'msmtdate2': 'date', 'msmttime2': 'time', 'mroute2': 'route', 'mascent2': 'ascent', 'msmtnote2': 'note'}, axis=1)
ascent_2_df['number'] = 2

ascent_3_df = df.loc[
	df.msmtdate3.notna() |
	df.msmttime3.notna() |
	(df.mroute3.notna() & df.mroute3 != 0) |
	(df.mascent3.notna() & df.mascent3 != 0),
	['expid', 'climber_id', 'msmtdate3', 'msmttime3', 'mroute3', 'mascent3', 'msmtnote3']]\
	.rename({'msmtdate3': 'date', 'msmttime3': 'time', 'mroute3': 'route', 'mascent3': 'ascent', 'msmtnote3': 'note'}, axis=1)
ascent_3_df['number'] = 3

df_ascents = pd.concat([ascent_1_df, ascent_2_df, ascent_3_df], ignore_index=True)

df = df.drop(
	['msmtdate1', 'msmttime1', 'mroute1', 'mascent1', 'msmtnote1', 'msmtdate2', 'msmttime2', 'mroute2', 'mascent2', 'msmtnote2',
	 'msmtdate3', 'msmttime3', 'mroute3', 'mascent3', 'msmtnote3'], axis=1)\
	.drop_duplicates()

# CALAMITIES
# Deaths
df_deaths = df.loc[
	df.death,
	['expid', 'climber_id', 'death', 'deathdate', 'deathtime', 'deathtype', 'deathhgtm', 'deathclass', 'ams', 'weather',
	 'deathnote', 'deathrte']]\
	.drop('death', axis=1)\
	.rename({'deathdate': 'date', 'deathtime': 'time', 'deathtype': 'cause', 'deathhgtm': 'altitude', 'deathclass': 'class',
					 'deathnote': 'note', 'deathrte': 'route'}, axis=1)
df_deaths['type'] = 'death'
df_deaths.route = float_to_int(df_deaths.route)

# Injuries
df_injuries = df.loc[
	df.injury,
	['expid', 'climber_id', 'injury', 'injurydate', 'injurytime', 'injurytype', 'injuryhgtm', 'deathnote']]\
	.drop('injury', axis=1)\
	.rename({'injurydate': 'date', 'injurytime': 'time', 'injurytype': 'cause', 'injuryhgtm': 'altitude', 'deathnote': 'note'},
					axis=1)
df_injuries['type'] = 'injury'

# Calamities
df_calamities = pd.concat([df_deaths, df_injuries], ignore_index=True)

df.drop(
	['death', 'deathdate', 'deathtime', 'deathtype', 'deathhgtm', 'deathclass', 'ams', 'weather', 'deathnote', 'deathrte',
	 'injury', 'injurydate', 'injurytime', 'injurytype', 'injuryhgtm', 'deathnote'], axis=1, inplace=True)