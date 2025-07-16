regions_insert = "INSERT INTO regions (id, name) VALUES (%s, %s);"
mountains_insert = "INSERT INTO mountains (id, name) VALUES (%s, %s);"
locations_insert = "INSERT INTO locations (id, name, mountain_id, region_id) VALUES (%s, %s, %s, %s);"
peaks_insert = """
	INSERT INTO peaks (
		id,
		name,
		location_id,
		height,
		open,
		unlisted,
		trekking,
		trekyear,
		restrict,
		climbed,
		peak_memo,
		reference_memo,
		photo_memo
	) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
local_names_insert = "INSERT INTO peak_local_names (peak_id, name) VALUES (?, ?);"
expeditions_insert = """
	INSERT INTO expeditions (
		id,
		peak_id,
		year,
		sponsor,
		claimed,
		disputed,
		approach,
		basecamp_date,
		summit_date,
		summit_time,
		termination_date,
		termination_reason,
		termination_note,
		highpoint,
		traverse,
		ski,
		parapente,
		camps,
		rope,
		o2_climb,
		o2_descent,
		o2_sleep,
		o2_medical,
		o2_taken,
		o2_unkown,
		other_summits,
		campsites,
		route_memo,
		accidents,
		achievements,
		agency,
		commercial_route,
		standard_route,
		checksum
	)
	VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s ,%s, %s ,%s, %s, %s, %s ,%s, %s);
"""