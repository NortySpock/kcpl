INSERT INTO history (date,energy_use ,peak_power_demand, peak_time, high_temp_F, low_temp_F, avg_temp_F)
VALUES('1970-01-01',6.28,3.14,'13:00:00',80,70,75);

ALTER TABLE history
ADD COLUMN active int;