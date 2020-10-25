WITH const(lookback) as (SELECT date(MAX(date_of_use),'-7 days') AS lookback FROM history)
UPDATE history
SET active=0
WHERE active = 1 and date_of_use >= (select lookback from const) and rowid NOT IN (
  SELECT MAX(rowid) 
  FROM history 
  WHERE date_of_use >= (select lookback from const)
  GROUP BY date_of_use
)