countries_ddl_query = """
	CREATE TABLE countries (
		id SMALLINT PRIMARY KEY,
		name TEXT
	);
"""

regions_ddl_query = """
	CREATE TABLE regions (
		id SMALLINT PRIMARY KEY,
		name TEXT
	);
"""

mountains_ddl_query = """
	CREATE TABLE mountains (
		id SMALLINT PRIMARY KEY,
		name TEXT
	);
"""

locations_ddl_query = """
	CREATE TABLE locations (
		id SMALLINT PRIMARY KEY,
    name TEXT,
    mountain_id SMALLINT,
    FOREIGN KEY (mountain_id) REFERENCES mountains (id)
	);
"""

peaks_ddl_query = """
	CREATE TABLE peaks (
		id CHAR(6),
		name TEXT,
		location_id SMALLINT,
		FOREIGN KEY (location_id) REFERENCES locations (id)
	);
"""

local_names_ddl_query = """
	CREATE TABLE local_names (
		peak_id,
		name,
		FOREIGN KEY (peak_id) REFERENCES peaks (id)
	);
"""