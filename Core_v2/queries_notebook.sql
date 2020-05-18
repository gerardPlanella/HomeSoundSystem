--+ &&0
DROP TABLE IF EXISTS EventLog CASCADE;
CREATE TABLE EventLog (
    location varchar(255),
    time timeStamp,
    type int,
    power numeric,
    PRIMARY KEY (location, time, type)
);

--+ &&@
INSERT INTO EventLog
VALUES (%s, %s, %s, %s);

-- &&1
SELECT COUNT(*) AS nEvents
FROM EventLog
WHERE
    MOD((newTime - time), 24*3600) > newPeriod AND
    (newTime - time) / (24*3600) <= newAmountOfDays;

-- &&2
SELECT COUNT(*) AS nEvents
FROM EventLog
WHERE
    MOD((newTime - time), 24*3600) > newPeriod AND
    (newTime - time) / (24*3600) <= newAmountOfDays AND
    location like newLocation;

-- &&3
SELECT type
FROM EventLog
ORDER BY time DESC
LIMIT 1;

-- &&4
SELECT type
FROM EventLog
WHERE location like newLocation
ORDER BY time DESC
LIMIT 1;

-- &&5
SELECT COUNT(*)
FROM EventLog
WHERE (newTime1 < time) AND (newTime2 > time) AND type = %s;

-- &&6
SELECT COUNT(*)
FROM EventLog
WHERE
    (newTime1 < time) AND (newTime2 > time) AND
    location like newLocation;

-- &&7
SELECT type, COUNT(*) AS nEvents
FROM EventLog
WHERE
    MOD((newTime - time), 24*3600) > newPeriod AND
    (newTime - time) / (24*3600) <= newAmountOfDays
GROUP BY type
LIMIT 1;

-- &&8
SELECT type, COUNT(*) AS nEvents
FROM EventLog
WHERE
    MOD((newTime - time), 24*3600) > newPeriod AND
    (newTime - time) / (24*3600) <= newAmountOfDays AND
    location like newLocation
GROUP BY type
LIMIT 1;
