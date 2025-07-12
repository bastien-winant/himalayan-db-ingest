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
		rope INTEGER,
		campsites TEXT,
		routememo TEXT,
		accidents TEXT,
		achievements TEXR,
		agency TEXT,
		commercial_route BOOLEAN BOOLEAN,
		standard_route BOOLEAN BOOLEAN,
		primary_route BOOLEAN BOOLEAN
	);
"""

ddl_queries = [
	countries_ddl,
	regions_ddl,
	region_hosts_ddl,
	mountains_ddl,
	locations_ddl,
	peaks_ddl,
	local_names_ddl
]