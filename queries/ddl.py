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
		FOREIGN KEY (region_id) REFERENCES regions(id),
		FOREIGN KEY (host_id) REFERENCES countries(id)
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
ddl_queries = []