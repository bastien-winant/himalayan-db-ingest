countries_create = """
	CREATE TABLE IF NOT EXISTS countries (
		id INTEGER PRIMARY KEY,
		name VARCHAR(100) NOT NULL UNIQUE
	);
"""

regions_create = """
	CREATE TABLE IF NOT EXISTS regions (
		id INTEGER PRIMARY KEY,
		name VARCHAR(100) NOT NULL UNIQUE
	);
"""

region_hosts_create = """
	CREATE TABLE IF NOT EXISTS region_host_links (
		region_id INTEGER NOT NULL REFERENCES regions(id),
		host_id INTEGER NOT NULL REFERENCES countries(id)
	);
"""

mountains_create = """
	CREATE TABLE IF NOT EXISTS mountains (
		id INTEGER PRIMARY KEY,
		name VARCHAR(100) NOT NULL
	);
"""

locations_create = """
	CREATE TABLE IF NOT EXISTS locations (
		id INTEGER PRIMARY KEY,
		name VARCHAR(100) NOT NULL UNIQUE,
		mountain_id INTEGER REFERENCES mountains(id),
		region_id INTEGER REFERENCES regions(id)
	);
"""

peaks_create = """
	CREATE TABLE IF NOT EXISTS peaks (
		id CHAR(6) PRIMARY KEY,
		name VARCHAR(100) NOT NULL UNIQUE,
		location_id INTEGER REFERENCES locations(id),
		height INTEGER,
		open BOOLEAN,
		unlisted BOOLEAN,
		trekking BOOLEAN,
		trekyear BOOLEAN,
		restrict BOOLEAN,
		climbed INTEGER,
		peak_memo TEXT,
		reference_memo TEXT,
		photo_memo TEXT
	);
"""

local_names_create = """
	CREATE TABLE IF NOT EXISTS peak_local_names (
		peak_id CHAR(6) NOT NULL REFERENCES peaks(id),
		name VARCHAR(100) NOT NULL
	);
"""

expeditions_create = """
	CREATE TABLE IF NOT EXISTS expeditions (
		id CHAR(14) PRIMARY KEY,
		peak_id CHAR(6) REFERENCES peaks(id),
		year INTEGER,
		sponsor TEXT,
		claimed BOOLEAN,
		disputed BOOLEAN,
		approach TEXT,
		basecamp_date DATE,
		summit_date DATE,
		summit_time TIME,
		termination_date DATE,
		termination_reason TEXT,
		termination_note TEXT,
		highpoint INTEGER,
		traverse BOOLEAN,
		ski BOOLEAN,
		parapente BOOLEAN,
		camps INTEGER,
		rope INTEGER,
		o2_climb BOOLEAN,
		o2_descent BOOLEAN,
		o2_sleep BOOLEAN,
		o2_medical BOOLEAN,
		o2_taken BOOLEAN,
		o2_unkown BOOLEAN,
		other_summits TEXT,
		campsites TEXT,
		route_memo TEXT,
		accidents TEXT,
		achievements TEXT,
		agency TEXT,
		commercial_route BOOLEAN,
		standard_route BOOLEAN,
		checksum INTEGER
	);
"""

expedition_nations_create = """
	CREATE TABLE IF NOT EXISTS expedition_nations (
		expedition_id CHAR(14) REFERENCES expeditions(id),
		country_id INTEGER REFERENCES countries(id)
	);
"""

routes_create = """
	CREATE TABLE IF NOT EXISTS expedition_routes (
		id INTEGER PRIMARY KEY,
		expedition_id CHAR(14) REFERENCES expeditions(id),
		route TEXT,
		success BOOLEAN,
		ascent TEXT,
		number INTEGER
	);
"""

climbers_create = """
	CREATE TABLE IF NOT EXISTS climbers (
		id INTEGER PRIMARY KEY,
		first_name TEXT,
		last_name TEXT,
		gender CHAR,
		birth_year INTEGER,
		residence TEXT,
		occupation TEXT,
		necrology TEXT,
		hcn TEXT
	);
"""

citizenships_create = """
	CREATE TABLE IF NOT EXISTS citizenships (
		climber_id INTEGER REFERENCES climbers(id),
		country_id INTEGER REFERENCES countries(id)
	);
"""

ascents_create = """
	CREATE TABLE IF NOT EXISTS ascents (
		expedition_id CHAR(14) REFERENCES expeditions(id),
		climber_id INTEGER REFERENCES climbers(id),
		summit_date DATE,
		summit_time TIME,
		route_number INTEGER,
		ascent_number INTEGER,
		summit_note TEXT,
		number INTEGER
	);
"""

calamities_create = """
	CREATE TABLE IF NOT EXISTS calamities (
		expedition_id CHAR(14) REFERENCES expeditions(id),
		climber_id INTEGER REFERENCES climbers(id),
		date DATE,
		time TIME,
		cause TEXT,
		height INTEGER,
		class TEXT,
		note TEXT,
		route_number INTEGER,
		type VARCHAR(6)
	);
"""

participations_create = """
	CREATE TABLE IF NOT EXISTS participations (
		expedition_id CHAR(14) REFERENCES expeditions(id),
		climber_id INTEGER REFERENCES climbers(id),
		member_id INTEGER,
		status TEXT,
		leader BOOLEAN,
		deputy BOOLEAN,
		basecamp_only BOOLEAN,
		not_to_basecamp BOOLEAN,
		support BOOLEAN,
		disabled BOOLEAN,
		hired BOOLEAN,
		sherpa BOOLEAN,
		tibetan BOOLEAN,
		sucess BOOLEAN,
		claimed BOOLEAN,
		disputed BOOLEAN,
		solo BOOLEAN,
		traverse BOOLEAN,
		ski BOOLEAN,
		parapente BOOLEAN,
		speed BOOLEAN,
		highpoint_reached BOOLEAN,
		personal_highpoint INTEGER,
		o2_used BOOLEAN,
		o2_climb BOOLEAN,
		o2_descent BOOLEAN,
		o2_sleep BOOLEAN,
		o2_medical BOOLEAN,
		o2_unknown BOOLEAN,
		o2_note TEXT,
		memo TEXT,
		outcome TEXT,
		termination_reason TEXT,
		checksum INTEGER
	);
"""

ddl_create_queries = [
	countries_create,
	regions_create,
	region_hosts_create,
	mountains_create,
	locations_create,
	peaks_create,
	local_names_create,
	expeditions_create,
	expedition_nations_create,
	routes_create,
	climbers_create,
	citizenships_create,
	ascents_create,
	calamities_create,
	participations_create
]