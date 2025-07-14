countries_ddl = """
	CREATE TABLE IF NOT EXISTS countries (
		id INTEGER PRIMARY KEY,
		name VARCHAR(100) NOT NULL UNIQUE
	);
"""

regions_ddl = """
	CREATE TABLE IF NOT EXISTS regions (
		id INTEGER PRIMARY KEY,
		name VARCHAR(100) NOT NULL UNIQUE
	);
"""

region_hosts_ddl = """
	CREATE TABLE IF NOT EXISTS region_host_links (
		region_id INTEGER NOT NULL,
		host_id INTEGER NOT NULL,
		FOREIGN KEY (region_id) REFERENCES regions(id)
		FOREIGN KEY (host_id) REFERENCES countries(id)
	);
"""

mountains_ddl = """
	CREATE TABLE IF NOT EXISTS mountains (
		id INTEGER PRIMARY KEY,
		name VARCHAR(100) NOT NULL
	);
"""

locations_ddl = """
	CREATE TABLE IF NOT EXISTS locations (
		id INTEGER PRIMARY KEY,
		name VARCHAR(100) NOT NULL UNIQUE,
		mountain_id INTEGER,
		region_id INTEGER,
		FOREIGN KEY (mountain_id) REFERENCES mountains(id),
		FOREIGN KEY (region_id) REFERENCES regions(id)
	);
"""

peaks_ddl = """
	CREATE TABLE IF NOT EXISTS peaks (
		id CHAR(6) PRIMARY KEY,
		name VARCHAR(100) NOT NULL UNIQUE,
		location_id INTEGER,
		height INTEGER,
		open BOOLEAN,
		unlisted BOOLEAN,
		trekking BOOLEAN,
		trekyear BOOLEAN,
		restrict BOOLEAN,
		climbed INTEGER,
		peakmemo TEXT,
		refermemo TEXT,
		photomemo TEXT,
		FOREIGN KEY (location_id) REFERENCES locations (id)
	);
"""

local_names_ddl = """
	CREATE TABLE IF NOT EXISTS peak_local_names (
		peak_id INTEGER NOT NULL,
		name VARCHAR(100) NOT NULL,
		FOREIGN KEY (peak_id) REFERENCES peaks(id)
	);
"""

expedition_nations_ddl = """
	CREATE TABLE IF NOT EXISTS expedition_nations (
		expedition_id CHAR(14),
		country_id INTEGER,
		FOREIGN KEY (expedition_id) REFERENCES expeditions (id),
		FOREIGN KEY (country_id) REFERENCES conutries (id)
	);
"""

routes_ddl = """
	CREATE TABLE IF NOT EXISTS expedition_routes (
		id INTEGER PRIMARY KEY,
		expedition_id CHAR(14),
		route TEXT,
		success BOOLEAN,
		ascent TEXT,
		number INTEGER,
		FOREIGN KEY (expedition_id) REFERENCES expeditions (id)
	);
"""

expeditions_ddl = """
	CREATE TABLE IF NOT EXISTS expeditions (
		id CHAR(14) PRIMARY KEY,
		peak_id CHAR(6),
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
		o2_unkown,
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

climbers_ddl = """
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

citizenships_ddl = """
	CREATE TABLE IF NOT EXISTS citizenships (
		climber_id INTEGER,
		country_id INTEGER,
		FOREIGN KEY (climber_id) REFERENCES climbers (id),
		FOREIGN KEY (country_id) REFERENCES countries (id)
	);
"""

ascents_ddl = """
	CREATE TABLE IF NOT EXISTS ascents (
		expedition_id CHAR(14),
		summit_date DATE,
		summit_time TIME,
		route_number INTEGER,
		ascent_number INTEGER,
		summit_note TEXT,
		number INTEGER,
		FOREIGN KEY (expedition_id) REFERENCES expeditions (id),
		FOREIGN KEY (route_number) REFERENCES routes (id)
	);
"""

calamities_ddl = """
	CREATE TABLE IF NOT EXISTS calamities (
		expedition_id CHAR(14),
		climber_id INTEGER,
		date DATE,
		time TIME,
		cause TEXT,
		height INTEGER,
		class TEXT,
		note TEXT,
		route_number INTEGER,
		type VARCHAR(6),
		FOREIGN KEY (expedition_id) REFERENCES expeditions (id),
		FOREIGN KEY (climber_id) REFERENCES climbers (id)
	);
"""

participations_ddl = """
	CREATE TABLE IF NOT EXISTS participations (
		expedition_id CHAR(14),
		climber_id INTEGER,
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
		checksum INTEGER,
		FOREIGN KEY (expedition_id) REFERENCES expeditions (id),
		FOREIGN KEY (climber_id) REFERENCES climbers (id)
	);
"""

ddl_queries = [
	countries_ddl,
	regions_ddl,
	region_hosts_ddl,
	mountains_ddl,
	locations_ddl,
	peaks_ddl,
	local_names_ddl,
	expedition_nations_ddl,
	routes_ddl,
	expeditions_ddl,
	climbers_ddl,
	ascents_ddl,
	calamities_ddl,
	participations_ddl
]