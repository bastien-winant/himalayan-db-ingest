countries_drop = "DROP TABLE IF EXISTS countries;"
regions_drop = "DROP TABLE IF EXISTS regions;"
region_hosts_drop = "DROP TABLE IF EXISTS region_host_links;"
mountains_drop = "DROP TABLE IF EXISTS mountains;"
locations_drop = "DROP TABLE IF EXISTS locations;"
peaks_drop = "DROP TABLE IF EXISTS peaks;"
local_names_drop = "DROP TABLE IF EXISTS peak_local_names;"
expeditions_drop = "DROP TABLE IF EXISTS expeditions;"
expedition_nations_drop = "DROP TABLE IF EXISTS expedition_nations;"
routes_drop = "DROP TABLE IF EXISTS routes;"
climbers_drop = "DROP TABLE IF EXISTS climbers;"
citizenships_drop = "DROP TABLE IF EXISTS citizenships;"
ascents_drop = "DROP TABLE IF EXISTS ascents;"
calamities_drop = "DROP TABLE IF EXISTS calamities;"
participations_drop = "DROP TABLE IF EXISTS participations;"

ddl_drop_queries = [
	participations_drop,
	calamities_drop,
	ascents_drop,
	routes_drop,
	citizenships_drop,
	climbers_drop,
	expedition_nations_drop,
	expeditions_drop,
	local_names_drop,
	peaks_drop,
	locations_drop,
	region_hosts_drop,
	regions_drop,
	mountains_drop,
	countries_drop
]