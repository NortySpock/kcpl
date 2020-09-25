CREATE TABLE history (
   	date TEXT,
	energy_use REAL,
	peak_power_demand REAL,
	peak_time text, 
	high_temp_F int,
	low_temp_F int,
	avg_temp_F int,
	active int NOT NULL DEFAULT 1
);
