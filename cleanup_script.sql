--cleanup_script
UPDATE history 
SET active=0
WHERE active = 1 and rowid NOT IN (
  SELECT MAX(rowid) 
  FROM history 
  GROUP BY date_of_use
)