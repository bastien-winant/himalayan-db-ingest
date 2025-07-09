countries_ddl_query = """
	CREATE TABLE countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);
"""

regions_ddl_query = """
	CREATE TABLE regions (
		id INTEGER PRIMARY KEY,
		name VARCHAR(100)
	);
"""

region_host_links_ddl_query = """
	CREATE TABLE region_hosts (
		region_id INTEGER,
		host_id INTEGER,
		FOREIGN KEY (region_id) REFERENCES regions (id),
		FOREIGN KEY (host_id) REFERENCES countries (id)
	);
"""

mountains_ddl_query = """
	CREATE TABLE mountains (
		id INTEGER PRIMARY KEY,
		name VARCHAR(100)
	);
"""

mountain_host_links_ddl_query = """
	CREATE TABLE mountain_hosts (
		mountain_id INTEGER,
		host_id INTEGER,
		FOREIGN KEY (mountain_id) REFERENCES mountains (id),
		FOREIGN KEY (host_id) REFERENCES countries (id)
	);
"""

locations_ddl_query = """
	CREATE TABLE locations (
		id INTEGER PRIMARY KEY,
    name TEXT,
    mountain_id INTEGER,
    FOREIGN KEY (mountain_id) REFERENCES mountains (id)
	);
"""

peaks_ddl_query = """
	CREATE TABLE peaks (
		id CHAR(6) PRIMARY KEY,
		name TEXT,
		location_id INTEGER,
		FOREIGN KEY (location_id) REFERENCES locations (id)
	);
"""

local_names_ddl_query = """
	CREATE TABLE local_names (
		peak_id INTEGER,
		name TEXT,
		FOREIGN KEY (peak_id) REFERENCES peaks (id)
	);
"""

expeditions_ddl_query = """
	CREATE TABLE expeditions (
		id CHAR(14) PRIMARY KEY,
		peak_id CHAR(6),
		year INTEGER,
		sponsor TEXT,
		claimed BOOLEAN,
		disputed BOOLEAN,
		approach TEXT,
		basecamp_date DATE,
		summit_date DATE,
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
		o2_medical BOOLEAN,
		o2_sleep BOOLEAN,
		o2_taken BOOLEAN,
		accidents TEXT,
		achievements TEXT,
		commercial_route BOOLEAN,
		standard_route BOOLEAN,
		FOREIGN KEY (peak_id) REFERENCES peaks (id)
	);
"""

climbers_ddl_query = """
	CREATE TABLE climbers (
		id INTEGER PRIMARY KEY,
		first_name VARCHAR(100),
		last_name VARCHAR(100),
		birth_year INTEGER,
		gender CHAR(1),
		occupation VARCHAR(100)
	);
"""

citizenships_ddl_query = """
	CREATE TABLE citizenships (
		climber_id INTEGER,
		country_id INTEGER,
		FOREIGN KEY (climber_id) REFERENCES climbers (id),
		FOREIGN KEY (country_id) REFERENCES countries (id)
	);
"""

routes_ddl_query = """
	CREATE TABLE routes (
		id INTEGER PRIMARY KEY,
		expedition_id CHAR(14),
		description VARCHAR(255),
		ascent VARCHAR(100),
		success BOOLEAN,
		number INTEGER,
		FOREIGN KEY (expedition_id) REFERENCES expeditions (id)
	);
"""

participations_ddl_query = """
	CREATE TABLE expeditions (
		id INTEGER PRIMARY KEY,
		expedition_id CHAR(14),
		FOREIGN KEY (expedition_id) REFERENCES expeditions (id)
	);
"""