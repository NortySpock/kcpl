CREATE TABLE history (
   	date_of_use TEXT,
	energy_use REAL,
	peak_power_demand REAL,
	peak_time text, 
	high_temp_F REAL,
	low_temp_F REAL,
	avg_temp_F REAL,
	active int NOT NULL DEFAULT 1
);
