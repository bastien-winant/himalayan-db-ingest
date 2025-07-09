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