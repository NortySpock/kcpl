--cleanup_script
UPDATE history as history1
SET active = 0
FROM (SELECT rowid,date,active FROM history) as history2
WHERE history2.date = history1.date AND history1.rowid < history2.rowid;
